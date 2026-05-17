"""UpdateMyFundraisingActivityPage <<Boundary>> — Sprint 2 US-15.

Diagram contract (US-15.jpg):
    + displaySuccess(): void

Fundraiser-scoped. Lists own activities, picks one, edits, submits.
Category is a `st.selectbox` populated from the PM-curated list per the
2026-05-18 US-13 attribute change (`category: String` → `FRACatId: String`).
Ownership is enforced both at the boundary (list scoped by owner) and
at the entity (UPDATE … WHERE fra_id AND owner_account_id).
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

import streamlit as st

from controller.update_my_fundraising_activity_controller import (
    UpdateMyFundraisingActivityController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)
from controller.view_my_fundraising_activity_controller import (
    ViewMyFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity

SELECTED_KEY = "update_my_fra_selected_id"


class UpdateMyFundraisingActivityPage:
    def render(self) -> None:
        st.header("Update My Fundraising Activity")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id

        if SELECTED_KEY not in st.session_state:
            self._render_picker(owner_account_id)
            return

        view_controller = ViewMyFundraisingActivityController()
        current = view_controller.view_my_fundraising_activity(
            owner_account_id=owner_account_id,
            fra_id=st.session_state[SELECTED_KEY],
        )
        if current is None:
            st.error("Selected activity no longer exists or is not yours.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        categories = (
            ViewFundraisingActivityCategoryController().view_all_categories()
        )
        # Allow keeping the current category even if it's now suspended.
        cat_options = {c.category_name: c.fra_cat_id for c in categories}
        cat_id_to_name = {v: k for k, v in cat_options.items()}
        current_name = cat_id_to_name.get(current.fra_cat_id)
        ordered_names = list(cat_options.keys())
        default_index = (
            ordered_names.index(current_name) if current_name in ordered_names else 0
        )

        with st.form("update_my_fra_form"):
            st.write(f"**Editing:** {current.fra_id}")
            title = st.text_input("Title", value=current.title)
            description = st.text_area("Description", value=current.description)
            target_amount_str = st.text_input(
                "Target amount", value=str(current.target_amount)
            )
            category_name = st.selectbox(
                "Category", ordered_names, index=default_index
            )
            fra_cat_id = cat_options[category_name]
            start_date = st.date_input("Start date", value=current.start_date)
            end_date = st.date_input("End date", value=current.end_date)
            completed = st.checkbox("Completed", value=current.completed)
            suspended = st.checkbox("Suspended", value=current.suspended)

            col_a, col_b = st.columns(2)
            with col_a:
                submitted = st.form_submit_button("Save changes")
            with col_b:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state.pop(SELECTED_KEY, None)
            st.rerun()
            return

        if not submitted:
            return

        if not self.validate_activity(
            title, description, target_amount_str, fra_cat_id, start_date, end_date
        ):
            self.display_error()
            return

        target_amount = Decimal(target_amount_str)
        ok = UpdateMyFundraisingActivityController().update_my_fundraising_activity(
            owner_account_id=owner_account_id,
            fra_id=st.session_state[SELECTED_KEY],
            updated_my_fra=FundraisingActivity(
                title=title.strip(),
                description=description.strip(),
                target_amount=target_amount,
                fra_cat_id=fra_cat_id,
                start_date=start_date,
                end_date=end_date,
                owner_account_id=owner_account_id,
                completed=completed,
                suspended=suspended,
            ),
        )
        if ok:
            self.display_success()
            st.session_state.pop(SELECTED_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def _render_picker(owner_account_id: str) -> None:
        activities = (
            ViewMyFundraisingActivityController().view_my_fundraising_activities(
                owner_account_id=owner_account_id
            )
        )
        if not activities:
            st.info("You have no fundraising activities yet — create one first.")
            return

        st.caption("Pick an activity to update.")
        cat_lookup = _build_category_lookup()
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": cat_lookup.get(a.fra_cat_id, a.fra_cat_id),
                "Target": f"${a.target_amount}",
                "Start": a.start_date.isoformat(),
                "End": a.end_date.isoformat(),
            }
            for a in activities
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
            st.session_state[SELECTED_KEY] = activities[selected[0]].fra_id
            st.rerun()

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
        # Existing activities may legitimately have a past start_date (already
        # running), so we don't re-validate start_date here. But the end date
        # must still be today or later — you can't update an activity to end
        # retroactively.
        if end_date < (today or date.today()):
            return False
        return True

    @staticmethod
    def display_success() -> None:
        st.success("Fundraising activity updated.")

    @staticmethod
    def display_error() -> None:
        st.error(
            "Update failed. Title, description, category, and a positive "
            "numeric target are required, start date must not be after end "
            "date, and end date must not be in the past."
        )


def _build_category_lookup() -> dict[str, str]:
    """fra_cat_id -> category_name. Used to render readable categories in tables."""
    cats = ViewFundraisingActivityCategoryController().view_all_categories()
    return {c.fra_cat_id: c.category_name for c in cats}
