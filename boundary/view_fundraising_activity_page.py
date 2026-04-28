"""ViewFundraisingActivityPage <<Boundary>> — Sprint 1 diagram US-21.

Donee browses a list of fundraising activities and clicks one to view details.
Clicking maps to the diagram's selectFundraisingActivity(activityID) message.
"""
from __future__ import annotations

import streamlit as st

from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)

SELECTED_KEY = "selected_activity_id"


class ViewFundraisingActivityPage:
    def render(self) -> None:
        st.header("View fundraising activity")
        controller = ViewFundraisingActivityController()

        if SELECTED_KEY in st.session_state:
            activity = controller.view_fundraising_activity_details(
                st.session_state[SELECTED_KEY]
            )
            if activity is None:
                st.error("Selected activity no longer exists.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_fundraising_activity_details(activity)
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
                "ID": a.activity_id,
                "Title": a.title,
                "Category": a.category,
                "Status": a.status,
                "Target": a.target_amount,
                "Start": a.start_date,
                "End": a.end_date,
            }
            for a in activities
        ]
        event = st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        selected = event.selection.rows
        if selected:
            self.select_fundraising_activity(str(activities[selected[0]].activity_id))
            st.rerun()

    @staticmethod
    def select_fundraising_activity(activity_id: str) -> None:
        st.session_state[SELECTED_KEY] = activity_id

    @staticmethod
    def display_fundraising_activity_details(activity) -> None:
        st.subheader(activity.title)
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Status:** {activity.status}")
        st.write(f"**Target:** ${activity.target_amount:,.2f}")
        st.write(f"**Runs:** {activity.start_date} → {activity.end_date}")
        st.write(activity.description)
