"""MyFavouritesPage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines US-24 (view) + US-23 (remove) + US-25
(search) into one page. Search box at top filters the list; each row
has a Remove button.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

import streamlit as st

from controller.remove_favourite_controller import RemoveFavouriteController
from controller.search_favourite_controller import SearchFavouriteController
from controller.view_favourite_controller import ViewFavouriteController


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
                search_criteria=search_term.strip(), account_id=account_id,
            )
        else:
            favourites = ViewFavouriteController().view_favourites(account_id)

        if not favourites:
            st.info(
                "No favourites match." if search_term.strip()
                else "You haven't favourited any activities yet."
            )
            return

        st.caption(f"{len(favourites)} favourite(s)")
        for fav in favourites:
            cols = st.columns([3, 3, 1])
            cols[0].write(f"**Activity:** {fav.fra_id}")
            cols[1].write(f"**Account:** {fav.account_id}")
            if cols[2].button("Remove", key=f"remove-fav-{fav.fra_id}"):
                ok = RemoveFavouriteController().remove_favourite(
                    fra_id=fav.fra_id, account_id=account_id,
                )
                if ok:
                    st.success("Removed from favourites.")
                    st.rerun()
                else:
                    st.error("Could not remove favourite.")
