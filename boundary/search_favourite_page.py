"""SearchFavouritePage <<Boundary>> — Sprint 3 diagram US-25.

Donee searches their own favourites by title/description/category of the
linked fundraising activity. Account is taken from session.
"""
from __future__ import annotations

import streamlit as st

from controller.search_favourite_controller import SearchFavouriteController
from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)


class SearchFavouritePage:
    def render(self) -> None:
        if "user" not in st.session_state:
            st.warning("Log in as a donee first.")
            return
        self.display_search_page()

    def display_search_page(self) -> None:
        st.header("Search my favourites")
        with st.form("search_favourite_form"):
            criteria = st.text_input(
                "Search (title, description, or category — leave blank for all)"
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        account_id = st.session_state["user"].account_id
        results = SearchFavouriteController().submit_search_criteria(
            criteria.strip(), account_id=account_id
        )
        self.display_matching_favourite(results)

    @staticmethod
    def display_matching_favourite(activity_list) -> None:
        if not activity_list:
            st.info("No favourites matched your search.")
            return

        view_ctrl = ViewFundraisingActivityController()
        rows = []
        for fav in activity_list:
            activity = view_ctrl.view_fundraising_activity_details(
                str(fav.activity_id)
            )
            if activity is None:
                continue
            rows.append({
                "ID": activity.activity_id,
                "Title": activity.title,
                "Category": activity.category,
                "Status": activity.status,
                "Target": activity.target_amount,
                "Start": activity.start_date,
                "End": activity.end_date,
            })

        st.caption(f"{len(rows)} matches")
        st.dataframe(rows, width="stretch", hide_index=True)
