"""CreateFundraisingActivityCategoryPage <<Boundary>> — Sprint 4 diagram US-34."""
from __future__ import annotations

import streamlit as st

from controller.create_fundraising_activity_category_controller import (
    CreateFundraisingActivityCategoryController,
)


class CreateFundraisingActivityCategoryPage:
    def render(self) -> None:
        self.display_create_category_page()

    def display_create_category_page(self) -> None:
        st.header("Create fundraising activity category")
        with st.form("create_category_form"):
            category_name = st.text_input("Category name")
            description = st.text_area("Description")
            submitted = st.form_submit_button("Create category", type="primary")

        if not submitted:
            return
        if not self._validate(category_name, description):
            return

        success = CreateFundraisingActivityCategoryController().create_category(
            category_name.strip(), description.strip()
        )
        if success:
            self.display_success()
        else:
            self.display_error()

    @staticmethod
    def _validate(category_name: str, description: str) -> bool:
        if not category_name.strip():
            st.error("Category name is required.")
            return False
        if not description.strip():
            st.error("Description is required.")
            return False
        return True

    @staticmethod
    def display_success() -> None:
        st.success("Category created.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not create category — name may already exist.")
