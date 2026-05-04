"""SearchUserProfilePage <<Boundary>> — Sprint 3 diagram US-5."""
from __future__ import annotations

import streamlit as st

from controller.search_user_profile_controller import SearchUserProfileController


class SearchUserProfilePage:
    def render(self) -> None:
        self.display_search_page()

    def display_search_page(self) -> None:
        st.header("Search user profiles")
        with st.form("search_profile_form"):
            criteria = st.text_input("Search (role or description)")
            submitted = st.form_submit_button("Search")

        if not submitted:
            return
        if not criteria.strip():
            st.error("Enter a search term.")
            return

        results = SearchUserProfileController().submit_search_criteria(
            criteria.strip()
        )
        self.display_matching_user_profile(results)

    @staticmethod
    def display_matching_user_profile(user_profile) -> None:
        if not user_profile:
            st.info("No profiles matched your search.")
            return
        st.caption(f"{len(user_profile)} matches")
        rows = [
            {
                "ID": p.profile_id,
                "Role": p.role,
                "Description": p.description,
                "Suspended": p.suspended,
            }
            for p in user_profile
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
