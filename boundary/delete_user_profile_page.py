"""DeleteUserProfilePage <<Boundary>> — Sprint 3 diagram US-4."""
from __future__ import annotations

import streamlit as st

from controller.delete_user_profile_controller import DeleteUserProfileController
from controller.view_profiles_controller import ViewProfilesController


class DeleteUserProfilePage:
    def render(self) -> None:
        st.header("Delete user profile")

        profiles = ViewProfilesController().view_all_profiles()
        if not profiles:
            st.info("No profiles to delete.")
            return

        labels = {self._label(p): p.profile_id for p in profiles}
        choice = st.selectbox("Profile", list(labels.keys()))

        if st.button("Delete", type="primary"):
            self.click_delete_button(str(labels[choice]))

    @staticmethod
    def click_delete_button(profile_id: str) -> None:
        success = DeleteUserProfileController().delete_user_profile(profile_id)
        if success:
            DeleteUserProfilePage.display_success()
        else:
            DeleteUserProfilePage.display_error()

    @staticmethod
    def _label(profile) -> str:
        desc = (profile.description or "")[:50]
        return f"#{profile.profile_id} — {profile.role}: {desc}"

    @staticmethod
    def display_success() -> None:
        st.success("Profile deleted.")

    @staticmethod
    def display_error() -> None:
        st.error(
            "Could not delete profile — it may be in use by an existing account."
        )
