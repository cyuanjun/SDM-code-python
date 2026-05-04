"""SearchUserAccountPage <<Boundary>> — Sprint 3 diagram US-10.

Note: the US-10 class diagram has the boundary's display method named
displayMatchingUserProfile, with parameter type List<UserAccount>. The
sequence diagram (and code here) names it displayMatchingUserAccount —
see docs/todo.md "Sprint 3 diagram typos".
"""
from __future__ import annotations

import streamlit as st

from controller.search_user_account_controller import SearchUserAccountController


class SearchUserAccountPage:
    def render(self) -> None:
        self.display_search_page()

    def display_search_page(self) -> None:
        st.header("Search user accounts")
        with st.form("search_account_form"):
            criteria = st.text_input("Search (email or name)")
            submitted = st.form_submit_button("Search")

        if not submitted:
            return
        if not criteria.strip():
            st.error("Enter a search term.")
            return

        results = SearchUserAccountController().submit_search_criteria(
            criteria.strip()
        )
        self.display_matching_user_account(results)

    @staticmethod
    def display_matching_user_account(user_account) -> None:
        if not user_account:
            st.info("No accounts matched your search.")
            return
        st.caption(f"{len(user_account)} matches")
        rows = [
            {
                "ID": a.account_id,
                "Email": a.email,
                "Name": a.name,
                "Profile ID": a.profile_id,
                "Suspended": a.suspended,
            }
            for a in user_account
        ]
        st.dataframe(rows, width="stretch", hide_index=True)
