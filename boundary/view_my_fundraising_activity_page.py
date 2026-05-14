"""ViewMyFundraisingActivityPage <<Boundary>> — Sprint 2 US-14.

Diagram contract (US-14.jpg):
    + displayMyFundraisingActivity(fundraisingActivity: FundraisingActivity): void

Fundraiser-scoped. Requires login. List of own activities → click → detail.
"""
from __future__ import annotations

import streamlit as st

from controller.view_my_fundraising_activity_controller import (
    ViewMyFundraisingActivityController,
)

SELECTED_KEY = "view_my_fra_selected_id"


class ViewMyFundraisingActivityPage:
    def render(self) -> None:
        st.header("View my fundraising activity")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id
        controller = ViewMyFundraisingActivityController()

        if SELECTED_KEY in st.session_state:
            activity = controller.view_my_fundraising_activity(
                owner_account_id=owner_account_id,
                fra_id=st.session_state[SELECTED_KEY],
            )
            if activity is None:
                st.error(
                    "Selected activity no longer exists or is not yours."
                )
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_my_fundraising_activity(activity)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        activities = controller.view_my_fundraising_activities(
            owner_account_id=owner_account_id
        )
        if not activities:
            st.info("You have no fundraising activities yet.")
            return

        st.caption(f"{len(activities)} of your activities")
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": a.category,
                "Target": f"${a.target_amount}",
                "Start": a.start_date.isoformat(),
                "End": a.end_date.isoformat(),
                "Completed": "yes" if a.completed else "no",
                "Suspended": "yes" if a.suspended else "no",
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
    def display_my_fundraising_activity(activity) -> None:
        st.subheader(activity.title)
        st.write(f"**FRAId:** {activity.fra_id}")
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Target:** ${activity.target_amount}")
        st.write(
            f"**Runs:** {activity.start_date.isoformat()} → "
            f"{activity.end_date.isoformat()}"
        )
        st.write(f"**Completed:** {'yes' if activity.completed else 'no'}")
        st.write(f"**Suspended:** {'yes' if activity.suspended else 'no'}")
        st.write(activity.description)
