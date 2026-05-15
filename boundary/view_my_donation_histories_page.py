"""ViewMyDonationHistoriesPage <<Boundary>> — Sprint 3 US-32.

Diagram contract (US-32.jpg):
    + displayMatchingDonationHistory(donationList: List<Donation>): void

Donee searches their donation history by activity title/description/category.
"""
from __future__ import annotations

import streamlit as st

from controller.search_donation_history_controller import (
    SearchDonationHistoryController,
)


class ViewMyDonationHistoriesPage:
    def render(self) -> None:
        st.header("Search My Donation History")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        account_id = st.session_state["user"].account_id

        with st.form("search_donation_history_form"):
            criteria = st.text_input(
                "Search criteria",
                placeholder="Activity title, description, or category…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not self.validate_criteria(criteria):
            self.display_error()
            return

        results = SearchDonationHistoryController().search_donation_history(
            search_criteria=criteria.strip(), account_id=account_id,
        )
        self.display_matching_donation_history(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_donation_history(donations) -> None:
        if not donations:
            st.info("No donations match.")
            return
        st.caption(f"{len(donations)} match")
        rows = [
            {
                "ID": d.donation_id,
                "Activity": d.fra_id,
                "Amount": f"${d.amount}",
                "Date": d.donation_date.isoformat(),
            }
            for d in donations
        ]
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")
