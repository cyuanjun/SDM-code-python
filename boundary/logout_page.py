"""LogoutPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st


class LogoutPage:
    def render(self) -> None:
        st.header("Log Out")

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
        st.rerun()
