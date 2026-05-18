"""LoginPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.login_controller import LoginController


class LoginPage:
    def render(self) -> None:
        st.header("Log In")

        if "user" in st.session_state:
            user = st.session_state["user"]
            st.info(f"Already signed in as {user.email} ({user.account_id}).")
            return

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")

        if not submitted:
            return

        if not self.validate_credentials(email, password):
            self.display_error()
            return

        account = LoginController().login(email.strip(), password)
        if account is None:
            self.display_error()
            return

        st.session_state["user"] = account
        st.rerun()

    @staticmethod
    def validate_credentials(email: str, password: str) -> bool:
        if not email.strip() or "@" not in email:
            return False
        if not password:
            return False
        return True

    @staticmethod
    def display_success() -> None:
        user = st.session_state.get("user")
        if user is not None:
            st.success(
                f"Logged in as {user.name} ({user.email}). "
                f"Account: {user.account_id}, profile: {user.profile_id}."
            )
        else:
            st.success("Logged in.")

    @staticmethod
    def display_error() -> None:
        st.error("Invalid email or password.")
