"""ViewUserProfilesPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.search_user_profile_controller import (
    SearchUserProfileController,
)


class ViewUserProfilesPage:
    def render(self) -> None:
        st.header("Search User Profiles")

        with st.form("search_user_profile_form"):
            criteria = st.text_input(
                "Search criteria",
                placeholder="Role or description…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not self.validate_criteria(criteria):
            self.display_error()
            return

        results = SearchUserProfileController().search_user_profile(
            criteria.strip()
        )
        self.display_matching_user_profile(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_user_profile(profiles) -> None:
        if not profiles:
            st.info("No profiles match.")
            return
        st.caption(f"{len(profiles)} match")
        rows = [
            {
                "ID": p.profile_id,
                "Role": p.role,
                "Description": p.description,
                "Suspended": "yes" if p.suspended else "no",
            }
            for p in profiles
        ]
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")
