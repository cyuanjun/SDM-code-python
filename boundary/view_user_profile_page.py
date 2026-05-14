"""ViewUserProfilePage <<Boundary>> — Sprint 2 US-2.

Diagram contract (US-02.jpg):
    + displayUserProfile(profile: UserProfile): void

The page shows a list of profiles on first paint, click a row for
details — same pattern as ViewFundraisingActivityPage (US-21). The
list method uses the existing Exception A `view_all_profiles`.
"""
from __future__ import annotations

import streamlit as st

from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_profile_controller import ViewUserProfileController

SELECTED_KEY = "selected_profile_id"


class ViewUserProfilePage:
    def render(self) -> None:
        st.header("View user profile")
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

    @staticmethod
    def display_user_profile(profile) -> None:
        st.subheader(f"{profile.role}")
        st.write(f"**Profile ID:** {profile.profile_id}")
        st.write(f"**Description:** {profile.description or '(none)'}")
        st.write(f"**Suspended:** {'yes' if profile.suspended else 'no'}")
