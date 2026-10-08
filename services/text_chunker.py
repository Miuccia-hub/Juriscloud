from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.legal_sections import article_units


@dataclass(frozen=True)
class DocumentChunk:
    """A searchable passage from a legal document."""

    chunk_id: str
    document_id: str
    filename: str
    text: str
    chunk_index: int
    page_number: int | None = None
    section: str | None = None
    article_number: str | None = None

    @property
    def word_count(self) -> int:
        return len(self.text.split())

    @property
    def citation_label(self) -> str:
        if self.page_number:
            return f"{self.filename}, page {self.page_number}"

        if self.section:
            return f"{self.filename}, {self.section}"

        return self.filename

    def to_metadata(self) -> dict[str, str | int]:
        metadata: dict[str, str | int] = {
            "document_id": self.document_id,
            "filename": self.filename,
            "chunk_index": self.chunk_index,
            "word_count": self.word_count,
        }

        if self.page_number is not None:
            metadata["page_number"] = self.page_number

        if self.section:
            metadata["section"] = self.section

        if self.article_number:
            metadata["article_number"] = self.article_number

        return metadata


def _read_attribute(
    item: Any,
    *attribute_names: str,
    default: Any = None,
) -> Any:
    """Read the first available attribute from an object."""

    for attribute_name in attribute_names:
        value = getattr(item, attribute_name, None)

        if value is not None:
            return value

    return default


def _document_text(document: Any) -> str:
    """Return the complete document text when blocks are unavailable."""

    value = _read_attribute(
        document,
        "full_text",
        "text",
        "content",
        default="",
    )

    return str(value).strip() if value else ""


def _document_filename(document: Any) -> str:
    """Return a display name for the document."""

    value = _read_attribute(
        document,
        "filename",
        "file_name",
        "name",
        default="Untitled document",
    )

    return str(value)


def _document_id(document: Any) -> str:
    """Return or generate a stable document identifier."""

    existing_id = _read_attribute(
        document,
        "document_id",
        "id",
        default=None,
    )

    if existing_id:
        return str(existing_id)

    fingerprint = (
        f"{_document_filename(document)}:"
        f"{_document_text(document)}"
    )

    return sha256(fingerprint.encode("utf-8")).hexdigest()


def _block_page_number(block: Any) -> int | None:
    """Extract a page number from a parsed block."""

    page_number = _read_attribute(
        block,
        "page_number",
        "page",
        default=None,
    )

    if isinstance(page_number, int):
        return page_number

    metadata = _read_attribute(block, "metadata", default={})

    if isinstance(metadata, dict):
        metadata_page = metadata.get("page_number") or metadata.get("page")

        if isinstance(metadata_page, int):
            return metadata_page

    return None


def _block_section(block: Any) -> str | None:
    """Extract a heading or section name from a parsed block."""

    section = _read_attribute(
        block,
        "section",
        "section_title",
        "heading",
        default=None,
    )

    if section:
        return str(section).strip()

    metadata = _read_attribute(block, "metadata", default={})

    if isinstance(metadata, dict):
        metadata_section = (
            metadata.get("section")
            or metadata.get("section_title")
            or metadata.get("heading")
        )

        if metadata_section:
            return str(metadata_section).strip()

    return None


def _block_text(block: Any) -> str:
    """Extract text from a parsed block."""

    text = _read_attribute(
        block,
        "text",
        "content",
        default="",
    )

    return str(text).strip() if text else ""


def chunk_document(
    document: Any,
    chunk_size: int = 1400,
    chunk_overlap: int = 220,
) -> list[DocumentChunk]:
    """
    Split a parsed legal document into searchable passages.

    Each resulting passage keeps its document name, page number and
    section information so Jurisource can later produce citations.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative.")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            "; ",
            "。 ",
            "？",
            "！",
            "；",
            " ",
            "",
        ],
    )

    filename = _document_filename(document)
    # Version the index so hot reloads do not reuse chunks without article metadata.
    document_id = _document_id(document) + ":articles-v1"
    blocks = _read_attribute(document, "blocks", default=[]) or []

    source_units: list[tuple[str, int | None, str | None]] = []

    for block in blocks:
        text = _block_text(block)

        if not text:
            continue

        source_units.append(
            (
                text,
                _block_page_number(block),
                _block_section(block),
            )
        )

    if not source_units:
        complete_text = _document_text(document)

        if complete_text:
            source_units.append((complete_text, None, None))

    chunks: list[DocumentChunk] = []
    chunk_index = 0

    current_article = None
    structured_units = []
    for source_text, page_number, section in source_units:
        units, current_article = article_units(source_text, current_article)
        for unit_text, article_number in units:
            structured_units.append((unit_text, page_number, section, article_number))

    for source_text, page_number, section, article_number in structured_units:
        split_passages = splitter.split_text(source_text)

        for passage in split_passages:
            cleaned_passage = passage.strip()

            if not cleaned_passage:
                continue

            chunk_fingerprint = (
                f"{document_id}:"
                f"{chunk_index}:"
                f"{page_number}:"
                f"{cleaned_passage}"
            )

            chunk_id = sha256(
                chunk_fingerprint.encode("utf-8")
            ).hexdigest()

            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    filename=filename,
                    text=cleaned_passage,
                    chunk_index=chunk_index,
                    page_number=page_number,
                    section=section,
                    article_number=article_number,
                )
            )

            chunk_index += 1

    return chunks


def chunk_documents(
    documents: list[Any],
    chunk_size: int = 1400,
    chunk_overlap: int = 220,
) -> list[DocumentChunk]:
    """Split several parsed documents into one searchable collection."""

    all_chunks: list[DocumentChunk] = []

    for document in documents:
        all_chunks.extend(
            chunk_document(
                document=document,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        )

    return all_chunks
