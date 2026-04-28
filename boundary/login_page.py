"""LoginPage <<Boundary>> — Sprint 1 diagrams US-11/18/26/39.

All input/format validation happens here. The Entity result (None vs UserAccount)
drives display_success() / display_error().
"""
from __future__ import annotations

import streamlit as st

from controller.login_controller import LoginController


class LoginPage:
    def render(self) -> None:
        st.header("Log in")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")

        if not submitted:
            return

        if not self._validate(email, password):
            return

        user = LoginController().login(email, password)
        if user is not None:
            st.session_state["user"] = user
            self.display_success()
        else:
            self.display_error()

    @staticmethod
    def _validate(email: str, password: str) -> bool:
        if not email or not password:
            st.error("Email and password are required.")
            return False
        if "@" not in email:
            st.error("Email must contain '@'.")
            return False
        return True

    @staticmethod
    def display_success() -> None:
        st.success("Logged in.")

    @staticmethod
    def display_error() -> None:
        st.error("Invalid email or password.")
