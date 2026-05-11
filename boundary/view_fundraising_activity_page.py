"""ViewFundraisingActivityPage <<Boundary>> — Sprint 1 diagram US-21.

Donee browses a list of fundraising activities and clicks one to view details.
Clicking maps to the diagram's selectFundraisingActivity(activityID) message.

Sprint 4 extension (US-28 / US-29): when the logged-in user is the activity's
owner, the page additionally shows the view count and save count via
displayFundraisingActivityViewCount() / displayFundraisingActivitySaveCount().
The donee's selectFundraisingActivity() click also bumps the activity's
view_count counter (US-28). See docs/todo.md for the diagram update owed.
"""
from __future__ import annotations

import streamlit as st

from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)
from controller.view_fundraising_activity_save_count_controller import (
    ViewFundraisingActivitySaveCountController,
)
from controller.view_fundraising_activity_view_count_controller import (
    ViewFundraisingActivityViewCountController,
)
from entity.fundraising_activity import FundraisingActivity

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
            width="stretch",
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
        # US-28: clicking through to the details view counts as one view.
        FundraisingActivity.increment_view_count(int(activity_id))

    def display_fundraising_activity_details(self, activity) -> None:
        st.subheader(activity.title)
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Status:** {activity.status}")
        st.write(f"**Target:** ${activity.target_amount:,.2f}")
        st.write(f"**Runs:** {activity.start_date} → {activity.end_date}")
        st.write(activity.description)

        user = st.session_state.get("user")
        if user is not None and user.account_id == activity.owner_account_id:
            view_count = ViewFundraisingActivityViewCountController().view_fundraising_activity_view_count(
                activity.activity_id
            )
            save_count = ViewFundraisingActivitySaveCountController().view_fundraising_activity_save_count(
                activity.activity_id
            )
            self.display_fundraising_activity_view_count(view_count)
            self.display_fundraising_activity_save_count(save_count)

    @staticmethod
    def display_fundraising_activity_view_count(view_count: int) -> None:
        st.metric("Views", view_count)

    @staticmethod
    def display_fundraising_activity_save_count(save_count: int) -> None:
        st.metric("Saves to favourites", save_count)
