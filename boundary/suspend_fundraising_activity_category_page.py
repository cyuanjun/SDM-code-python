"""SuspendFundraisingActivityCategoryPage <<Boundary>> — Sprint 4 diagram US-38."""
from __future__ import annotations

import streamlit as st

from controller.suspend_fundraising_activity_category_controller import (
    SuspendFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)


class SuspendFundraisingActivityCategoryPage:
    def render(self) -> None:
        st.header("Suspend fundraising activity category")
        categories = ViewFundraisingActivityCategoryController().view_all_categories()
        active = [c for c in categories if c.status != "suspended"]
        if not active:
            st.info("No active categories to suspend.")
            return

        labels = {self._label(c): c.category_id for c in active}
        choice = st.selectbox("Category", list(labels.keys()))
        chosen_id = int(labels[choice])

        self.display_fra_category_detail(chosen_id)

        if st.button("Suspend", type="primary"):
            self.click_suspend_fra_category_button(chosen_id)

    def display_fra_category_detail(self, category_id: int) -> None:
        category = ViewFundraisingActivityCategoryController().view_fundraising_activity_category(
            category_id
        )
        if category is None:
            return
        st.write(f"**Name:** {category.category_name}")
        st.write(f"**Description:** {category.description or '—'}")
        st.write(f"**Status:** {category.status}")

    def click_suspend_fra_category_button(self, category_id: int) -> None:
        success = SuspendFundraisingActivityCategoryController().suspend_fundraising_activity_category(
            category_id
        )
        if success:
            self.display_success()
        else:
            self.display_error()

    @staticmethod
    def _label(category) -> str:
        return f"#{category.category_id} — {category.category_name}"

    @staticmethod
    def display_success() -> None:
        st.success("Category suspended.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not suspend category.")
