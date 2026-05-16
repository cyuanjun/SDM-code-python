"""ViewFavouriteListPage <<Boundary>> — Sprint 2 US-24 + Sprint 3 US-23 + US-25.

Diagram contracts:
    US-24.jpg: + displayFavouriteList(favouriteList: List<Favourite>): void
    US-23.jpg: + displaySuccess(): void  (remove favourite; same page.)
    US-25.jpg: + displayMatchingFavourites(favouriteList: List<Favourite>): void
               (search favourites; same page.)

Donee-only. Lists current favourites or search matches; each row has a
Remove button.
"""
from __future__ import annotations

import streamlit as st

from controller.remove_favourite_controller import RemoveFavouriteController
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
            self.display_matching_favourites(favourites, account_id)
        else:
            favourites = ViewFavouriteListController().view_favourite_list(account_id)
            self.display_favourite_list(favourites, account_id)

    def display_favourite_list(self, favourites, account_id: str) -> None:
        if not favourites:
            st.info("You haven't favourited any activities yet.")
            return

        st.caption(f"{len(favourites)} favourite activities")
        self._render_rows(favourites, account_id)

    def display_matching_favourites(self, favourites, account_id: str) -> None:
        if not favourites:
            st.info("No favourites match.")
            return

        st.caption(f"{len(favourites)} match")
        self._render_rows(favourites, account_id)

    def _render_rows(self, favourites, account_id: str) -> None:
        for fav in favourites:
            cols = st.columns([3, 3, 1])
            cols[0].write(f"**Activity:** {fav.fra_id}")
            cols[1].write(f"**Account:** {fav.account_id}")
            if cols[2].button("Remove", key=f"remove-{fav.fra_id}"):
                ok = RemoveFavouriteController().remove_favourite(
                    fra_id=fav.fra_id, account_id=account_id,
                )
                if ok:
                    self.display_success()
                    st.rerun()
                else:
                    self.display_error()

    @staticmethod
    def display_success() -> None:
        st.success("Removed from favourites.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not remove favourite.")
