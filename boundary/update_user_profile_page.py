"""UpdateUserProfilePage <<Boundary>> — Sprint 2 diagram US-3."""
from __future__ import annotations

import streamlit as st

from controller.update_user_profile_controller import UpdateUserProfileController
from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_profile_controller import ViewUserProfileController
from entity.user_profile import UserProfile

EDIT_KEY = "editing_profile_id"


class UpdateUserProfilePage:
    def render(self) -> None:
        st.header("Update user profile")

        profiles = ViewProfilesController().view_all_profiles()
        if not profiles:
            st.info("No profiles to update.")
            return

        if EDIT_KEY not in st.session_state:
            st.caption("Select a profile to edit:")
            labels = {self._label(p): p.profile_id for p in profiles}
            choice = st.selectbox("Profile", list(labels.keys()))
            if st.button("Edit", key="click_edit_option"):
                self.click_edit_option(str(labels[choice]))
                st.rerun()
            return

        self.display_update_page()

    def display_update_page(self) -> None:
        profile_id = st.session_state[EDIT_KEY]
        current = ViewUserProfileController().view_user_profile(profile_id)
        if current is None:
            st.error("Profile not found.")
            st.session_state.pop(EDIT_KEY, None)
            return

        with st.form("update_profile_form"):
            role = st.text_input("Role", value=current.role)
            description = st.text_area("Description", value=current.description or "")
            suspended = st.checkbox("Suspended", value=current.suspended)
            cols = st.columns(2)
            submitted = cols[0].form_submit_button("Save changes", type="primary")
            cancelled = cols[1].form_submit_button("Cancel")

        if cancelled:
            st.session_state.pop(EDIT_KEY, None)
            st.rerun()
            return

        if not submitted:
            return

        if not self._validate(role, description):
            return

        updated = UserProfile(
            role=role.strip(),
            description=description.strip(),
            profile_id=int(profile_id),
            suspended=suspended,
        )
        success = UpdateUserProfileController().update_user_profile(profile_id, updated)
        if success:
            self.display_success()
            st.session_state.pop(EDIT_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def click_edit_option(profile_id: str) -> None:
        st.session_state[EDIT_KEY] = profile_id

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
    def _label(profile) -> str:
        desc_preview = (profile.description or "")[:50]
        return f"#{profile.profile_id} — {profile.role}: {desc_preview}"

    @staticmethod
    def display_success() -> None:
        st.success("Profile updated.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not update profile.")
