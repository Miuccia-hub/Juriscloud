from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any
from uuid import uuid4

import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from rank_bm25 import BM25Okapi

from services.text_chunker import DocumentChunk
from services.legal_sections import requested_articles


load_dotenv()


@dataclass(frozen=True)
class SearchResult:
    """A passage returned by semantic search."""

    text: str
    document_id: str
    filename: str
    chunk_index: int
    distance: float | None
    page_number: int | None = None
    section: str | None = None
    article_number: str | None = None

    @property
    def citation_label(self) -> str:
        if self.page_number is not None:
            return f"{self.filename}, page {self.page_number}"

        if self.section:
            return f"{self.filename}, {self.section}"

        return self.filename


class JurisourceVectorStore:
    """Store and retrieve legal document passages with ChromaDB."""

    def __init__(
        self,
        api_key: str,
        collection_name: str = "jurisource_legal_sources",
    ) -> None:
        cleaned_api_key = api_key.strip()

        if not cleaned_api_key:
            raise ValueError(
                "An OpenAI API key is required."
            )

        self.embedding_model = os.getenv(
            "OPENAI_EMBEDDING_MODEL",
            "text-embedding-3-large",
        )

        self.openai_client = OpenAI(
            api_key=cleaned_api_key
        )

        # Each user session receives an isolated in-memory database.
        self.chroma_client = chromadb.EphemeralClient()

        session_collection_name = (
            f"{collection_name}_{uuid4().hex}"
        )

        self.collection = (
            self.chroma_client.get_or_create_collection(
                name=session_collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        )

    def _create_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Create OpenAI embeddings for a list of passages."""

        if not texts:
            return []

        response = self.openai_client.embeddings.create(
            model=self.embedding_model,
            input=texts,
            encoding_format="float",
        )

        ordered_items = sorted(
            response.data,
            key=lambda item: item.index,
        )

        return [
            item.embedding
            for item in ordered_items
        ]

    def index_chunks(
        self,
        chunks: list[DocumentChunk],
        batch_size: int = 50,
    ) -> int:
        """Add document chunks to ChromaDB in small batches."""

        if not chunks:
            return 0

        indexed_count = 0

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start : start + batch_size]
            texts = [chunk.text for chunk in batch]
            embeddings = self._create_embeddings(texts)

            self.collection.upsert(
                ids=[
                    chunk.chunk_id
                    for chunk in batch
                ],
                documents=texts,
                embeddings=embeddings,
                metadatas=[
                    chunk.to_metadata()
                    for chunk in batch
                ],
            )

            indexed_count += len(batch)

        return indexed_count

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """Remove all indexed passages belonging to one document."""

        self.collection.delete(
            where={
                "document_id": {
                    "$eq": document_id
                }
            }
        )

    def search(
        self,
        question: str,
        document_ids: list[str] | None = None,
        top_k: int = 8,
    ) -> list[SearchResult]:
        """Find the most relevant passages for a question."""

        cleaned_question = question.strip()

        if not cleaned_question:
            return []

        if self.collection.count() == 0:
            return []

        document_filter = None
        if document_ids is not None:
            if not document_ids:
                return []
            document_filter = {"document_id": {"$in": document_ids}}

        articles = requested_articles(cleaned_question)
        if articles:
            article_filter = {"article_number": {"$in": list(articles)}}
            where = {"$and": [document_filter, article_filter]} if document_filter else article_filter
            exact = self.collection.get(where=where, include=["documents", "metadatas"])
            results = self._records_to_results(exact)
            # Do not answer a provision question from unrelated semantic matches.
            if not set(articles).issubset({r.article_number for r in results}):
                return []
            return sorted(results, key=lambda r: (r.document_id, r.chunk_index))

        query_embedding = self._create_embeddings(
            [cleaned_question]
        )[0]

        query_arguments: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": min(max(top_k * 3, 1), self.collection.count()),
            "include": [
                "documents",
                "metadatas",
                "distances",
            ],
        }

        if document_ids:
            if len(document_ids) == 1:
                query_arguments["where"] = {
                    "document_id": {
                        "$eq": document_ids[0]
                    }
                }
            else:
                query_arguments["where"] = {
                    "document_id": {
                        "$in": document_ids
                    }
                }

        raw_results = self.collection.query(
            **query_arguments
        )

        documents = (
            raw_results.get("documents") or [[]]
        )[0]

        metadatas = (
            raw_results.get("metadatas") or [[]]
        )[0]

        distances = (
            raw_results.get("distances") or [[]]
        )[0]

        search_results: list[SearchResult] = []

        for index, text in enumerate(documents):
            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            ) or {}

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            page_number = metadata.get("page_number")

            if not isinstance(page_number, int):
                page_number = None

            chunk_index = metadata.get(
                "chunk_index",
                index,
            )

            if not isinstance(chunk_index, int):
                chunk_index = index

            search_results.append(
                SearchResult(
                    text=text,
                    document_id=str(
                        metadata.get(
                            "document_id",
                            "",
                        )
                    ),
                    filename=str(
                        metadata.get(
                            "filename",
                            "Untitled document",
                        )
                    ),
                    chunk_index=chunk_index,
                    page_number=page_number,
                    section=metadata.get("section"),
                    article_number=metadata.get("article_number"),
                    distance=(
                        float(distance)
                        if distance is not None
                        else None
                    ),
                )
            )

        # Fuse keyword and semantic ranks for general questions.
        arguments = {"include": ["documents", "metadatas"]}
        if document_filter:
            arguments["where"] = document_filter
        records = self.collection.get(**arguments)
        lexical_results = self._records_to_results(records)
        tokens = lambda value: re.findall(r"\w+", value.lower())
        corpus = [tokens(r.text) for r in lexical_results]
        if not corpus or not any(corpus):
            return search_results[:top_k]
        scores = BM25Okapi(corpus).get_scores(tokens(cleaned_question))
        ranked_lexical = sorted(
            [(r, score) for r, score in zip(lexical_results, scores) if score > 0],
            key=lambda pair: pair[1], reverse=True,
        )[:top_k * 3]
        fused = {}
        result_map = {}
        for ranking in (search_results, [r for r, _ in ranked_lexical]):
            for rank, result in enumerate(ranking, start=1):
                key = (result.document_id, result.chunk_index)
                fused[key] = fused.get(key, 0) + 1 / (60 + rank)
                result_map[key] = result
        return [result_map[key] for key in sorted(fused, key=fused.get, reverse=True)[:top_k]]

    @staticmethod
    def _records_to_results(records: dict[str, Any]) -> list[SearchResult]:
        return [SearchResult(
            text=text,
            document_id=str(metadata.get("document_id", "")),
            filename=str(metadata.get("filename", "Untitled document")),
            chunk_index=int(metadata.get("chunk_index", 0)),
            distance=None,
            page_number=metadata.get("page_number"),
            section=metadata.get("section"),
            article_number=metadata.get("article_number"),
        ) for text, metadata in zip(
            records.get("documents") or [], records.get("metadatas") or []
        )]

    def has_document(
        self,
        document_id: str,
    ) -> bool:
        """Check whether a document has already been indexed."""

        result = self.collection.get(
            where={
                "document_id": {
                    "$eq": document_id
                }
            },
            limit=1,
            include=["metadatas"],
        )

        record_ids = result.get("ids") or []
        return bool(record_ids)

    def count(self) -> int:
        """Return the number of indexed passages."""

        return self.collection.count()
