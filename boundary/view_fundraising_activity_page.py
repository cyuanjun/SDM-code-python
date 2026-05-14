"""ViewFundraisingActivityPage <<Boundary>> — Sprint 1 US-21.

Diagram contract (US-21.jpg):
    + displayFundraisingActivity(fundraisingActivity: FundraisingActivity): void

US-21's diagram shows the donee picking an activity by id; the page
serves both the list view (Exception A `view_all_fundraising_activities`)
and the detail view (`viewFundraisingActivity(activityId)`).
"""
from __future__ import annotations

import streamlit as st

from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)

SELECTED_KEY = "selected_fra_id"


class ViewFundraisingActivityPage:
    def render(self) -> None:
        st.header("View fundraising activity")
        controller = ViewFundraisingActivityController()

        if SELECTED_KEY in st.session_state:
            activity = controller.view_fundraising_activity(
                st.session_state[SELECTED_KEY]
            )
            if activity is None:
                st.error("Selected activity no longer exists.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_fundraising_activity(activity)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        activities = controller.view_all_fundraising_activities()
        if not activities:
            st.info("No fundraising activities yet.")
            return

        st.caption(f"{len(activities)} activities — click a row to view details")
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
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        selected = event.selection.rows
        if selected:
            st.session_state[SELECTED_KEY] = activities[selected[0]].fra_id
            st.rerun()

    @staticmethod
    def display_fundraising_activity(activity) -> None:
        st.subheader(activity.title)
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Target:** ${activity.target_amount}")
        st.write(
            f"**Runs:** {activity.start_date.isoformat()} → "
            f"{activity.end_date.isoformat()}"
        )
        if activity.completed:
            st.info("This activity is marked completed.")
        if activity.suspended:
            st.warning("This activity is currently suspended.")
        st.write(activity.description)
