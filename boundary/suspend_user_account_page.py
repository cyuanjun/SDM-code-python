"""SuspendUserAccountPage <<Boundary>> — Sprint 3 diagram US-9."""
from __future__ import annotations

import streamlit as st

from controller.suspend_user_account_controller import SuspendUserAccountController
from controller.view_user_account_controller import ViewUserAccountController


class SuspendUserAccountPage:
    def render(self) -> None:
        st.header("Suspend user account")

        accounts = ViewUserAccountController().view_all_user_accounts()
        active = [a for a in accounts if not a.suspended]
        if not active:
            st.info("No active accounts to suspend.")
            return

        labels = {self._label(a): a.account_id for a in active}
        choice = st.selectbox("Account", list(labels.keys()))

        if st.button("Suspend", type="primary"):
            self.click_suspend_user_account_option(str(labels[choice]))

    @staticmethod
    def click_suspend_user_account_option(account_id: str) -> None:
        success = SuspendUserAccountController().suspend_user_account(account_id)
        if success:
            SuspendUserAccountPage.display_success()
        else:
            SuspendUserAccountPage.display_error()

    @staticmethod
    def _label(account) -> str:
        return f"#{account.account_id} — {account.email} ({account.name})"

    @staticmethod
    def display_success() -> None:
        st.success("Account suspended.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not suspend account.")
