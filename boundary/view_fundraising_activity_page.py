"""ViewFundraisingActivityPage <<Boundary>> — Sprint 1 US-21 + Sprint 2 US-22 + Sprint 4 US-28/29.

Diagram contracts:
    US-21.jpg: + displayFundraisingActivity(fundraisingActivity: FundraisingActivity): void
    US-22.jpg: + displaySuccess(): void  (save-to-favourites; same boundary class)
    US-28.jpg: + displayFundraisingActivityViewCount(viewCount: Integer): void
    US-29.jpg: + displayFundraisingActivitySaveCount(saveCount: Integer): void

US-28 / US-29 diagrams place the view/save count display on this same
boundary (typo logged — actor is Fundraiser but boundary is donee's
page). Implementation gates the count display to the activity owner.

The Exception A view-count increment fires once when a donee opens
the detail view.
"""
from __future__ import annotations

import streamlit as st

from controller.save_fundraising_activity_controller import (
    SaveFundraisingActivityController,
)
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
                self._maybe_display_counts(activity)
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
            chosen = activities[selected[0]].fra_id
            # US-28: every donee detail view bumps the view count.
            FundraisingActivity.increment_view_count(chosen)
            st.session_state[SELECTED_KEY] = chosen
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

        # US-22: donee saves this activity to their favourites.
        user = st.session_state.get("user")
        if user is not None:
            if st.button("⭐ Save to favourites"):
                ok = (
                    SaveFundraisingActivityController()
                    .save_fundraising_activity(
                        account_id=user.account_id, fra_id=activity.fra_id
                    )
                )
                if ok:
                    self.display_success()
                else:
                    self.display_save_error()

    @staticmethod
    def display_success() -> None:
        st.success("Saved to your favourites.")

    @staticmethod
    def display_save_error() -> None:
        st.info("Already in your favourites.")

    def _maybe_display_counts(self, activity) -> None:
        """US-28 / US-29: render the view/save counts only when the
        logged-in user owns the activity. Diagram puts these on this
        page despite it being the donee view — owner-gating keeps the
        info private."""
        user = st.session_state.get("user")
        if user is None or user.account_id != activity.owner_account_id:
            return
        view_count = (
            ViewFundraisingActivityViewCountController()
            .view_fundraising_activity_view_count(activity.fra_id)
        )
        save_count = (
            ViewFundraisingActivitySaveCountController()
            .view_fundraising_activity_save_count(activity.fra_id)
        )
        self.display_fundraising_activity_view_count(view_count)
        self.display_fundraising_activity_save_count(save_count)

    @staticmethod
    def display_fundraising_activity_view_count(view_count: int) -> None:
        st.metric("Views", view_count)

    @staticmethod
    def display_fundraising_activity_save_count(save_count: int) -> None:
        st.metric("Saves to favourites", save_count)
