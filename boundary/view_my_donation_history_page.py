"""ViewMyDonationHistoryPage <<Boundary>> — Sprint 3 US-33.

Diagram contract (US-33.jpg):
    + displayMyDonationHistory(donation: Donation): void

Donee picks one of their donations (Exception A view_my_donations) and
the page renders the details.
"""
from __future__ import annotations

import streamlit as st

from controller.view_my_donation_history_controller import (
    ViewMyDonationHistoryController,
)

SELECTED_KEY = "view_my_donation_selected_id"


class ViewMyDonationHistoryPage:
    def render(self) -> None:
        st.header("View My Donation History")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        account_id = st.session_state["user"].account_id
        controller = ViewMyDonationHistoryController()

        if SELECTED_KEY in st.session_state:
            donation = controller.view_my_donation_history(
                account_id=account_id,
                donation_id=st.session_state[SELECTED_KEY],
            )
            if donation is None:
                st.error("Selected donation is not yours or no longer exists.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_my_donation_history(donation)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        donations = controller.view_my_donations(account_id)
        if not donations:
            st.info("You have no donations yet.")
            return

        st.caption(f"{len(donations)} donations")
        rows = [
            {
                "ID": d.donation_id,
                "Activity": d.fra_id,
                "Amount": f"${d.amount}",
                "Date": d.donation_date.isoformat(),
            }
            for d in donations
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
            st.session_state[SELECTED_KEY] = donations[selected[0]].donation_id
            st.rerun()

    @staticmethod
    def display_my_donation_history(donation) -> None:
        st.subheader(f"Donation {donation.donation_id}")
        st.write(f"**Activity:** {donation.fra_id}")
        st.write(f"**Amount:** ${donation.amount}")
        st.write(f"**Date:** {donation.donation_date.isoformat()}")
