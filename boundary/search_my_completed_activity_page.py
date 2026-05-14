"""SearchMyCompletedActivityPage <<Boundary>> — Sprint 3 US-30.

Diagram contract (US-30.jpg):
    + displayMatchingCompletedActivity(myCompletedFRAList: List<FundraisingActivity>): void

Class diagram names the boundary `ViewMyFundraisingActivitiesPage`
(same as US-17). Implementation uses `SearchMyCompletedActivityPage`
to keep US-30 distinct from US-17 in the sidebar. Logged in docs/todo.md.
"""
from __future__ import annotations

import streamlit as st

from controller.search_my_completed_fundraising_activity_controller import (
    SearchMyCompletedFundraisingActivityController,
)


class SearchMyCompletedActivityPage:
    def render(self) -> None:
        st.header("Search my completed activities")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id

        with st.form("search_my_completed_fra_form"):
            criteria = st.text_input(
                "Search criteria",
                placeholder="Title, description, or category…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not self.validate_criteria(criteria):
            self.display_error()
            return

        results = (
            SearchMyCompletedFundraisingActivityController()
            .search_my_completed_fra(
                owner_account_id=owner_account_id,
                search_criteria=criteria.strip(),
            )
        )
        self.display_matching_completed_activity(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_completed_activity(activities) -> None:
        if not activities:
            st.info("No completed activities of yours match.")
            return
        st.caption(f"{len(activities)} match")
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": a.category,
                "Target": f"${a.target_amount}",
                "Start": a.start_date.isoformat(),
                "End": a.end_date.isoformat(),
            }
            for a in activities
        ]
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")
