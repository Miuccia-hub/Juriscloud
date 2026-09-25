import streamlit as st

from ui.styles import apply_styles


st.set_page_config(
    page_title="Jurisource",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_styles()


def initialise_session_state() -> None:
    """Create the session values used by the interface."""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "research_mode" not in st.session_state:
        st.session_state.research_mode = "Single Document"

    if "language_mode" not in st.session_state:
        st.session_state.language_mode = "English"


def format_file_size(size_in_bytes: int) -> str:
    """Return a readable file size."""

    size_in_mb = size_in_bytes / (1024 * 1024)

    if size_in_mb >= 1:
        return f"{size_in_mb:.1f} MB"

    size_in_kb = size_in_bytes / 1024
    return f"{size_in_kb:.0f} KB"


initialise_session_state()


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

    st.subheader("Document library")

    uploaded_files = st.file_uploader(
        "Upload legal documents",
        type=["pdf", "txt", "docx", "doc"],
        accept_multiple_files=True,
        help="Upload up to 10 files. Maximum size: 25 MB per file.",
    )

    if uploaded_files:
        st.caption(f"{len(uploaded_files)} document(s) selected")

        for uploaded_file in uploaded_files:
            st.markdown(
                f"""
                <div class="jurisource-file">
                    📄 {uploaded_file.name}
                    <div class="jurisource-file-meta">
                        {format_file_size(uploaded_file.size)} · Ready to process
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
    language_mode = st.selectbox(
        "Language",
        options=["English", "English + 中文"],
        key="language_mode",
    )


research_mode = st.radio(
    "Research mode",
    options=["Single Document", "Multi-source Research"],
    horizontal=True,
    key="research_mode",
)

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


if not st.session_state.messages:
    if uploaded_files:
        st.markdown(
            """
            <div class="jurisource-empty">
                <div class="jurisource-empty-icon">💬</div>
                <h3>Your documents are ready for the next step</h3>
                <p>
                    Document parsing and grounded answers will be connected
                    in the next development stage.
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
    disabled=not uploaded_files,
)

if user_question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": (
                "The interface is working. Document processing and "
                "AI-generated answers will be connected next."
            ),
        }
    )

    st.rerun()