"""UpdateUserProfilePage <<Boundary>> — Sprint 2 US-3.

Diagram contract (US-03.jpg):
    + displaySuccess(): void

Admin picks a profile from the list (Exception A view_all_profiles),
edits its fields, submits. Entity returns Boolean; boundary calls
displaySuccess on True, displayError on False.
"""
from __future__ import annotations

import streamlit as st

from controller.update_user_profile_controller import (
    UpdateUserProfileController,
)
from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_profile_controller import ViewUserProfileController
from entity.user_profile import UserProfile

SELECTED_KEY = "update_profile_selected_id"


class UpdateUserProfilePage:
    def render(self) -> None:
        st.header("Update user profile")

        if SELECTED_KEY not in st.session_state:
            self._render_picker()
            return

        current = ViewUserProfileController().view_user_profile(
            st.session_state[SELECTED_KEY]
        )
        if current is None:
            st.error("Selected profile no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        with st.form("update_profile_form"):
            st.write(f"**Editing:** {current.profile_id}")
            role = st.text_input("Role", value=current.role)
            description = st.text_area("Description", value=current.description)
            suspended = st.checkbox("Suspended", value=current.suspended)
            col_a, col_b = st.columns(2)
            with col_a:
                submitted = st.form_submit_button("Save changes")
            with col_b:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state.pop(SELECTED_KEY, None)
            st.rerun()
            return

        if not submitted:
            return

        if not self.validate_profile(role, description):
            self.display_error()
            return

        ok = UpdateUserProfileController().update_user_profile(
            st.session_state[SELECTED_KEY],
            UserProfile(
                role=role.strip(),
                description=description.strip(),
                suspended=suspended,
            ),
        )
        if ok:
            self.display_success()
            st.session_state.pop(SELECTED_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def _render_picker() -> None:
        profiles = ViewProfilesController().view_all_profiles()
        if not profiles:
            st.info("No user profiles yet — create one first.")
            return

        st.caption("Pick a profile to update.")
        rows = [
            {
                "ID": p.profile_id,
                "Role": p.role,
                "Description": p.description,
                "Suspended": "yes" if p.suspended else "no",
            }
            for p in profiles
        ]
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        selected = event.selection.rows
        if selected:
            st.session_state[SELECTED_KEY] = profiles[selected[0]].profile_id
            st.rerun()

    @staticmethod
    def validate_profile(role: str, description: str) -> bool:
        return bool(role.strip()) and bool(description.strip())

    @staticmethod
    def display_success() -> None:
        st.success("Profile updated.")

    @staticmethod
    def display_error() -> None:
        st.error("Update failed. Role and description are both required.")
