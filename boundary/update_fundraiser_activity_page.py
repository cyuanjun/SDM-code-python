"""UpdateFundraiserActivityPage <<Boundary>> — Sprint 2 diagram US-15.

Fundraiser updates one of their own fundraising activities. List is scoped
to the logged-in fundraiser's activities.
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from boundary.create_fundraising_activity_page import DEFAULT_CATEGORIES
from controller.update_fundraiser_activity_controller import (
    UpdateFundraiserActivityController,
)
from controller.view_fundraiser_activity_controller import (
    ViewFundraiserActivityController,
)
from entity.fundraising_activity import FundraisingActivity

EDIT_KEY = "editing_fundraiser_activity_id"
STATUSES = ("active", "completed", "suspended")


class UpdateFundraiserActivityPage:
    def render(self) -> None:
        st.header("Update my fundraising activity")

        if "user" not in st.session_state:
            st.warning("Log in as a fundraiser first.")
            return
        owner_account_id = st.session_state["user"].account_id
        view_ctrl = ViewFundraiserActivityController()

        activities = view_ctrl.view_activities_by_owner(owner_account_id)
        if not activities:
            st.info("You have no activities to update.")
            return

        if EDIT_KEY not in st.session_state:
            labels = {f"#{a.activity_id} — {a.title}": a.activity_id for a in activities}
            choice = st.selectbox("Activity", list(labels.keys()))
            if st.button("Edit", key="click_edit_option_fra"):
                self.click_edit_option(str(labels[choice]))
                st.rerun()
            return

        self.display_update_page(owner_account_id)

    def display_update_page(self, owner_account_id: int) -> None:
        activity_id = st.session_state[EDIT_KEY]
        current = ViewFundraiserActivityController().view_fundraiser_activity(activity_id)
        if current is None or current.owner_account_id != owner_account_id:
            st.error("Activity not found or not owned by you.")
            st.session_state.pop(EDIT_KEY, None)
            return

        try:
            start_value = date.fromisoformat(current.start_date)
            end_value = date.fromisoformat(current.end_date)
        except ValueError:
            start_value = date.today()
            end_value = date.today()

        category_options = list(DEFAULT_CATEGORIES)
        if current.category not in category_options:
            category_options.append(current.category)

        with st.form("update_fra_form"):
            title = st.text_input("Title", value=current.title)
            description = st.text_area("Description", value=current.description or "")
            target_amount = st.number_input(
                "Target amount",
                min_value=0.0,
                value=float(current.target_amount),
                step=100.0,
            )
            category = st.selectbox(
                "Category", category_options, index=category_options.index(current.category)
            )
            start_date_in = st.date_input("Start date", value=start_value)
            end_date_in = st.date_input("End date", value=end_value)
            status = st.selectbox(
                "Status", STATUSES, index=STATUSES.index(current.status) if current.status in STATUSES else 0
            )
            cols = st.columns(2)
            submitted = cols[0].form_submit_button("Save changes", type="primary")
            cancelled = cols[1].form_submit_button("Cancel")

        if cancelled:
            st.session_state.pop(EDIT_KEY, None)
            st.rerun()
            return

        if not submitted:
            return

        if not self._validate(title, description, target_amount, start_date_in, end_date_in):
            self.display_error()
            return

        updated = FundraisingActivity(
            title=title.strip(),
            description=description.strip(),
            target_amount=float(target_amount),
            category=category,
            start_date=start_date_in.isoformat(),
            end_date=end_date_in.isoformat(),
            status=status,
            activity_id=int(activity_id),
            owner_account_id=owner_account_id,
        )
        success = UpdateFundraiserActivityController().update_fundraiser_activity(
            activity_id, updated
        )
        if success:
            self.display_success()
            st.session_state.pop(EDIT_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def click_edit_option(activity_id: str) -> None:
        st.session_state[EDIT_KEY] = activity_id

    @staticmethod
    def _validate(title, description, target_amount, start_date, end_date) -> bool:
        if not title.strip() or not description.strip():
            return False
        if target_amount <= 0:
            return False
        if start_date > end_date:
            return False
        return True

    @staticmethod
    def display_success() -> None:
        st.success("Fundraising activity updated.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not update fundraising activity.")
