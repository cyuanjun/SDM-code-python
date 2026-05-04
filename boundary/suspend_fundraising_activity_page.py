"""SuspendFundraisingActivityPage <<Boundary>> — Sprint 3 diagram US-16.

Fundraiser suspends donations on one of *their own* fundraising activities.
"""
from __future__ import annotations

import streamlit as st

from controller.suspend_fundraising_activity_controller import (
    SuspendFundraisingActivityController,
)
from controller.view_fundraiser_activity_controller import (
    ViewFundraiserActivityController,
)


class SuspendFundraisingActivityPage:
    def render(self) -> None:
        st.header("Suspend my fundraising activity")

        if "user" not in st.session_state:
            st.warning("Log in as a fundraiser first.")
            return
        owner_account_id = st.session_state["user"].account_id

        activities = ViewFundraiserActivityController().view_activities_by_owner(
            owner_account_id
        )
        suspendable = [a for a in activities if a.status != "suspended"]
        if not suspendable:
            st.info("You have no active activities to suspend.")
            return

        labels = {self._label(a): a.activity_id for a in suspendable}
        choice = st.selectbox("Fundraising activity", list(labels.keys()))

        if st.button("Suspend", type="primary"):
            self.click_suspend_fundraising_activity_option(str(labels[choice]))

    @staticmethod
    def click_suspend_fundraising_activity_option(activity_id: str) -> None:
        success = SuspendFundraisingActivityController().suspend_fundraising_activity(
            activity_id
        )
        if success:
            SuspendFundraisingActivityPage.display_success()
        else:
            SuspendFundraisingActivityPage.display_error()

    @staticmethod
    def _label(activity) -> str:
        return (
            f"#{activity.activity_id} — {activity.title} "
            f"[{activity.status}]"
        )

    @staticmethod
    def display_success() -> None:
        st.success("Fundraising activity suspended.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not suspend the activity.")
