"""ViewFundraisingActivityPage <<Boundary>> — Sprint 1 US-21 + Sprint 2 US-22 + Sprint 3 US-23 + Sprint 4 US-28/29.

Diagram contracts:
    US-21.jpg: + displayFundraisingActivity(fundraisingActivity: FundraisingActivity): void
    US-22.jpg: + displaySuccess(): void  (save-to-favourites; same boundary class)
    US-23.jpg: + displaySuccess(): void  (remove-favourite; same boundary class — symmetric with US-22)
    US-28.jpg: + displayFundraisingActivityViewCount(viewCount: Integer): void
    US-29.jpg: + displayFundraisingActivitySaveCount(saveCount: Integer): void

US-22 (Save) and US-23 (Remove) both live on the donee's activity detail
page — mirrors how US-15 (Update) and US-16 (Suspend) live on the
fundraiser's MyFRA detail page. Whichever button is shown depends on
whether the activity is currently in the donee's favourites.

US-28 / US-29 diagrams place the view/save count display on this same
boundary; implementation gates the count display to the activity owner.

The Exception A view-count increment fires once when a donee opens
the detail view.
"""
from __future__ import annotations

import streamlit as st

from controller.remove_favourite_controller import RemoveFavouriteController
from controller.save_fundraising_activity_controller import (
    SaveFundraisingActivityController,
)
from controller.view_favourite_list_controller import ViewFavouriteListController
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
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


def _category_lookup() -> dict[str, str]:
    cats = ViewFundraisingActivityCategoryController().view_all_categories()
    return {c.fra_cat_id: c.category_name for c in cats}

SELECTED_KEY = "selected_fra_id"

# After Save/Remove fires the action message is stashed here so the
# post-rerun render can pick it up. `st.success(...)` followed by
# `st.rerun()` would otherwise discard the widget.
ACTION_MSG_KEY = "view_fra_action_msg"


class ViewFundraisingActivityPage:
    def render(self) -> None:
        st.header("View Fundraising Activity")
        controller = ViewFundraisingActivityController()

        if SELECTED_KEY in st.session_state:
            activity = controller.view_fundraising_activity(
                st.session_state[SELECTED_KEY]
            )
            if activity is None:
                st.error("Selected activity no longer exists.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                if ACTION_MSG_KEY in st.session_state:
                    st.success(st.session_state.pop(ACTION_MSG_KEY))
                self.display_fundraising_activity(activity)
                self._maybe_display_counts(activity)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.session_state.pop(ACTION_MSG_KEY, None)
                st.rerun()
            return

        activities = controller.view_all_fundraising_activities()
        if not activities:
            st.info("No fundraising activities yet.")
            return

        st.caption(f"{len(activities)} activities — click a row to view details")
        cat_lookup = _category_lookup()
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": cat_lookup.get(a.fra_cat_id, a.fra_cat_id),
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

    def display_fundraising_activity(self, activity) -> None:
        st.subheader(activity.title)
        cat_name = _category_lookup().get(activity.fra_cat_id, activity.fra_cat_id)
        st.write(f"**Category:** {cat_name}")
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

        # US-22 / US-23: donee saves or removes this activity to/from
        # their favourites. Mutually exclusive — show whichever applies.
        user = st.session_state.get("user")
        if user is None:
            return
        already_favourited = self._is_in_favourites(
            user.account_id, activity.fra_id
        )
        if already_favourited:
            if st.button("✖ Remove from favourites"):
                ok = (
                    RemoveFavouriteController()
                    .remove_favourite(
                        fra_id=activity.fra_id, account_id=user.account_id,
                    )
                )
                if ok:
                    st.session_state[ACTION_MSG_KEY] = (
                        "Removed from your favourites."
                    )
                    st.rerun()
                else:
                    self.display_remove_error()
        else:
            if st.button("⭐ Save to favourites"):
                ok = (
                    SaveFundraisingActivityController()
                    .save_fundraising_activity(
                        account_id=user.account_id, fra_id=activity.fra_id
                    )
                )
                if ok:
                    st.session_state[ACTION_MSG_KEY] = (
                        "Saved to your favourites."
                    )
                    st.rerun()
                else:
                    self.display_save_error()

    @staticmethod
    def _is_in_favourites(account_id: str, fra_id: str) -> bool:
        favourites = (
            ViewFavouriteListController().view_favourite_list(account_id)
        )
        return any(f.fra_id == fra_id for f in favourites)

    @staticmethod
    def display_success() -> None:
        st.success("Saved to your favourites.")

    @staticmethod
    def display_save_error() -> None:
        st.info("Already in your favourites.")

    @staticmethod
    def display_remove_success() -> None:
        st.success("Removed from your favourites.")

    @staticmethod
    def display_remove_error() -> None:
        st.error("Could not remove favourite.")

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
