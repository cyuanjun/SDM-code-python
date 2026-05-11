"""ViewFundraisingActivityCategoryPage <<Boundary>> — Sprint 4 diagram US-35.

Diagram note: the US-35 class diagram lists Boundary methods as
`displayCreateCategoryPage()` and `displaySuccess()`, which are copy-paste
errors from US-34. This page exposes `display_view_category_page()` and
`display_fra_category()` — see docs/todo.md "Sprint 4 diagram typos".
"""
from __future__ import annotations

import streamlit as st

from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)


class ViewFundraisingActivityCategoryPage:
    def render(self) -> None:
        self.display_view_category_page()

    def display_view_category_page(self) -> None:
        st.header("View fundraising activity category")
        controller = ViewFundraisingActivityCategoryController()
        categories = controller.view_all_categories()
        if not categories:
            st.info("No categories yet. Use [PM] Create FRA category to add one.")
            return

        labels = {self._label(c): c.category_id for c in categories}
        choice = st.selectbox("Category", list(labels.keys()))
        if st.button("View details"):
            self.click_fundraising_activity_category(int(labels[choice]))

    def click_fundraising_activity_category(self, category_id: int) -> None:
        category = ViewFundraisingActivityCategoryController().view_fundraising_activity_category(
            category_id
        )
        if category is None:
            st.error("Category not found.")
            return
        self.display_fra_category(category)

    @staticmethod
    def display_fra_category(category) -> None:
        st.subheader(category.category_name)
        st.write(f"**ID:** {category.category_id}")
        st.write(f"**Status:** {category.status}")
        st.write(f"**Description:** {category.description or '—'}")

    @staticmethod
    def _label(category) -> str:
        return f"#{category.category_id} — {category.category_name} ({category.status})"
