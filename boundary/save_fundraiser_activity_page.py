"""SaveFundraiserActivityPage <<Boundary>> — Sprint 2 diagram US-22.

Donee picks a fundraising activity from the public list and saves it to their
favourites. The save method receives (accountId, activityId) per the diagram.
"""
from __future__ import annotations

import streamlit as st

from controller.save_fundraiser_activity_controller import (
    SaveFundraiserActivityController,
)
from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)


class SaveFundraiserActivityPage:
    def render(self) -> None:
        st.header("Save fundraising activity to favourites")

        if "user" not in st.session_state:
            st.warning("Log in as a donee first.")
            return
        account_id = st.session_state["user"].account_id

        activities = ViewFundraisingActivityController().view_all_fundraising_activities()
        if not activities:
            st.info("No fundraising activities yet.")
            return

        labels = {f"#{a.activity_id} — {a.title}": a.activity_id for a in activities}
        choice = st.selectbox("Activity", list(labels.keys()))
        if st.button("Save to favourites", key="click_save_option", type="primary"):
            self.click_save_option(account_id, int(labels[choice]))

    def click_save_option(self, account_id, activity_id) -> None:
        success = SaveFundraiserActivityController().save_fundraising_activity(
            account_id, activity_id
        )
        if success:
            self.display_success()
        else:
            st.warning("Already in your favourites (or invalid activity).")

    @staticmethod
    def display_success() -> None:
        st.success("Saved to favourites.")
