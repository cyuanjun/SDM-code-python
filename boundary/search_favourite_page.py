"""SearchFavouritePage <<Boundary>> — Sprint 3 US-25.

Diagram contract (US-25.jpg):
    + displayMatchingFavourite(favouriteList: List<Favourite>): void

Class diagram names the boundary `ViewFundraisingActivitiesPage` —
collides with the Sprint 2 US-20 page. Implementation uses
`SearchFavouritePage` instead (typo logged in docs/todo.md).
"""
from __future__ import annotations

import streamlit as st

from controller.search_favourite_controller import SearchFavouriteController


class SearchFavouritePage:
    def render(self) -> None:
        st.header("Search My Favourites")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        account_id = st.session_state["user"].account_id

        with st.form("search_favourite_form"):
            criteria = st.text_input(
                "Search criteria",
                placeholder="Title, description, or category…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not self.validate_criteria(criteria):
            self.display_error()
            return

        results = SearchFavouriteController().search_favourite(
            search_criteria=criteria.strip(), account_id=account_id,
        )
        self.display_matching_favourite(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_favourite(favourites) -> None:
        if not favourites:
            st.info("No favourites match.")
            return
        st.caption(f"{len(favourites)} match")
        rows = [
            {"Activity": f.fra_id, "Account": f.account_id}
            for f in favourites
        ]
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")
