"""ViewFundraisingActivityPage <<Boundary>>."""
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
from entity.fundraising_activity import FundraisingActivity


def _category_lookup() -> dict[str, str]:
    cats = ViewFundraisingActivityCategoryController().view_all_categories()
    return {c.fra_cat_id: c.category_name for c in cats}

SELECTED_KEY = "selected_fra_id"
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
