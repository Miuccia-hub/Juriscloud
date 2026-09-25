import streamlit as st


def apply_styles() -> None:
    """Apply the Jurisource visual design."""

    st.markdown(
        """
        <style>
        :root {
            --jurisource-dark-blue: #123b70;
            --jurisource-blue: #1f66d1;
            --jurisource-light-blue: #e2f0ff;
            --jurisource-background: #ffffff;
            --jurisource-soft-background: #f7faff;
            --jurisource-border: #dce5ef;
            --jurisource-text: #10233f;
            --jurisource-muted: #66758a;
        }

        .stApp {
            background: var(--jurisource-background);
            color: var(--jurisource-text);
        }

        [data-testid="stSidebar"] {
            background: var(--jurisource-soft-background);
            border-right: 1px solid var(--jurisource-border);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.4rem;
        }

        .block-container {
            max-width: 960px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .jurisource-brand {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 1.4rem;
        }

        .jurisource-logo {
            display: flex;
            flex: 0 0 2.2rem;
            align-items: center;
            justify-content: center;
            width: 2.2rem;
            height: 2.2rem;
            border-radius: 0.7rem;
            background: var(--jurisource-dark-blue);
            color: white;
            font-size: 1rem;
        }

        .jurisource-brand-name {
            margin: 0;
            color: var(--jurisource-text);
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.2;
        }

        .jurisource-brand-description {
            margin: 0.15rem 0 0;
            color: var(--jurisource-muted);
            font-size: 0.7rem;
            line-height: 1.3;
            white-space: nowrap;
        }

        .jurisource-header {
            margin-bottom: 1rem;
        }

        .jurisource-header h1 {
            margin-bottom: 0.35rem;
            color: var(--jurisource-text);
            font-size: 2rem;
            font-weight: 600;
        }

        .jurisource-header p {
            margin: 0;
            color: var(--jurisource-muted);
        }

        .jurisource-empty {
            margin-top: 1.5rem;
            padding: 2.4rem 1.5rem;
            border: 1px solid var(--jurisource-border);
            border-radius: 1rem;
            background: var(--jurisource-soft-background);
            text-align: center;
        }

        .jurisource-empty-icon {
            margin-bottom: 0.6rem;
            font-size: 2rem;
        }

        .jurisource-empty h3 {
            margin: 0 0 0.4rem;
            color: var(--jurisource-text);
            font-size: 1.1rem;
            font-weight: 600;
        }

        .jurisource-empty p {
            margin: 0;
            color: var(--jurisource-muted);
            font-size: 0.9rem;
        }

        .jurisource-disclaimer {
            margin: 0.8rem 0 1.1rem;
            padding: 0.7rem 0.9rem;
            border-radius: 0.75rem;
            background: var(--jurisource-light-blue);
            color: var(--jurisource-dark-blue);
            font-size: 0.82rem;
        }

        .jurisource-file {
            margin-bottom: 0.45rem;
            padding: 0.65rem 0.75rem;
            border: 1px solid var(--jurisource-border);
            border-radius: 0.7rem;
            background: white;
            color: var(--jurisource-text);
            font-size: 0.82rem;
        }

        .jurisource-file-meta {
            margin-top: 0.15rem;
            color: var(--jurisource-muted);
            font-size: 0.72rem;
        }

        .stButton > button {
            border-radius: 0.7rem;
        }

        [data-testid="stFileUploader"] {
            border-radius: 0.8rem;
        }

        [data-testid="stChatInput"] {
            border-radius: 1rem;
        }

        [data-testid="stChatMessage"] {
            border-radius: 1rem;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )