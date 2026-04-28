"""CreateFundraisingActivityPage <<Boundary>> — Sprint 1 diagram US-13."""
from __future__ import annotations

from datetime import date

import streamlit as st

from controller.create_fundraising_activity_controller import (
    CreateFundraisingActivityController,
)

DEFAULT_CATEGORIES = ("medical", "education", "disaster_relief", "community", "other")


class CreateFundraisingActivityPage:
    def render(self) -> None:
        st.header("Create fundraising activity")
        with st.form("create_fsa_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            target_amount = st.number_input("Target amount", min_value=0.0, step=100.0)
            category = st.selectbox("Category", DEFAULT_CATEGORIES)
            start_date = st.date_input("Start date", value=date.today())
            end_date = st.date_input("End date", value=date.today())
            submitted = st.form_submit_button("Create activity")

        if not submitted:
            return

        if not self.validate_fundraising_activity(
            title, description, target_amount, start_date, end_date
        ):
            self.display_fundraising_activity_validation_error()
            return

        owner_email = (
            st.session_state["user"].email if "user" in st.session_state else None
        )
        success = CreateFundraisingActivityController().create_fundraising_activity(
            title=title,
            description=description,
            target_amount=float(target_amount),
            category=category,
            start_date=start_date,
            end_date=end_date,
            owner_email=owner_email,
        )
        if success:
            self.display_fundraising_activity_confirmation()
        else:
            self.display_fundraising_activity_validation_error()

    @staticmethod
    def validate_fundraising_activity(
        title: str,
        description: str,
        target_amount: float,
        start_date: date,
        end_date: date,
    ) -> bool:
        if not title.strip() or not description.strip():
            return False
        if target_amount <= 0:
            return False
        if start_date > end_date:
            return False
        return True

    @staticmethod
    def display_fundraising_activity_confirmation() -> None:
        st.success("Fundraising activity created.")

    @staticmethod
    def display_fundraising_activity_validation_error() -> None:
        st.error(
            "Invalid fundraising activity details. "
            "Check that all fields are filled, target amount is positive, and dates are valid."
        )
