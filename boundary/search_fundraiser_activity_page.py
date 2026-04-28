"""SearchFundraiserActivityPage <<Boundary>> — Sprint 2 diagram US-20.

Donee searches fundraising activities by free-text criteria. Results are
displayed; clicking a row drills into the existing view-FSA flow.
"""
from __future__ import annotations

import streamlit as st

from controller.search_fundraiser_activity_controller import (
    SearchFundraiserActivityController,
)


class SearchFundraiserActivityPage:
    def render(self) -> None:
        self.display_search_page()

    def display_search_page(self) -> None:
        st.header("Search fundraising activities")
        with st.form("search_form"):
            search_criteria = st.text_input(
                "Search (title, description, or category)"
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not search_criteria.strip():
            st.error("Enter a search term.")
            return

        results = SearchFundraiserActivityController().submit_search_criteria(
            search_criteria.strip()
        )
        self.display_matching_fundraising_activities(results)

    @staticmethod
    def display_matching_fundraising_activities(fundraising_activities) -> None:
        if not fundraising_activities:
            st.info("No activities matched your search.")
            return

        st.caption(f"{len(fundraising_activities)} matches")
        rows = [
            {
                "ID": a.activity_id,
                "Title": a.title,
                "Category": a.category,
                "Status": a.status,
                "Target": a.target_amount,
                "Start": a.start_date,
                "End": a.end_date,
            }
            for a in fundraising_activities
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
