"""ViewMyDonationHistoriesPage <<Boundary>> — Sprint 3 US-32 + US-33.

Diagram contracts (2026-05-18 set):
    US-32: + displayMatchingMyDonationHistories(donationList: List<Donation>): void
    US-33: + displayMyDonationHistories(donationList: List<Donation>): void

Both USes share this boundary class. US-32 fires when the donee submits
a search; US-33 is the default list rendering when no search criteria is
supplied.
"""
from __future__ import annotations

import streamlit as st

from controller.search_my_donation_histories_controller import (
    SearchMyDonationHistoriesController,
)
from controller.view_my_donation_histories_controller import (
    ViewMyDonationHistoriesController,
)


class ViewMyDonationHistoriesPage:
    def render(self) -> None:
        st.header("My Donation Histories")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        account_id = st.session_state["user"].account_id

        with st.form("my_donation_histories_form"):
            criteria = st.text_input(
                "Search criteria (leave blank to list all)",
                placeholder="Activity title, description, or category…",
            )
            submitted = st.form_submit_button("Show")

        if not submitted:
            donations = (
                ViewMyDonationHistoriesController()
                .view_my_donation_histories(account_id=account_id)
            )
            self.display_my_donation_histories(donations)
            return

        if criteria.strip():
            results = (
                SearchMyDonationHistoriesController()
                .search_my_donation_history(
                    account_id=account_id, search_criteria=criteria.strip(),
                )
            )
            self.display_matching_my_donation_histories(results)
        else:
            donations = (
                ViewMyDonationHistoriesController()
                .view_my_donation_histories(account_id=account_id)
            )
            self.display_my_donation_histories(donations)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_my_donation_histories(donations) -> None:
        if not donations:
            st.info("No donations match.")
            return
        st.caption(f"{len(donations)} match")
        ViewMyDonationHistoriesPage._render_table(donations)

    @staticmethod
    def display_my_donation_histories(donations) -> None:
        if not donations:
            st.info("You have no donations yet.")
            return
        st.caption(f"{len(donations)} donation(s)")
        ViewMyDonationHistoriesPage._render_table(donations)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")

    @staticmethod
    def _render_table(donations) -> None:
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
