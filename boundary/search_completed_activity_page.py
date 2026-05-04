"""SearchCompletedActivityPage <<Boundary>> — Sprint 3 diagram US-30.

Fundraiser searches the history of *their own completed* fundraising
activities. Owner and status='completed' come from session/page context.
"""
from __future__ import annotations

import streamlit as st

from controller.search_completed_activity_controller import (
    SearchCompletedActivityController,
)


class SearchCompletedActivityPage:
    def render(self) -> None:
        if "user" not in st.session_state:
            st.warning("Log in as a fundraiser first.")
            return
        self.display_search_page()

    def display_search_page(self) -> None:
        st.header("Search my completed activities")
        with st.form("search_completed_form"):
            criteria = st.text_input(
                "Search (title, description, or category — leave blank for all)"
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        owner_account_id = st.session_state["user"].account_id
        results = SearchCompletedActivityController().submit_search_criteria(
            criteria.strip(),
            owner_account_id=owner_account_id,
            status="completed",
        )
        self.display_matching_completed_activity(results)

    @staticmethod
    def display_matching_completed_activity(activity_list) -> None:
        if not activity_list:
            st.info("No completed activities matched your search.")
            return
        st.caption(f"{len(activity_list)} matches")
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
            for a in activity_list
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
