from pathlib import Path
import os

import chromadb
import pytest

from services.document_parser import ParsedBlock, ParsedDocument, parse_document
from services.text_chunker import chunk_document
from services.vector_store import JurisourceVectorStore
from services.answer_generator import stream_grounded_answer, _build_source_context
from services.legal_sections import requested_articles


def document(blocks, name="Act.pdf"):
    return ParsedDocument(name, name, ".pdf", name, tuple(blocks))


def store_chunks(chunks):
    store = JurisourceVectorStore.__new__(JurisourceVectorStore)
    store.chroma_client = chromadb.EphemeralClient()
    from uuid import uuid4
    store.collection = store.chroma_client.create_collection("test_" + uuid4().hex)
    # Deterministic embeddings: exact article retrieval must not call a model.
    store._create_embeddings = lambda texts: [[1.0, 0.0] for _ in texts]
    store.index_chunks(chunks)
    return store


@pytest.fixture
def chunks():
    return chunk_document(document([
        ParsedBlock("Article 4\nAI literacy\nProviders promote literacy.", page_number=12),
        ParsedBlock("CHAPTER II\nArticle 5\nProhibited AI practices\n1. Manipulation is prohibited.", page_number=13),
        ParsedBlock("2. Biometric identification restrictions.\n" * 200, page_number=14),
        ParsedBlock("3. Safeguards for authorisation.", page_number=15),
        ParsedBlock("5. Member States shall lay down detailed rules.", page_number=16),
        ParsedBlock("8. Other Union law applies.\nArticle 6\nHigh-risk classification\nClassification rules.", page_number=17),
        ParsedBlock("References to Articles 5, 6, and 7 of Regulation 1025/2012.\nArticle 41\nCommon specifications\n1. Commission may adopt specifications.", page_number=50),
        ParsedBlock("5. Providers justify alternative solutions.\n6. Notify the Commission.", page_number=51),
        ParsedBlock("ANNEX I\nProduct legislation.", page_number=130),
    ]))


@pytest.mark.parametrize("question", ["What is Article 5?", "EU ai act的article5是什么", "解释第5条", "Explain Art. 5"])
def test_question_numbers(question):
    assert requested_articles(question) == ("5",)


def test_article_boundaries_and_cross_references(chunks):
    fifth = [c for c in chunks if c.article_number == "5"]
    assert {c.page_number for c in fifth} == {13, 14, 15, 16, 17}
    assert all("High-risk classification" not in c.text for c in fifth)
    assert all(c.article_number == "41" for c in chunks if c.page_number == 51)
    assert all(c.article_number is None for c in chunks if c.page_number == 130)


def test_exact_retrieval_complete_and_no_embedding_call(chunks):
    store = store_chunks(chunks)
    def fail(_):
        raise AssertionError("Exact provision lookup must not use semantic search")
    store._create_embeddings = fail
    results = store.search("What is Article 5?", [chunks[0].document_id], top_k=8)
    assert len(results) > 8
    assert {r.page_number for r in results} == {13, 14, 15, 16, 17}
    assert {r.article_number for r in results} == {"5"}
    assert "Provision: Article 5" in _build_source_context(results)
    assert store.search("Article 999?", [chunks[0].document_id]) == []
    assert store.search("Article 5?", ["other-document"]) == []
    assert store.search("Article 5?", []) == []


def test_wrong_evidence_is_rejected(chunks):
    store = store_chunks(chunks)
    wrong = store.search("Article 41?", [chunks[0].document_id])
    answer = "".join(stream_grounded_answer("Article 5?", wrong, "unused", "English + 中文"))
    assert "could not locate" in answer
    assert "未能" in answer


def test_general_questions_still_work(chunks):
    store = store_chunks(chunks)
    results = store.search("common specifications", [chunks[0].document_id], top_k=3)
    assert len(results) == 3
    assert any("Common specifications" in r.text for r in results)


def test_selected_documents_and_multiple_articles(chunks):
    second = chunk_document(document([ParsedBlock("Article 5\nAnother law\nDifferent provisions.", page_number=1)], "Other.pdf"))
    store = store_chunks(chunks + second)
    results = store.search("Compare Article 5 and Article 41", [chunks[0].document_id])
    assert {r.article_number for r in results} == {"5", "41"}
    assert all(r.document_id == chunks[0].document_id for r in results)
    assert store.search("Compare Article 5 and Article 999", [chunks[0].document_id]) == []


@pytest.mark.skipif(not os.getenv("JURISCLOUD_TEST_PDF"), reason="Optional local EU AI Act PDF")
def test_real_eu_ai_act():
    path = Path(os.environ["JURISCLOUD_TEST_PDF"])
    parsed = parse_document(path.name, path.read_bytes())
    chunks = chunk_document(parsed)
    store = store_chunks(chunks)
    results = store.search("What is Article 5 of the EU AI Act?", [chunks[0].document_id])
    assert {r.page_number for r in results} == {13, 14, 15, 16, 17}
    assert {r.article_number for r in results} == {"5"}
    assert any("Prohibited AI practices" in r.text for r in results)
    assert any("(ba)" in r.text for r in results)
    assert all("Article 6" not in r.text for r in results)
    common = store.search("Article 41", [chunks[0].document_id])
    assert {r.page_number for r in common} == {50, 51}
