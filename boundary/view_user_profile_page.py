"""ViewUserProfilePage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.suspend_user_profile_controller import (
    SuspendUserProfileController,
)
from controller.non_diagram.view_profiles_controller import ViewProfilesController
from controller.view_user_profile_controller import ViewUserProfileController

SELECTED_KEY = "selected_profile_id"


class ViewUserProfilePage:
    def render(self) -> None:
        st.header("View User Profile")
        controller = ViewUserProfileController()

        if SELECTED_KEY in st.session_state:
            profile = controller.view_user_profile(
                st.session_state[SELECTED_KEY]
            )
            if profile is None:
                st.error("Selected profile no longer exists.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_user_profile(profile)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        profiles = ViewProfilesController().view_all_profiles()
        if not profiles:
            st.info("No user profiles yet.")
            return

        st.caption(f"{len(profiles)} profiles — click a row to view details")
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

    def display_user_profile(self, profile) -> None:
        st.subheader(f"{profile.role}")
        st.write(f"**Profile ID:** {profile.profile_id}")
        st.write(f"**Description:** {profile.description or '(none)'}")
        st.write(f"**Suspended:** {'yes' if profile.suspended else 'no'}")

        if not profile.suspended:
            if st.button("🚫 Suspend this profile"):
                ok = SuspendUserProfileController().suspend_user_profile(
                    profile.profile_id
                )
                if ok:
                    self.display_success()
                    st.rerun()
                else:
                    self.display_error()

    @staticmethod
    def display_success() -> None:
        st.success("Profile suspended.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not suspend profile.")
