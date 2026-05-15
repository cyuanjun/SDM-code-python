"""ViewFundraisingActivitiesPage <<Boundary>> — Sprint 2 US-20.

Diagram contract (US-20.jpg):
    + displayMatchingFundraisingActivities(FRAList: List<FundraisingActivity>): void

Diagram names the boundary class `ViewFundraisingActivities` (no `Page`
suffix); the implementation uses `ViewFundraisingActivitiesPage` to
keep the project's class-name rule. Logged in docs/todo.md as a
Sprint 2 typo.
"""
from __future__ import annotations

import streamlit as st

from controller.search_fundraising_activity_controller import (
    SearchFundraisingActivityController,
)


class ViewFundraisingActivitiesPage:
    def render(self) -> None:
        st.header("Search Fundraising Activities")

        with st.form("search_fra_form"):
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
            SearchFundraisingActivityController().search_fundraising_activity(
                criteria.strip()
            )
        )
        self.display_matching_fundraising_activities(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_fundraising_activities(activities) -> None:
        if not activities:
            st.info("No activities match.")
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
