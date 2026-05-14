"""LogoutPage <<Boundary>> — Sprint 1 US-12/19/27/40 (shared across actors).

Diagram contract (US-12/19/27/40.jpg):
    + logout(): void

The four logout diagrams are identical apart from the actor — no
controller, no entity, just LogoutPage.logout() as a self-call. The
self-call clears st.session_state["user"].
"""
from __future__ import annotations

import streamlit as st


class LogoutPage:
    def render(self) -> None:
        st.header("Log out")

        if "user" not in st.session_state:
            st.info("You are not signed in.")
            return

        user = st.session_state["user"]
        st.write(f"Signed in as **{user.name}** ({user.email}).")
        if st.button("Log out"):
            self.logout()

    @staticmethod
    def logout() -> None:
        st.session_state.pop("user", None)
        # Re-run so the sidebar caption flips back to "Not signed in" right
        # away instead of showing the stale signed-in summary.
        st.rerun()
