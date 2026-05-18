"""BrowseFundraisingActivityPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.remove_favourite_controller import RemoveFavouriteController
from controller.save_fundraising_activity_controller import (
    SaveFundraisingActivityController,
)
from controller.search_fundraising_activity_controller import (
    SearchFundraisingActivityController,
)
from controller.view_favourite_list_controller import (
    ViewFavouriteListController,
)
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


ACTION_MSG_KEY = "browse_fra_action_msg"


def render_activity_detail(selected_key: str) -> None:
    fra_id = st.session_state[selected_key]
    activity = (
        ViewFundraisingActivityController()
        .view_fundraising_activity(fra_id)
    )
    if activity is None:
        st.error("Activity no longer exists.")
        st.session_state.pop(selected_key, None)
        return

    if ACTION_MSG_KEY in st.session_state:
        st.success(st.session_state.pop(ACTION_MSG_KEY))

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
    if user is not None:
        favourites = (
            ViewFavouriteListController().view_favourite_list(user.account_id)
        )
        already_favourited = any(f.fra_id == activity.fra_id for f in favourites)
        if already_favourited:
            if st.button("✖ Remove from favourites"):
                ok = (
                    RemoveFavouriteController()
                    .remove_favourite(
                        fra_id=activity.fra_id,
                        account_id=user.account_id,
                    )
                )
                if ok:
                    st.session_state[ACTION_MSG_KEY] = (
                        "Removed from your favourites."
                    )
                    st.rerun()
                else:
                    st.error("Could not remove from favourites.")
        else:
            if st.button("⭐ Save to favourites"):
                ok = (
                    SaveFundraisingActivityController()
                    .save_fundraising_activity(
                        account_id=user.account_id,
                        fra_id=activity.fra_id,
                    )
                )
                if ok:
                    st.session_state[ACTION_MSG_KEY] = (
                        "Saved to your favourites."
                    )
                    st.rerun()
                else:
                    st.info("Already in your favourites.")

    if st.button("← Back to list"):
        st.session_state.pop(selected_key, None)
        st.session_state.pop(ACTION_MSG_KEY, None)
        st.rerun()


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

    def _render_detail(self) -> None:
        render_activity_detail(SELECTED_KEY)
