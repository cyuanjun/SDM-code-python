"""MyDonationsPage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines US-33 (view) + US-32 (search) into one
page. Search box at top filters; click a row to view details.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

import streamlit as st

from controller.search_my_donation_histories_controller import (
    SearchMyDonationHistoriesController,
)
from controller.view_my_donation_history_controller import (
    ViewMyDonationHistoryController,
)

SELECTED_KEY = "my_donations_selected_id"


class MyDonationsPage:
    def render(self) -> None:
        st.header("My Donations")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        account_id = st.session_state["user"].account_id

        if SELECTED_KEY in st.session_state:
            self._render_detail(account_id)
        else:
            self._render_list(account_id)

    def _render_list(self, account_id: str) -> None:
        search_term = st.text_input(
            "Search my donations",
            placeholder="Activity title, description, or category…",
        )
        if search_term.strip():
            donations = SearchMyDonationHistoriesController().search_my_donation_history(
                account_id=account_id, search_criteria=search_term.strip(),
            )
        else:
            donations = (
                ViewMyDonationHistoryController().view_my_donations(account_id)
            )

        if not donations:
            st.info(
                "No donations match." if search_term.strip()
                else "You have no donations yet."
            )
            return

        st.caption(f"{len(donations)} donation(s) — click a row to view")
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

    def _render_detail(self, account_id: str) -> None:
        donation = (
            ViewMyDonationHistoryController().view_my_donation_history(
                account_id=account_id,
                donation_id=st.session_state[SELECTED_KEY],
            )
        )
        if donation is None:
            st.error("Donation is not yours or no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        st.subheader(f"Donation {donation.donation_id}")
        st.write(f"**Activity:** {donation.fra_id}")
        st.write(f"**Amount:** ${donation.amount}")
        st.write(f"**Date:** {donation.donation_date.isoformat()}")

        if st.button("← Back to list"):
            st.session_state.pop(SELECTED_KEY, None)
            st.rerun()
