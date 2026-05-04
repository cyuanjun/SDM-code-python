"""ViewCompletedActivityPage <<Boundary>> — Sprint 3 diagram US-31.

Fundraiser reviews the details of one of their completed activities. Lists
the fundraiser's completed activities and drills into details on click.
"""
from __future__ import annotations

import streamlit as st

from controller.search_completed_activity_controller import (
    SearchCompletedActivityController,
)
from controller.view_completed_activity_controller import (
    ViewCompletedActivityController,
)

SELECTED_KEY = "selected_completed_activity_id"


class ViewCompletedActivityPage:
    def render(self) -> None:
        st.header("View my completed activities")

        if "user" not in st.session_state:
            st.warning("Log in as a fundraiser first.")
            return
        owner_account_id = st.session_state["user"].account_id

        if SELECTED_KEY in st.session_state:
            activity = ViewCompletedActivityController().view_completed_activity(
                st.session_state[SELECTED_KEY]
            )
            if activity is None or activity.owner_account_id != owner_account_id:
                st.error("Activity not found, not completed, or not owned by you.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_completed_activity(activity)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        completed = SearchCompletedActivityController().submit_search_criteria(
            "", owner_account_id=owner_account_id, status="completed"
        )
        if not completed:
            st.info("You have no completed fundraising activities yet.")
            return

        st.caption(f"{len(completed)} completed activities — click a row to view")
        rows = [
            {
                "ID": a.activity_id,
                "Title": a.title,
                "Category": a.category,
                "Target": a.target_amount,
                "Start": a.start_date,
                "End": a.end_date,
            }
            for a in completed
        ]
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="df_view_completed_activities",
        )
        selected = event.selection.rows
        if selected:
            self.click_completed_activity(str(completed[selected[0]].activity_id))
            st.rerun()

    @staticmethod
    def click_completed_activity(activity_id: str) -> None:
        st.session_state[SELECTED_KEY] = activity_id

    @staticmethod
    def display_completed_activity(activity) -> None:
        st.subheader(activity.title)
        st.write(f"**Activity ID:** {activity.activity_id}")
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Status:** {activity.status}")
        st.write(f"**Target:** ${activity.target_amount:,.2f}")
        st.write(f"**Runs:** {activity.start_date} → {activity.end_date}")
        st.write(activity.description)
