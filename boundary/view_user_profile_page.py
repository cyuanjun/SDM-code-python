"""ViewUserProfilePage <<Boundary>> — Sprint 2 diagram US-2.

Admin browses profiles and clicks one to view details. Click maps to the
diagram's clickUserProfile() message.
"""
from __future__ import annotations

import streamlit as st

from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_profile_controller import ViewUserProfileController

SELECTED_KEY = "selected_profile_id"


class ViewUserProfilePage:
    def render(self) -> None:
        st.header("View user profile")

        if SELECTED_KEY in st.session_state:
            profile = ViewUserProfileController().view_user_profile(
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
            st.info("No profiles yet.")
            return

        st.caption(f"{len(profiles)} profiles — click a row to view details")
        rows = [
            {"ID": p.profile_id, "Role": p.role, "Description": p.description}
            for p in profiles
        ]
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="df_view_profiles",
        )
        selected = event.selection.rows
        if selected:
            self.click_user_profile(str(profiles[selected[0]].profile_id))
            st.rerun()

    @staticmethod
    def click_user_profile(profile_id: str) -> None:
        st.session_state[SELECTED_KEY] = profile_id

    @staticmethod
    def display_user_profile(profile) -> None:
        st.subheader(f"Profile #{profile.profile_id}")
        st.write(f"**Role:** {profile.role}")
        st.write(f"**Description:** {profile.description}")
        st.write(f"**Suspended:** {'yes' if profile.suspended else 'no'}")
