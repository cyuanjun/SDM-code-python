"""CreateFundraisingActivityCategoryPage <<Boundary>> — Sprint 4 US-34."""
from __future__ import annotations

import streamlit as st

from controller.create_fundraising_activity_category_controller import (
    CreateFundraisingActivityCategoryController,
)


class CreateFundraisingActivityCategoryPage:
    def render(self) -> None:
        st.header("Create Fundraising Activity Category")
        with st.form("create_fra_category_form"):
            name = st.text_input("Category name")
            description = st.text_area("Description")
            submitted = st.form_submit_button("Create category")

        if not submitted:
            return

        if not self.validate_category(name, description):
            self.display_error()
            return

        cat = (
            CreateFundraisingActivityCategoryController()
            .create_category(
                category_name=name.strip(), description=description.strip()
            )
        )
        self.display_success(cat)

    @staticmethod
    def validate_category(name: str, description: str) -> bool:
        return bool(name.strip()) and bool(description.strip())

    @staticmethod
    def display_success(category) -> None:
        st.success(
            f"Category created: {category.fra_cat_id} ({category.category_name})"
        )

    @staticmethod
    def display_error() -> None:
        st.error("Both category name and description are required.")
