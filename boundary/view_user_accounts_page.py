"""ViewUserAccountsPage <<Boundary>> — Sprint 3 US-10.

Diagram contract (US-10.jpg):
    + displayMatchingUserAccount(accountList: List<UserAccount>): void
"""
from __future__ import annotations

import streamlit as st

from controller.search_user_account_controller import (
    SearchUserAccountController,
)


class ViewUserAccountsPage:
    def render(self) -> None:
        st.header("Search user accounts")

        with st.form("search_user_account_form"):
            criteria = st.text_input(
                "Search criteria",
                placeholder="Email or name…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not self.validate_criteria(criteria):
            self.display_error()
            return

        results = SearchUserAccountController().search_user_account(
            criteria.strip()
        )
        self.display_matching_user_account(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_user_account(accounts) -> None:
        if not accounts:
            st.info("No accounts match.")
            return
        st.caption(f"{len(accounts)} match")
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
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")
