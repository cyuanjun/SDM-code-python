"""DeleteFavouritePage <<Boundary>> — Sprint 3 diagram US-23."""
from __future__ import annotations

import streamlit as st

from controller.delete_favourite_controller import DeleteFavouriteController
from controller.view_favourite_list_controller import ViewFavouriteListController
from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)


class DeleteFavouritePage:
    def render(self) -> None:
        st.header("Delete a favourite")

        if "user" not in st.session_state:
            st.warning("Log in as a donee first.")
            return
        account_id = st.session_state["user"].account_id

        favourites = ViewFavouriteListController().view_favourite_list(account_id)
        if not favourites:
            st.info("Your favourites list is empty.")
            return

        view_ctrl = ViewFundraisingActivityController()
        labels: dict[str, int] = {}
        for fav in favourites:
            activity = view_ctrl.view_fundraising_activity_details(
                str(fav.activity_id)
            )
            if activity is None:
                continue
            labels[f"#{activity.activity_id} — {activity.title}"] = fav.activity_id

        if not labels:
            st.info("No removable favourites.")
            return

        choice = st.selectbox("Favourite", list(labels.keys()))

        if st.button("Delete", type="primary"):
            self.click_delete_favourite_option(labels[choice], account_id)

    @staticmethod
    def click_delete_favourite_option(activity_id, account_id) -> None:
        success = DeleteFavouriteController().delete_favourite(
            activity_id, account_id
        )
        if success:
            DeleteFavouritePage.display_success()
        else:
            DeleteFavouritePage.display_error()

    @staticmethod
    def display_success() -> None:
        st.success("Favourite deleted.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not delete favourite.")
