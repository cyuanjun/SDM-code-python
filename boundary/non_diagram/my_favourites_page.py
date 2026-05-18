"""MyFavouritesPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from boundary.non_diagram.browse_fundraising_activity_page import (
    _category_lookup,
    render_activity_detail,
)
from controller.search_favourite_controller import SearchFavouriteController
from controller.view_favourite_list_controller import ViewFavouriteListController
from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity


SELECTED_KEY = "my_favourites_selected_id"


class MyFavouritesPage:
    def render(self) -> None:
        st.header("My Favourites")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        if SELECTED_KEY in st.session_state:
            render_activity_detail(SELECTED_KEY)
            return

        self._render_list()

    def _render_list(self) -> None:
        account_id = st.session_state["user"].account_id

        search_term = st.text_input(
            "Search my favourites",
            placeholder="Activity title, description, or category…",
        )
        if search_term.strip():
            favourites = SearchFavouriteController().search_favourite(
                account_id=account_id, search_criteria=search_term.strip(),
            )
        else:
            favourites = ViewFavouriteListController().view_favourite_list(account_id)

        if not favourites:
            st.info(
                "No favourites match." if search_term.strip()
                else "You haven't favourited any activities yet."
            )
            return

        activities = [
            ViewFundraisingActivityController().view_fundraising_activity(f.fra_id)
            for f in favourites
        ]
        activities = [a for a in activities if a is not None]

        st.caption(f"{len(activities)} favourite(s) — click a row to view details")
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
