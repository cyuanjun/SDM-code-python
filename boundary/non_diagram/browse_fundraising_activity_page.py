"""BrowseFundraisingActivityPage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines US-20 (search) + US-21 (view detail) +
US-22 (save to favourites). The save action is already on the detail
view per the US-22 diagram; this page just merges search + browse.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

import streamlit as st

from controller.save_fundraising_activity_controller import (
    SaveFundraisingActivityController,
)
from controller.search_fundraising_activity_controller import (
    SearchFundraisingActivityController,
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

SELECTED_KEY = "browse_fra_selected_id"


class BrowseFundraisingActivityPage:
    def render(self) -> None:
        st.header("Browse Fundraising Activities")

        if SELECTED_KEY in st.session_state:
            self._render_detail()
        else:
            self._render_list()

    def _render_list(self) -> None:
        search_term = st.text_input(
            "Search activities",
            placeholder="Title, description, or category…",
        )
        if search_term.strip():
            activities = (
                SearchFundraisingActivityController()
                .search_fundraising_activity(search_term.strip())
            )
        else:
            activities = (
                ViewFundraisingActivityController()
                .view_all_fundraising_activities()
            )

        if not activities:
            st.info(
                "No activities match." if search_term.strip()
                else "No fundraising activities yet."
            )
            return

        st.caption(f"{len(activities)} activity(s) — click a row to view details")
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
            # US-28: bump view count.
            FundraisingActivity.increment_view_count(chosen)
            st.session_state[SELECTED_KEY] = chosen
            st.rerun()

    def _render_detail(self) -> None:
        fra_id = st.session_state[SELECTED_KEY]
        activity = (
            ViewFundraisingActivityController()
            .view_fundraising_activity(fra_id)
        )
        if activity is None:
            st.error("Activity no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

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

        # Owner-gated metrics (US-28 / US-29).
        user = st.session_state.get("user")
        if user is not None and user.account_id == activity.owner_account_id:
            view_count = (
                ViewFundraisingActivityViewCountController()
                .view_fundraising_activity_view_count(activity.fra_id)
            )
            save_count = (
                ViewFundraisingActivitySaveCountController()
                .view_fundraising_activity_save_count(activity.fra_id)
            )
            cols = st.columns(2)
            cols[0].metric("Views", view_count)
            cols[1].metric("Saves to favourites", save_count)

        # US-22: save to favourites (donee action).
        if user is not None and st.button("⭐ Save to favourites"):
            ok = (
                SaveFundraisingActivityController()
                .save_fundraising_activity(
                    account_id=user.account_id, fra_id=activity.fra_id,
                )
            )
            if ok:
                st.success("Saved to your favourites.")
            else:
                st.info("Already in your favourites.")

        if st.button("← Back to list"):
            st.session_state.pop(SELECTED_KEY, None)
            st.rerun()
