"""CreateProfilePage <<Boundary>> — Sprint 1 US-1.

Diagram contract (US-01.jpg):
    + displaySuccess(profile: UserProfile): void

Validation lives here per the project rule. `displayError` is not on the
diagram but is required by the validation rule (logged in docs/todo.md).
"""
from __future__ import annotations

import streamlit as st

from controller.create_profile_controller import CreateProfileController


class CreateProfilePage:
    def render(self) -> None:
        st.header("Create User Profile")
        with st.form("create_profile_form"):
            role = st.text_input("Role")
            description = st.text_area("Description")
            submitted = st.form_submit_button("Create profile")

        if not submitted:
            return

        if not self.validate_profile(role, description):
            self.display_error()
            return

        profile = CreateProfileController().create_profile(
            role=role.strip(), description=description.strip()
        )
        self.display_success(profile)

    @staticmethod
    def validate_profile(role: str, description: str) -> bool:
        return bool(role.strip()) and bool(description.strip())

    @staticmethod
    def display_success(profile) -> None:
        st.success(
            f"Profile created: {profile.profile_id} ({profile.role})"
        )

    @staticmethod
    def display_error() -> None:
        st.error("Role and description are both required.")
