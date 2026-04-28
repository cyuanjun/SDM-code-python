"""ViewUserAccountPage <<Boundary>> — Sprint 2 diagram US-7.

Admin browses accounts and clicks one to view details. Maps to the diagram's
clickUserAccount() message.
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
            account = controller.view_user_account(st.session_state[SELECTED_KEY])
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
            st.info("No accounts yet.")
            return

        st.caption(f"{len(accounts)} accounts — click a row to view details")
        rows = [
            {
                "ID": a.account_id,
                "Email": a.email,
                "Name": a.name,
                "Profile ID": a.profile_id,
                "Suspended": a.suspended,
            }
            for a in accounts
        ]
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="df_view_accounts",
        )
        selected = event.selection.rows
        if selected:
            self.click_user_account(str(accounts[selected[0]].account_id))
            st.rerun()

    @staticmethod
    def click_user_account(account_id: str) -> None:
        st.session_state[SELECTED_KEY] = account_id

    @staticmethod
    def display_user_account(account) -> None:
        st.subheader(account.name)
        st.write(f"**Account ID:** {account.account_id}")
        st.write(f"**Email:** {account.email}")
        st.write(f"**DOB:** {account.dob}")
        st.write(f"**Phone:** {account.phone_num}")
        st.write(f"**Profile ID:** {account.profile_id}")
        st.write(f"**Suspended:** {'yes' if account.suspended else 'no'}")
