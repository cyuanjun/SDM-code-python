"""SearchFundraisingActivityCategoryPage <<Boundary>> — Sprint 4 diagram US-37."""
from __future__ import annotations

import streamlit as st

from controller.search_fundraising_activity_category_controller import (
    SearchFundraisingActivityCategoryController,
)


class SearchFundraisingActivityCategoryPage:
    def render(self) -> None:
        self.display_search_fra_category_page()

    def display_search_fra_category_page(self) -> None:
        st.header("Search fundraising activity categories")
        with st.form("search_category_form"):
            criteria = st.text_input("Search (name or description)")
            submitted = st.form_submit_button("Search")

        if not submitted:
            return
        if not criteria.strip():
            st.error("Enter a search term.")
            return

        results = SearchFundraisingActivityCategoryController().submit_search_criteria(
            criteria.strip()
        )
        self.display_matching_fra_category(results)

    @staticmethod
    def display_matching_fra_category(fra_category_list) -> None:
        if not fra_category_list:
            st.info("No categories matched your search.")
            return
        st.caption(f"{len(fra_category_list)} matches")
        rows = [
            {
                "ID": c.category_id,
                "Name": c.category_name,
                "Description": c.description,
                "Status": c.status,
            }
            for c in fra_category_list
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
