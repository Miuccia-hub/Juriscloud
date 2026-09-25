from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

from services.text_chunker import DocumentChunk


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

        self.collection = (
            self.chroma_client.get_or_create_collection(
                name=collection_name,
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
                ids=[chunk.chunk_id for chunk in batch],
                documents=texts,
                embeddings=embeddings,
                metadatas=[
                    chunk.to_metadata()
                    for chunk in batch
                ],
            )

            indexed_count += len(batch)

        return indexed_count

def delete_document(self, document_id: str) -> None:
        """Remove all indexed passages belonging to one document."""

        self.collection.delete(
            where={"document_id": {"$eq": document_id}}
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

        query_embedding = self._create_embeddings(
            [cleaned_question]
        )[0]

        query_arguments: dict[str, Any] = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
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

        documents = (raw_results.get("documents") or [[]])[0]
        metadatas = (raw_results.get("metadatas") or [[]])[0]
        distances = (raw_results.get("distances") or [[]])[0]

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

            chunk_index = metadata.get("chunk_index", index)

            if not isinstance(chunk_index, int):
                chunk_index = index

            search_results.append(
                SearchResult(
                    text=text,
                    document_id=str(
                        metadata.get("document_id", "")
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
                    distance=(
                        float(distance)
                        if distance is not None
                        else None
                    ),
                )
            )

        return search_results
def has_document(self, document_id: str) -> bool:
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
    