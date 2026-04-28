"""ViewFavouriteListPage <<Boundary>> — Sprint 2 diagram US-24."""
from __future__ import annotations

import streamlit as st

from controller.view_favourite_list_controller import ViewFavouriteListController
from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)


class ViewFavouriteListPage:
    def render(self) -> None:
        st.header("My favourites")

        if "user" not in st.session_state:
            st.warning("Log in as a donee first.")
            return
        account_id = st.session_state["user"].account_id

        favourites = ViewFavouriteListController().view_favourite_list(account_id)
        self.display_favourite_list(favourites)

    @staticmethod
    def display_favourite_list(favourite_list) -> None:
        if not favourite_list:
            st.info("Your favourites list is empty.")
            return

        view_ctrl = ViewFundraisingActivityController()
        rows = []
        for fav in favourite_list:
            activity = view_ctrl.view_fundraising_activity_details(str(fav.activity_id))
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

        st.caption(f"{len(rows)} favourited activities")
        st.dataframe(rows, width="stretch", hide_index=True)
