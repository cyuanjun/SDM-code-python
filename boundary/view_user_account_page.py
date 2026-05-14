"""ViewUserAccountPage <<Boundary>> — Sprint 2 US-7.

Diagram contract (US-07.jpg):
    + displayUserAccount(account: UserAccount): void

List-then-detail pattern. The list uses Exception A view_all_user_accounts.
"""
from __future__ import annotations

import streamlit as st

from controller.view_user_account_controller import ViewUserAccountController

SELECTED_KEY = "selected_account_id"


class ViewUserAccountPage:
    def render(self) -> None:
        st.header("View user account")
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

    @staticmethod
    def display_user_account(account) -> None:
        st.subheader(account.name)
        st.write(f"**Account ID:** {account.account_id}")
        st.write(f"**Email:** {account.email}")
        st.write(f"**Date of birth:** {account.dob.isoformat()}")
        st.write(f"**Phone:** {account.phone_num}")
        st.write(f"**Profile:** {account.profile_id}")
        st.write(f"**Suspended:** {'yes' if account.suspended else 'no'}")
