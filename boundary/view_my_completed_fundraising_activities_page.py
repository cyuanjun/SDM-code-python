"""ViewMyCompletedFundraisingActivitiesPage <<Boundary>> — Sprint 3 US-30 + US-31.

Diagram contracts:
    US-30: + displayMatchingMyCompletedFundraisingActivity(myCompletedFRAList: List<FundraisingActivity>): void
    US-31: + displayMyCompletedFundraisingActivities(myCompletedFRAList: List<FundraisingActivity>): void

Both USes name the same Boundary class on their diagrams. The page renders
US-31's full list by default; supplying search criteria switches to US-30's
filtered results.
"""
from __future__ import annotations

import streamlit as st

from controller.search_my_completed_fundraising_activity_controller import (
    SearchMyCompletedFundraisingActivityController,
)
from controller.view_my_completed_fundraising_activities_controller import (
    ViewMyCompletedFundraisingActivitiesController,
)


class ViewMyCompletedFundraisingActivitiesPage:
    def render(self) -> None:
        st.header("My Completed Fundraising Activities")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id

        with st.form("my_completed_fra_form"):
            criteria = st.text_input(
                "Search criteria (leave blank to list all)",
                placeholder="Title, description, or category…",
            )
            submitted = st.form_submit_button("Show")

        if not submitted:
            activities = (
                ViewMyCompletedFundraisingActivitiesController()
                .view_my_completed_fundraising_activities(
                    owner_account_id=owner_account_id,
                )
            )
            self.display_my_completed_fundraising_activities(activities)
            return

        if criteria.strip():
            results = (
                SearchMyCompletedFundraisingActivityController()
                .search_my_completed_fundraising_activity(
                    owner_account_id=owner_account_id,
                    search_criteria=criteria.strip(),
                )
            )
            self.display_matching_my_completed_fundraising_activity(results)
        else:
            activities = (
                ViewMyCompletedFundraisingActivitiesController()
                .view_my_completed_fundraising_activities(
                    owner_account_id=owner_account_id,
                )
            )
            self.display_my_completed_fundraising_activities(activities)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_my_completed_fundraising_activity(activities) -> None:
        if not activities:
            st.info("No completed activities of yours match.")
            return
        st.caption(f"{len(activities)} match")
        ViewMyCompletedFundraisingActivitiesPage._render_table(activities)

    @staticmethod
    def display_my_completed_fundraising_activities(activities) -> None:
        if not activities:
            st.info("You have no completed activities yet.")
            return
        st.caption(f"{len(activities)} of your completed activities")
        ViewMyCompletedFundraisingActivitiesPage._render_table(activities)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")

    @staticmethod
    def _render_table(activities) -> None:
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
