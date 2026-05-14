"""CreateFundraisingActivityPage <<Boundary>> — Sprint 1 US-13.

Diagram contract (US-13.jpg):
    + displaySuccess(fundraisingActivity: FundraisingActivity): void

The fundraiser fills the form; owner_account_id comes from
st.session_state["user"].account_id (the logged-in fundraiser).
Category is a free-text input per the project rule "diagram says String,
Boundary uses text input" — no closed dropdown of categories in Sprint 1.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

import streamlit as st

from controller.create_fundraising_activity_controller import (
    CreateFundraisingActivityController,
)


class CreateFundraisingActivityPage:
    def render(self) -> None:
        st.header("Create fundraising activity")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        with st.form("create_fra_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            target_amount_str = st.text_input("Target amount", value="0.00")
            category = st.text_input("Category")
            start_date = st.date_input("Start date", value=date.today())
            end_date = st.date_input("End date", value=date.today())
            submitted = st.form_submit_button("Create activity")

        if not submitted:
            return

        if not self.validate_activity(
            title, description, target_amount_str, category, start_date, end_date
        ):
            self.display_error()
            return

        target_amount = Decimal(target_amount_str)
        owner_account_id = st.session_state["user"].account_id

        activity = (
            CreateFundraisingActivityController().create_fundraising_activity(
                title=title.strip(),
                description=description.strip(),
                target_amount=target_amount,
                category=category.strip(),
                start_date=start_date,
                end_date=end_date,
                owner_account_id=owner_account_id,
            )
        )
        self.display_success(activity)

    @staticmethod
    def validate_activity(
        title: str,
        description: str,
        target_amount_str: str,
        category: str,
        start_date: date,
        end_date: date,
    ) -> bool:
        if not title.strip():
            return False
        if not description.strip():
            return False
        if not category.strip():
            return False
        try:
            amount = Decimal(target_amount_str)
        except (InvalidOperation, ValueError):
            return False
        if amount <= 0:
            return False
        if start_date > end_date:
            return False
        return True

    @staticmethod
    def display_success(activity) -> None:
        st.success(
            f"Fundraising activity created: {activity.fra_id} — "
            f"{activity.title} (target ${activity.target_amount})"
        )

    @staticmethod
    def display_error() -> None:
        st.error(
            "Invalid fundraising activity. Title, description, category, and a "
            "positive numeric target are required, and start date must not be "
            "after end date."
        )
