"""ViewFundraisingActivityCategoriesPage <<Boundary>> — Sprint 4 US-37."""
from __future__ import annotations

import streamlit as st

from controller.search_fundraising_activity_category_controller import (
    SearchFundraisingActivityCategoryController,
)


class ViewFundraisingActivityCategoriesPage:
    def render(self) -> None:
        st.header("Search fundraising activity categories")

        with st.form("search_fra_cat_form"):
            criteria = st.text_input(
                "Search criteria",
                placeholder="Name or description…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not self.validate_criteria(criteria):
            self.display_error()
            return

        results = (
            SearchFundraisingActivityCategoryController()
            .search_fundraising_activity_category(criteria.strip())
        )
        self.display_matching_fra_category(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_fra_category(categories) -> None:
        if not categories:
            st.info("No categories match.")
            return
        st.caption(f"{len(categories)} match")
        rows = [
            {
                "ID": c.fra_cat_id,
                "Name": c.category_name,
                "Description": c.description,
                "Suspended": "yes" if c.suspended else "no",
            }
            for c in categories
        ]
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")
