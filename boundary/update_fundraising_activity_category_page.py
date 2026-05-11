"""UpdateFundraisingActivityCategoryPage <<Boundary>> — Sprint 4 diagram US-36."""
from __future__ import annotations

import streamlit as st

from controller.update_fundraising_activity_category_controller import (
    UpdateFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)
from entity.fundraising_activity_category import FundraisingActivityCategory

EDIT_KEY = "editing_category_id"


class UpdateFundraisingActivityCategoryPage:
    def render(self) -> None:
        st.header("Update fundraising activity category")

        controller = ViewFundraisingActivityCategoryController()
        categories = controller.view_all_categories()
        if not categories:
            st.info("No categories to update.")
            return

        if EDIT_KEY not in st.session_state:
            labels = {self._label(c): c.category_id for c in categories}
            choice = st.selectbox("Category", list(labels.keys()))
            if st.button("Edit", key="click_edit_category"):
                self.click_edit_button(int(labels[choice]))
                st.rerun()
            return

        self.display_update_category_page()

    def display_update_category_page(self) -> None:
        category_id = int(st.session_state[EDIT_KEY])
        current = ViewFundraisingActivityCategoryController().view_fundraising_activity_category(
            category_id
        )
        if current is None:
            st.error("Category not found.")
            st.session_state.pop(EDIT_KEY, None)
            return

        with st.form("update_category_form"):
            name = st.text_input("Category name", value=current.category_name)
            description = st.text_area("Description", value=current.description or "")
            status = st.text_input("Status", value=current.status)
            cols = st.columns(2)
            submitted = cols[0].form_submit_button("Save changes", type="primary")
            cancelled = cols[1].form_submit_button("Cancel")

        if cancelled:
            st.session_state.pop(EDIT_KEY, None)
            st.rerun()
            return
        if not submitted:
            return
        if not self._validate(name, description, status):
            return

        updated = FundraisingActivityCategory(
            category_id=category_id,
            category_name=name.strip(),
            description=description.strip(),
            status=status.strip(),
        )
        success = UpdateFundraisingActivityCategoryController().update_fundraising_activity_category(
            category_id, updated
        )
        if success:
            self.display_success()
            st.session_state.pop(EDIT_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def click_edit_button(category_id: int) -> None:
        st.session_state[EDIT_KEY] = category_id

    @staticmethod
    def _validate(name: str, description: str, status: str) -> bool:
        if not name.strip():
            st.error("Category name is required.")
            return False
        if not description.strip():
            st.error("Description is required.")
            return False
        if not status.strip():
            st.error("Status is required.")
            return False
        return True

    @staticmethod
    def _label(category) -> str:
        return f"#{category.category_id} — {category.category_name} ({category.status})"

    @staticmethod
    def display_success() -> None:
        st.success("Category updated.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not update category.")
