"""LogoutPage <<Boundary>> — Sprint 1 diagrams US-12/19/27/40.

Self-contained: clears the session. No Controller/Entity per the diagrams.
"""
from __future__ import annotations

import streamlit as st


class LogoutPage:
    def render(self) -> None:
        st.header("Log out")
        if st.button("Confirm log out"):
            self.logout()

    def logout(self) -> None:
        for key in ("user", "page"):
            st.session_state.pop(key, None)
        st.success("Logged out.")
        st.rerun()
