from __future__ import annotations

import hmac

import streamlit as st


def require_app_password() -> bool:
    """Require the shared application password."""

    if st.session_state.get("app_authenticated", False):
        return True

    try:
        expected_password = str(
            st.secrets["APP_PASSWORD"]
        )
    except KeyError:
        st.error(
            "APP_PASSWORD has not been configured."
        )
        return False

    st.title("Jurisource")
    st.caption(
        "Enter the application password to continue."
    )

    with st.form("jurisource_login"):
        entered_password = st.text_input(
            "Application password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Continue",
            use_container_width=True,
        )

    if submitted:
        password_matches = hmac.compare_digest(
            entered_password,
            expected_password,
        )

        if password_matches:
            st.session_state.app_authenticated = True
            st.rerun()

        st.error("Incorrect application password.")

    return False
