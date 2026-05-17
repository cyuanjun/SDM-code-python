"""MyFavouritesPage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines US-24 (view) + US-25 (search) into one
page. Search box at top filters the list.

Remove-favourite (US-23) lives on `ViewFundraisingActivityPage` (the
donee's activity detail page) — symmetric with US-22 Save. From this
page the donee navigates to a favourite's activity via [Browse
Fundraising Activities] and clicks Remove from the detail screen.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

import streamlit as st

from controller.search_favourite_controller import SearchFavouriteController
from controller.view_favourite_list_controller import ViewFavouriteListController


class MyFavouritesPage:
    def render(self) -> None:
        st.header("My Favourites")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

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

        st.caption(
            f"{len(favourites)} favourite(s) — open one via "
            f"[Browse Fundraising Activities] to remove it"
        )
        rows = [
            {"Activity": fav.fra_id, "Account": fav.account_id}
            for fav in favourites
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
