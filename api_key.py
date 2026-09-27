from __future__ import annotations

import streamlit as st


JURISOURCE_API_OPTION = "Use Juriscloud API access"
PERSONAL_API_OPTION = "Use my own OpenAI API key"


def _save_personal_api_key() -> None:
    """Save the user's API key in the current session."""

    entered_key = st.session_state.get(
        "personal_api_key_input",
        "",
    ).strip()

    if entered_key:
        st.session_state.personal_openai_api_key = entered_key
        st.session_state.personal_api_key_input = ""
        st.session_state.api_key_message = "saved"
    else:
        st.session_state.api_key_message = "missing"


def _remove_personal_api_key() -> None:
    """Remove the user's API key from the current session."""

    st.session_state.personal_openai_api_key = None
    st.session_state.personal_api_key_input = ""
    st.session_state.api_key_message = "removed"


def render_api_credentials_sidebar() -> str | None:
    """
    Let the user choose between the application's API key
    and their own OpenAI API key.

    Adapted from:
    https://github.com/mls-laws90286-2026/openai_credentials
    """

    if "personal_openai_api_key" not in st.session_state:
        st.session_state.personal_openai_api_key = None

    if "api_key_message" not in st.session_state:
        st.session_state.api_key_message = None

    st.sidebar.subheader("OpenAI API credentials")

    api_option = st.sidebar.radio(
        "Choose how to access OpenAI",
        options=[
            JURISOURCE_API_OPTION,
            PERSONAL_API_OPTION,
        ],
        key="api_key_option",
    )

    if api_option == JURISOURCE_API_OPTION:
        try:
            application_api_key = str(
                st.secrets["OPENAI_API_KEY"]
            ).strip()
        except KeyError:
            st.sidebar.error(
                "The Juriscloud API key has not been configured."
            )
            return None

        if not application_api_key:
            st.sidebar.error(
                "The Juriscloud API key is empty."
            )
            return None

        st.sidebar.success(
            "Using API access provided by Juriscloud."
        )
        st.sidebar.caption(
            "API usage will be charged to the application owner."
        )

        return application_api_key

    st.sidebar.text_input(
        "Enter your OpenAI API key",
        type="password",
        key="personal_api_key_input",
        placeholder="sk-...",
        help=(
            "The key is kept only in your current browser session "
            "and is not written to the repository."
        ),
    )

    save_column, remove_column = st.sidebar.columns(2)

    save_column.button(
        "Use key",
        on_click=_save_personal_api_key,
        use_container_width=True,
    )

    remove_column.button(
        "Remove",
        on_click=_remove_personal_api_key,
        use_container_width=True,
        disabled=not bool(
            st.session_state.personal_openai_api_key
        ),
    )

    personal_api_key = (
        st.session_state.personal_openai_api_key
    )

    if personal_api_key:
        st.sidebar.success(
            "Your personal API key is active."
        )
        st.sidebar.caption(
            "API usage will be charged to your OpenAI account."
        )

    elif st.session_state.api_key_message == "missing":
        st.sidebar.warning(
            "Please enter an OpenAI API key."
        )

    else:
        st.sidebar.info(
            "Enter your own API key to continue."
        )

    return personal_api_key