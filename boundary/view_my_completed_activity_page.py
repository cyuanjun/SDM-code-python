"""ViewMyCompletedActivityPage <<Boundary>> — Sprint 3 US-31.

Diagram contract (US-31.jpg):
    + displayMyCompletedActivity(fundraisingActivity: FundraisingActivity): void

Fundraiser picks one of their completed activities from a list (Exception A,
reuses view_my_fundraising_activities filtered to completed by the boundary)
and the page renders details.
"""
from __future__ import annotations

import streamlit as st

from controller.view_my_completed_activity_controller import (
    ViewMyCompletedActivityController,
)
from controller.view_my_fundraising_activity_controller import (
    ViewMyFundraisingActivityController,
)

SELECTED_KEY = "view_my_completed_selected_id"


class ViewMyCompletedActivityPage:
    def render(self) -> None:
        st.header("View My Completed Activity")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id
        controller = ViewMyCompletedActivityController()

        if SELECTED_KEY in st.session_state:
            activity = controller.view_my_completed_activity(
                owner_account_id=owner_account_id,
                fra_id=st.session_state[SELECTED_KEY],
            )
            if activity is None:
                st.error(
                    "Selected activity isn't yours, or is not completed."
                )
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_my_completed_activity(activity)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        all_mine = (
            ViewMyFundraisingActivityController()
            .view_my_fundraising_activities(owner_account_id=owner_account_id)
        )
        completed = [a for a in all_mine if a.completed]

        if not completed:
            st.info("You have no completed activities yet.")
            return

        st.caption(f"{len(completed)} of your completed activities")
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": a.category,
                "Target": f"${a.target_amount}",
                "Start": a.start_date.isoformat(),
                "End": a.end_date.isoformat(),
            }
            for a in completed
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
            st.session_state[SELECTED_KEY] = completed[selected[0]].fra_id
            st.rerun()

    @staticmethod
    def display_my_completed_activity(activity) -> None:
        st.subheader(activity.title)
        st.write(f"**FRAId:** {activity.fra_id}")
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Target:** ${activity.target_amount}")
        st.write(
            f"**Ran:** {activity.start_date.isoformat()} → "
            f"{activity.end_date.isoformat()}"
        )
        st.write(f"**Views:** {activity.view_count}")
        st.write(f"**Saves:** {activity.save_count}")
        st.write(activity.description)
