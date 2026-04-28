"""CreateProfilePage <<Boundary>> — Sprint 1 diagram US-1."""
from __future__ import annotations

import streamlit as st

from controller.create_profile_controller import CreateProfileController


class CreateProfilePage:
    def render(self) -> None:
        st.header("Create user profile")
        with st.form("create_profile_form"):
            role = st.text_input("Role")
            description = st.text_area("Description")
            submitted = st.form_submit_button("Create profile")

        if not submitted:
            return

        if not self._validate(role, description):
            return

        profile = CreateProfileController().create_profile(role, description)
        if profile is not None:
            self.display_success()
        else:
            self.display_error()

    @staticmethod
    def _validate(role: str, description: str) -> bool:
        if not role.strip():
            st.error("Role is required.")
            return False
        if not description.strip():
            st.error("Description is required.")
            return False
        return True

    @staticmethod
    def display_success() -> None:
        st.success("Profile created.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not create profile.")
