"""ViewFavouritePage <<Boundary>> — Sprint 2 US-24.

Diagram contract (US-24.jpg):
    + displayFavourite(favourite: Favourite): void
    (the diagram displays a single Favourite; the user story is "view ALL my
    favourites" so the implementation calls displayFavourites with the full
    list. Sprint 2 typo logged in docs/todo.md.)

Donee-only. Requires login.
"""
from __future__ import annotations

import streamlit as st

from controller.view_favourite_controller import ViewFavouriteController


class ViewFavouritePage:
    def render(self) -> None:
        st.header("My favourites")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        favourites = ViewFavouriteController().view_favourites(
            st.session_state["user"].account_id
        )
        self.display_favourites(favourites)

    @staticmethod
    def display_favourites(favourites) -> None:
        if not favourites:
            st.info("You haven't favourited any activities yet.")
            return

        st.caption(f"{len(favourites)} favourite activities")
        rows = [
            {"Account": f.account_id, "Activity": f.fra_id}
            for f in favourites
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
