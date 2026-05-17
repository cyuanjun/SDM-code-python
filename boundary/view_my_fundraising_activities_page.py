"""ViewMyFundraisingActivitiesPage <<Boundary>> — Sprint 3 US-17, US-30, US-31.

Diagram contracts (2026-05-18 set):
    US-17: + displayMatchingMyFundraisingActivity(myFRAList: List<FundraisingActivity>): void
    US-30: + displayMatchingMyCompletedFundraisingActivity(myCompletedFRAList: List<FundraisingActivity>): void
    US-31: + displayMyCompletedFundraisingActivities(myCompletedFRAList: List<FundraisingActivity>): void

Per the sketch design (2026-05-17): one page with a search bar plus an
[All] / [Completed] tab toggle. US-17 fires when [All] is selected with
a search term; US-30 fires when [Completed] is selected with a search
term; US-31 fires when [Completed] is selected with no search term.
"""
from __future__ import annotations

import streamlit as st

from controller.search_my_completed_fundraising_activity_controller import (
    SearchMyCompletedFundraisingActivityController,
)
from controller.search_my_fundraising_activity_controller import (
    SearchMyFundraisingActivityController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)
from controller.view_my_completed_fundraising_activities_controller import (
    ViewMyCompletedFundraisingActivitiesController,
)


def _category_lookup() -> dict[str, str]:
    """fra_cat_id -> category_name, for rendering readable category cells."""
    cats = ViewFundraisingActivityCategoryController().view_all_categories()
    return {c.fra_cat_id: c.category_name for c in cats}


class ViewMyFundraisingActivitiesPage:
    def render(self) -> None:
        st.header("My Fundraising Activities")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id

        tab_all, tab_completed = st.tabs(["All", "Completed"])

        with tab_all:
            self._render_all_tab(owner_account_id)
        with tab_completed:
            self._render_completed_tab(owner_account_id)

    def _render_all_tab(self, owner_account_id: str) -> None:
        with st.form("search_my_fra_all_form"):
            criteria = st.text_input(
                "Search my activities (leave blank to skip search)",
                placeholder="Title, description, or category…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted or not criteria.strip():
            return

        results = (
            SearchMyFundraisingActivityController()
            .search_my_fundraising_activity(
                owner_account_id=owner_account_id,
                search_criteria=criteria.strip(),
            )
        )
        self.display_matching_my_fundraising_activity(results)

    def _render_completed_tab(self, owner_account_id: str) -> None:
        with st.form("search_my_completed_fra_form"):
            criteria = st.text_input(
                "Search my completed activities (leave blank to list all)",
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
    def display_matching_my_fundraising_activity(activities) -> None:
        if not activities:
            st.info("No activities of yours match.")
            return
        st.caption(f"{len(activities)} match")
        ViewMyFundraisingActivitiesPage._render_table(activities, include_status=True)

    @staticmethod
    def display_matching_my_completed_fundraising_activity(activities) -> None:
        if not activities:
            st.info("No completed activities of yours match.")
            return
        st.caption(f"{len(activities)} match")
        ViewMyFundraisingActivitiesPage._render_table(activities, include_status=False)

    @staticmethod
    def display_my_completed_fundraising_activities(activities) -> None:
        if not activities:
            st.info("You have no completed activities yet.")
            return
        st.caption(f"{len(activities)} of your completed activities")
        ViewMyFundraisingActivitiesPage._render_table(activities, include_status=False)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")

    @staticmethod
    def _render_table(activities, include_status: bool) -> None:
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": _category_lookup().get(a.fra_cat_id, a.fra_cat_id),
                "Target": f"${a.target_amount}",
                "Start": a.start_date.isoformat(),
                "End": a.end_date.isoformat(),
                **(
                    {
                        "Completed": "yes" if a.completed else "no",
                        "Suspended": "yes" if a.suspended else "no",
                    }
                    if include_status
                    else {}
                ),
            }
            for a in activities
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
