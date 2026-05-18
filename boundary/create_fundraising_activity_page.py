"""CreateFundraisingActivityPage <<Boundary>>."""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

import streamlit as st

from controller.create_fundraising_activity_controller import (
    CreateFundraisingActivityController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)


class CreateFundraisingActivityPage:
    def render(self) -> None:
        st.header("Create Fundraising Activity")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        categories = (
            ViewFundraisingActivityCategoryController().view_all_categories()
        )
        active_categories = [c for c in categories if not c.suspended]
        if not active_categories:
            st.warning(
                "No active categories exist yet. Ask the platform manager "
                "to create one before adding fundraising activities."
            )
            return

        with st.form("create_fra_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            target_amount_str = st.text_input("Target amount", value="0.00")
            cat_options = {c.category_name: c.fra_cat_id for c in active_categories}
            category_name = st.selectbox("Category", list(cat_options.keys()))
            fra_cat_id = cat_options[category_name]
            start_date = st.date_input("Start date", value=date.today())
            end_date = st.date_input("End date", value=date.today())
            submitted = st.form_submit_button("Create activity")

        if not submitted:
            return

        if not self.validate_activity(
            title, description, target_amount_str, fra_cat_id, start_date, end_date
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
                fra_cat_id=fra_cat_id,
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
        fra_cat_id: str,
        start_date: date,
        end_date: date,
        today: date | None = None,
    ) -> bool:
        if not title.strip():
            return False
        if not description.strip():
            return False
        if not fra_cat_id.strip():
            return False
        try:
            amount = Decimal(target_amount_str)
        except (InvalidOperation, ValueError):
            return False
        if amount <= 0:
            return False
        if start_date > end_date:
            return False
        if start_date < (today or date.today()):
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
            "positive numeric target are required, start date must not be after "
            "end date, and start date must not be in the past."
        )
