"""ViewFavouriteListPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.search_favourite_controller import SearchFavouriteController
from controller.view_favourite_list_controller import ViewFavouriteListController


class ViewFavouriteListPage:
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
            self.display_matching_favourites(favourites)
        else:
            favourites = ViewFavouriteListController().view_favourite_list(account_id)
            self.display_favourite_list(favourites)

    def display_favourite_list(self, favourites) -> None:
        if not favourites:
            st.info("You haven't favourited any activities yet.")
            return

        st.caption(f"{len(favourites)} favourite activities")
        self._render_table(favourites)

    def display_matching_favourites(self, favourites) -> None:
        if not favourites:
            st.info("No favourites match.")
            return

        st.caption(f"{len(favourites)} match")
        self._render_table(favourites)

    @staticmethod
    def _render_table(favourites) -> None:
        rows = [
            {"Activity": f.fra_id, "Account": f.account_id}
            for f in favourites
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
