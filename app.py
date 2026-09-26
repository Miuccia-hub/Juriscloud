from __future__ import annotations

import hashlib
import html
from typing import Any
import re

import streamlit as st

from services.document_parser import DocumentParsingError, parse_document
from services.text_chunker import chunk_document
from services.vector_store import JurisourceVectorStore
from ui.styles import apply_styles
from services.answer_generator import stream_grounded_answer
from api_key import render_api_credentials_sidebar
from auth import require_app_password
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Jurisource",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not require_app_password():
    st.stop()

apply_styles()
st.markdown(
    """
    <style>
    @keyframes jurisource-cloud-breathe {
        0%, 100% {
            transform: scale(0.82);
            opacity: 0.55;
        }

        50% {
            transform: scale(1.18);
            opacity: 1;
        }
    }

    .jurisource-thinking {
        min-height: 92px;
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 18px 20px;
        color: #17365f;
        background: #f5f9ff;
        border: 1px solid #d9e7f7;
        border-radius: 18px;
    }

    .jurisource-thinking-cloud {
        display: inline-block;
        font-size: 34px;
        line-height: 1;
        transform-origin: center;
        animation: jurisource-cloud-breathe 1.45s ease-in-out infinite;
    }

    .jurisource-thinking-text {
        font-size: 15px;
        color: #60738e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def get_vector_store(api_key: str) -> JurisourceVectorStore:
    """Return a session-specific vector store for the selected API key."""

    key_fingerprint = hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()

    current_store = st.session_state.get("vector_store")
    current_fingerprint = st.session_state.get(
        "vector_store_key_fingerprint"
    )

    if (
        current_store is None
        or current_fingerprint != key_fingerprint
    ):
        st.session_state.vector_store = JurisourceVectorStore(
            api_key=api_key
        )
        st.session_state.vector_store_key_fingerprint = key_fingerprint

    return st.session_state.vector_store


def initialise_session_state() -> None:
    """Create values used by the interface."""

    defaults = {
        "messages": [],
        "research_mode": "Single Document",
        "language_mode": "English",
        "parsed_documents": {},
        "parsing_errors": {},
        "analysis_mode": "Standard",
        "vector_store": None,
        "vector_store_key_fingerprint": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def format_file_size(size_in_bytes: int) -> str:
    """Return a readable file size."""

    size_in_mb = size_in_bytes / (1024 * 1024)

    if size_in_mb >= 1:
        return f"{size_in_mb:.1f} MB"

    return f"{size_in_bytes / 1024:.0f} KB"


def make_file_key(filename: str, file_bytes: bytes) -> str:
    """Create a stable uploaded-file identifier."""

    digest = hashlib.sha256(file_bytes).hexdigest()
    return f"{filename}:{digest}"


def read_attribute(
    item: Any,
    *attribute_names: str,
    default: Any = None,
) -> Any:
    """Read the first available attribute."""

    for attribute_name in attribute_names:
        value = getattr(item, attribute_name, None)

        if value is not None:
            return value

    return default


def get_document_text(document: Any) -> str:
    """Return all text stored in a parsed document."""

    direct_text = read_attribute(
        document,
        "full_text",
        "text",
        "content",
        default="",
    )

    if direct_text:
        return str(direct_text)

    block_texts = []

    for block in read_attribute(document, "blocks", default=[]) or []:
        text = read_attribute(
            block,
            "text",
            "content",
            default="",
        )

        if text:
            block_texts.append(str(text))

    return "\n\n".join(block_texts)


def get_word_count(document: Any) -> int:
    """Return a document word count."""

    stored_count = read_attribute(
        document,
        "word_count",
        default=None,
    )

    if stored_count is not None:
        return int(stored_count)

    return len(get_document_text(document).split())


def get_page_count(document: Any) -> int | None:
    """Return a document page count when available."""

    page_count = read_attribute(
        document,
        "page_count",
        "pages",
        default=None,
    )

    if isinstance(page_count, int):
        return page_count

    if isinstance(page_count, list):
        return len(page_count)

    return None


def parse_uploaded_files(
    uploaded_files: list[Any],
) -> list[dict[str, Any]]:
    """Parse uploaded files and cache the results."""

    parsed_items = []

    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.getvalue()
        file_key = make_file_key(
            uploaded_file.name,
            file_bytes,
        )

        if (
            file_key not in st.session_state.parsed_documents
            and file_key not in st.session_state.parsing_errors
        ):
            try:
                st.session_state.parsed_documents[file_key] = (
                    parse_document(
                        uploaded_file.name,
                        file_bytes,
                    )
                )

            except DocumentParsingError as error:
                st.session_state.parsing_errors[file_key] = str(error)

            except Exception as error:
                st.session_state.parsing_errors[file_key] = (
                    f"Unexpected parsing error: {error}"
                )

        parsed_items.append(
            {
                "key": file_key,
                "name": uploaded_file.name,
                "size": uploaded_file.size,
                "document": (
                    st.session_state.parsed_documents.get(file_key)
                ),
                "error": (
                    st.session_state.parsing_errors.get(file_key)
                ),
                "indexed": False,
                "document_id": None,
                "chunk_count": 0,
            }
        )

    return parsed_items


def index_parsed_documents(
    parsed_items: list[dict[str, Any]],
    vector_store: JurisourceVectorStore,
) -> None:
    """Split and index successfully parsed documents."""

    for item in parsed_items:
        if item["document"] is None or item["error"]:
            continue

        try:
            chunks = chunk_document(item["document"])

            if not chunks:
                item["error"] = (
                    "No searchable text could be extracted."
                )
                continue

            document_id = chunks[0].document_id

            item["document_id"] = document_id
            item["chunk_count"] = len(chunks)

            if not vector_store.has_document(document_id):
                vector_store.index_chunks(chunks)

            item["indexed"] = True

        except Exception as error:
            item["error"] = f"Indexing failed: {error}"


def build_retrieval_message(results: list[Any]) -> str:
    """Format retrieved passages for temporary inspection."""

    if not results:
        return (
            "I could not find a sufficiently relevant passage in the "
            "selected documents. Try rephrasing the question."
        )

    lines = [
        "I found the following relevant passages in your selected sources:",
        "",
    ]

    for number, result in enumerate(results, start=1):
        excerpt = " ".join(result.text.split())

        if len(excerpt) > 650:
            excerpt = excerpt[:650].rstrip() + "…"

        lines.extend(
            [
                f"**[{number}] {result.citation_label}**",
                "",
                f"> {excerpt}",
                "",
            ]
        )

    lines.append(
        "_This is the retrieval-check stage. AI synthesis will be "
        "connected in the next step._"
    )

    return "\n".join(lines)

def render_source_evidence(
    sources: list[dict[str, Any]],
) -> None:
    """Show the exact retrieved passages behind an answer."""

    if not sources:
        return

    with st.expander(
        f"View cited passages ({len(sources)})"
    ):
        for source in sources:
            st.markdown(
                f"**[{source['source_id']}] "
                f"{source['citation_label']}**"
            )

            quoted_text = str(source["text"]).replace(
                "\n",
                "\n> ",
            )

            st.markdown(f"> {quoted_text}")
            st.divider()
initialise_session_state()

uploaded_files = []
parsed_items = []
vector_store = None
selected_api_key: str | None = None


with st.sidebar:
    st.markdown(
        """
        <div class="jurisource-brand">
            <div class="jurisource-logo">⚖</div>
            <div>
                <p class="jurisource-brand-name">Jurisource</p>
                <p class="jurisource-brand-description">
                    Grounded legal research
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    selected_api_key = render_api_credentials_sidebar()

    st.divider()
    st.subheader("Document library")

    uploaded_files = st.file_uploader(
        "Upload legal documents",
        type=["pdf", "txt", "docx", "doc"],
        accept_multiple_files=True,
        help="Upload up to 10 files. Maximum size: 25 MB per file.",
    )

    if uploaded_files:
        if len(uploaded_files) > 10:
            st.error("Please upload no more than 10 documents.")
            uploaded_files = uploaded_files[:10]

        oversized_names = [
            uploaded_file.name
            for uploaded_file in uploaded_files
            if uploaded_file.size > 25 * 1024 * 1024
        ]

        if oversized_names:
            st.error(
                "These files exceed 25 MB: "
                + ", ".join(oversized_names)
            )

            uploaded_files = [
                uploaded_file
                for uploaded_file in uploaded_files
                if uploaded_file.size <= 25 * 1024 * 1024
            ]

        with st.spinner("Reading your legal documents..."):
            parsed_items = parse_uploaded_files(uploaded_files)

        if selected_api_key:
            try:
                vector_store = get_vector_store(selected_api_key)

                with st.spinner("Preparing the searchable index..."):
                    index_parsed_documents(
                        parsed_items,
                        vector_store,
                    )

            except Exception as error:
                st.error(f"Vector database error: {error}")
        else:
            st.warning(
                "Choose an API access option before indexing documents."
            )

        indexed_items = [
            item
            for item in parsed_items
            if item["indexed"] and not item["error"]
        ]

        st.caption(
            f"{len(indexed_items)} of "
            f"{len(parsed_items)} document(s) indexed"
        )

        for item in parsed_items:
            safe_filename = html.escape(item["name"])
            readable_size = format_file_size(item["size"])

            if item["error"]:
                st.markdown(
                    f"""
                    <div class="jurisource-file">
                        📄 {safe_filename}
                        <div class="jurisource-file-meta">
                            {readable_size} · Processing failed
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.error(item["error"])

            else:
                document = item["document"]
                word_count = get_word_count(document)
                page_count = get_page_count(document)

                metadata_parts = [
                    readable_size,
                    f"{word_count:,} words",
                ]

                if page_count:
                    metadata_parts.append(
                        f"{page_count} "
                        f"{'page' if page_count == 1 else 'pages'}"
                    )

                metadata_parts.append(
                    f"{item['chunk_count']} passages"
                )
                metadata_parts.append("Indexed")

                st.markdown(
                    f"""
                    <div class="jurisource-file">
                        📄 {safe_filename}
                        <div class="jurisource-file-meta">
                            {" · ".join(metadata_parts)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:
        st.caption("No documents uploaded yet.")

    st.divider()

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


indexed_items = [
    item
    for item in parsed_items
    if item["indexed"] and not item["error"]
]

available_file_keys = [
    item["key"]
    for item in indexed_items
]

document_names = {
    item["key"]: item["name"]
    for item in indexed_items
}

vector_document_ids = {
    item["key"]: item["document_id"]
    for item in indexed_items
}


header_column, language_column = st.columns([4, 1])

with header_column:
    st.markdown(
        """
        <div class="jurisource-header">
            <h1>Research your legal sources</h1>
            <p>
                Ask grounded questions across legal articles, judgments,
                contracts and reports.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with language_column:
    st.selectbox(
        "Language",
        options=["English", "English + 中文"],
        key="language_mode",
    )
if "_initial_scroll_complete" not in st.session_state:
    components.html(
        """
        <script>
            function scrollToAppTop() {
                const doc = window.parent.document;

                const targets = [
                    doc.documentElement,
                    doc.body,
                    doc.querySelector('[data-testid="stAppViewContainer"]'),
                    doc.querySelector('[data-testid="stMain"]'),
                    doc.querySelector('.stMain')
                ];

                targets.forEach((element) => {
                    if (element) {
                        element.scrollTop = 0;
                        element.scrollTo?.(0, 0);
                    }
                });

                window.parent.scrollTo(0, 0);
            }

            setTimeout(scrollToAppTop, 100);
            setTimeout(scrollToAppTop, 350);
            setTimeout(scrollToAppTop, 800);
        </script>
        """,
        height=0,
    )

    st.session_state["_initial_scroll_complete"] = True

st.radio(
    "Research mode",
    options=["Single Document", "Multi-source Research"],
    horizontal=True,
    key="research_mode",
)
analysis_mode = st.selectbox(
    "Answer depth",
    options=["Standard", "Deep Analysis"],
    key="analysis_mode",
    help=(
        "Standard uses GPT-4o. Deep Analysis uses GPT-5 Pro "
        "and may take several minutes and cost substantially more."
    ),
)

selected_file_keys: list[str] = []

if available_file_keys:
    if st.session_state.research_mode == "Single Document":
        current_key = st.session_state.get(
            "single_document_key"
        )

        if current_key not in available_file_keys:
            st.session_state.single_document_key = (
                available_file_keys[0]
            )

        selected_key = st.selectbox(
            "Document to research",
            options=available_file_keys,
            format_func=lambda key: document_names[key],
            key="single_document_key",
        )

        selected_file_keys = [selected_key]

    else:
        if "multi_document_keys" not in st.session_state:
            st.session_state.multi_document_keys = (
                available_file_keys.copy()
            )
        else:
            valid_keys = [
                key
                for key in st.session_state.multi_document_keys
                if key in available_file_keys
            ]

            st.session_state.multi_document_keys = (
                valid_keys or available_file_keys.copy()
            )

        selected_file_keys = st.multiselect(
            "Documents to research",
            options=available_file_keys,
            format_func=lambda key: document_names[key],
            key="multi_document_keys",
        )


selected_document_ids = [
    vector_document_ids[file_key]
    for file_key in selected_file_keys
    if vector_document_ids.get(file_key)
]


st.markdown(
    """
    <div class="jurisource-disclaimer">
        🛡️ For research assistance only — not legal advice.
        Answers will be grounded in the documents you select.
    </div>
    """,
    unsafe_allow_html=True,
)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            render_source_evidence(
                message.get("sources", [])
            )


if not st.session_state.messages:
    if indexed_items:
        st.markdown(
            f"""
            <div class="jurisource-empty">
                <div class="jurisource-empty-icon">✅</div>
                <h3>Your legal sources are searchable</h3>
                <p>
                    {len(selected_document_ids)} document(s) selected.
                    Ask a question to test source retrieval.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif uploaded_files:
        st.markdown(
            """
            <div class="jurisource-empty">
                <div class="jurisource-empty-icon">⚠️</div>
                <h3>The documents could not be indexed</h3>
                <p>
                    Review the messages in the document library.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        st.markdown(
            """
            <div class="jurisource-empty">
                <div class="jurisource-empty-icon">📚</div>
                <h3>Begin with your legal sources</h3>
                <p>
                    Upload one or more PDF, TXT, DOCX or DOC files
                    from the document library.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


user_question = st.chat_input(
    "Ask a question about your selected sources…",
    disabled=(
        not selected_document_ids
        or vector_store is None
    ),
)

if user_question and vector_store is not None:
    earlier_history = st.session_state.messages.copy()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()
        answer_placeholder = st.empty()

        thinking_placeholder.markdown(
            """
            <div class="jurisource-thinking">
                <span class="jurisource-thinking-cloud">💭</span>
                <span class="jurisource-thinking-text">
                    Reviewing your legal sources…
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        complete_answer = ""
        first_text_received = False
        verified_sources: list[dict[str, Any]] = []

        try:
            search_results = vector_store.search(
                question=user_question,
                document_ids=selected_document_ids,
                top_k=8,
            )

            answer_stream = stream_grounded_answer(
                question=user_question,
                search_results=search_results,
                api_key=selected_api_key,
                language_mode=st.session_state.language_mode,
                analysis_mode=st.session_state.analysis_mode,
                conversation_history=earlier_history,
            )

            for text_delta in answer_stream:
                if not first_text_received:
                    thinking_placeholder.empty()
                    first_text_received = True

                complete_answer += text_delta

                answer_placeholder.markdown(
                    complete_answer + " ▌"
                )

            thinking_placeholder.empty()

            cited_source_numbers = sorted(
                {
                    int(source_number)
                    for source_number in re.findall(
                        r"\[S(\d+)\]",
                        complete_answer,
                    )
                    if 1 <= int(source_number) <= len(search_results)
                }
            )

            if cited_source_numbers:
                source_lines = [
                    "",
                    "",
                    "---",
                    "**Sources**",
                ]

                for source_number in cited_source_numbers:
                    result = search_results[source_number - 1]

                    source_lines.append(
                        f"- [S{source_number}] "
                        f"{result.citation_label}"
                    )

                    verified_sources.append(
                        {
                            "source_id": f"S{source_number}",
                            "citation_label": (
                                result.citation_label
                            ),
                            "text": result.text,
                            "filename": result.filename,
                            "page_number": result.page_number,
                        }
                    )

                complete_answer += "\n".join(source_lines)

            answer_placeholder.markdown(complete_answer)
            render_source_evidence(verified_sources)

        except Exception as error:
            thinking_placeholder.empty()

            complete_answer = (
                "Jurisource could not generate an answer. "
                f"Technical detail: {error}"
            )

            answer_placeholder.error(complete_answer)

        st.session_state.messages.append(
        {
            "role": "assistant",
            "content": complete_answer,
            "sources": verified_sources,
        }
    )
       