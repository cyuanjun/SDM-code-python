"""MyDonationsPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.search_my_donation_histories_controller import (
    SearchMyDonationHistoriesController,
)
from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)
from controller.view_my_donation_histories_controller import (
    ViewMyDonationHistoriesController,
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
                ViewMyDonationHistoriesController()
                .view_my_donation_histories(account_id=account_id)
            )

        if not donations:
            st.info(
                "No donations match." if search_term.strip()
                else "You have no donations yet."
            )
            return

        st.caption(f"{len(donations)} donation(s) — click a row to view")
        view_ctrl = ViewFundraisingActivityController()
        activities = {
            d.fra_id: view_ctrl.view_fundraising_activity(d.fra_id)
            for d in donations
        }
        rows = [
            {
                "ID": d.donation_id,
                "Activity ID": d.fra_id,
                "Title": activities[d.fra_id].title if activities[d.fra_id] else "(missing)",
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
        all_mine = (
            ViewMyDonationHistoriesController()
            .view_my_donation_histories(account_id=account_id)
        )
        target_id = st.session_state[SELECTED_KEY]
        donation = next(
            (d for d in all_mine if d.donation_id == target_id), None
        )
        if donation is None:
            st.error("Donation is not yours or no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        st.subheader(f"Donation {donation.donation_id}")
        activity = ViewFundraisingActivityController().view_fundraising_activity(
            donation.fra_id
        )
        if activity is not None:
            st.write(f"**Activity:** {activity.title} ({donation.fra_id})")
            st.write(f"**Description:** {activity.description}")
        else:
            st.write(f"**Activity:** {donation.fra_id} (no longer available)")
        st.write(f"**Amount:** ${donation.amount}")
        st.write(f"**Date:** {donation.donation_date.isoformat()}")

        if st.button("← Back to list"):
            st.session_state.pop(SELECTED_KEY, None)
            st.rerun()
