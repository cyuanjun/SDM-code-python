"""ViewUserAccountPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.suspend_user_account_controller import (
    SuspendUserAccountController,
)
from controller.view_user_account_controller import ViewUserAccountController

SELECTED_KEY = "selected_account_id"


class ViewUserAccountPage:
    def render(self) -> None:
        st.header("View User Account")
        controller = ViewUserAccountController()

        if SELECTED_KEY in st.session_state:
            account = controller.view_user_account(
                st.session_state[SELECTED_KEY]
            )
            if account is None:
                st.error("Selected account no longer exists.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_user_account(account)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        accounts = controller.view_all_user_accounts()
        if not accounts:
            st.info("No user accounts yet.")
            return

        st.caption(f"{len(accounts)} accounts — click a row to view details")
        rows = [
            {
                "ID": a.account_id,
                "Email": a.email,
                "Name": a.name,
                "Profile": a.profile_id,
                "Suspended": "yes" if a.suspended else "no",
            }
            for a in accounts
        ]
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        selected = event.selection.rows
        if selected:
            st.session_state[SELECTED_KEY] = accounts[selected[0]].account_id
            st.rerun()

    def display_user_account(self, account) -> None:
        st.subheader(account.name)
        st.write(f"**Account ID:** {account.account_id}")
        st.write(f"**Email:** {account.email}")
        st.write(f"**Date of birth:** {account.dob.isoformat()}")
        st.write(f"**Phone:** {account.phone_num}")
        st.write(f"**Profile:** {account.profile_id}")
        st.write(f"**Suspended:** {'yes' if account.suspended else 'no'}")

        if not account.suspended:
            if st.button("🚫 Suspend this account"):
                ok = SuspendUserAccountController().suspend_user_account(
                    account.account_id
                )
                if ok:
                    self.display_success()
                    st.rerun()
                else:
                    self.display_error()

    @staticmethod
    def display_success() -> None:
        st.success("Account suspended.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not suspend account.")
