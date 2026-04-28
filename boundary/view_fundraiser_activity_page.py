"""ViewFundraiserActivityPage <<Boundary>> — Sprint 2 diagram US-14.

Fundraiser views *their own* fundraising activities. The list is scoped to
activities owned by the logged-in fundraiser. Click maps to the diagram's
clickFundraisingActivity() message.
"""
from __future__ import annotations

import streamlit as st

from controller.view_fundraiser_activity_controller import (
    ViewFundraiserActivityController,
)

SELECTED_KEY = "selected_fundraiser_activity_id"


class ViewFundraiserActivityPage:
    def render(self) -> None:
        st.header("View my fundraising activity")

        if "user" not in st.session_state:
            st.warning("Log in as a fundraiser first.")
            return
        owner_account_id = st.session_state["user"].account_id
        controller = ViewFundraiserActivityController()

        if SELECTED_KEY in st.session_state:
            activity = controller.view_fundraiser_activity(
                st.session_state[SELECTED_KEY]
            )
            if activity is None or activity.owner_account_id != owner_account_id:
                st.error("Activity not found or not owned by you.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_fundraising_activity(activity)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        activities = controller.view_activities_by_owner(owner_account_id)
        if not activities:
            st.info("You haven't created any fundraising activities yet.")
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
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="df_view_fundraiser_activities",
        )
        selected = event.selection.rows
        if selected:
            self.click_fundraising_activity(str(activities[selected[0]].activity_id))
            st.rerun()

    @staticmethod
    def click_fundraising_activity(activity_id: str) -> None:
        st.session_state[SELECTED_KEY] = activity_id

    @staticmethod
    def display_fundraising_activity(activity) -> None:
        st.subheader(activity.title)
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Status:** {activity.status}")
        st.write(f"**Target:** ${activity.target_amount:,.2f}")
        st.write(f"**Runs:** {activity.start_date} → {activity.end_date}")
        st.write(activity.description)
