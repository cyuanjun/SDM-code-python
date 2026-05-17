"""UpdateFundraisingActivityCategoryPage <<Boundary>> — Sprint 4 US-36."""
from __future__ import annotations

import streamlit as st

from controller.update_fundraising_activity_category_controller import (
    UpdateFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)

SELECTED_KEY = "update_fra_cat_selected_id"


class UpdateFundraisingActivityCategoryPage:
    def render(self) -> None:
        st.header("Update Fundraising Activity Category")

        if SELECTED_KEY not in st.session_state:
            self._render_picker()
            return

        view_controller = ViewFundraisingActivityCategoryController()
        current = view_controller.view_fundraising_activity_category(
            st.session_state[SELECTED_KEY]
        )
        if current is None:
            st.error("Selected category no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        with st.form("update_fra_cat_form"):
            st.write(f"**Editing:** {current.fra_cat_id}")
            name = st.text_input("Category name", value=current.category_name)
            description = st.text_area("Description", value=current.description)
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

        if not self.validate_category(name, description):
            self.display_error()
            return

        ok = (
            UpdateFundraisingActivityCategoryController()
            .update_fundraising_activity_category(
                fra_cat_id=st.session_state[SELECTED_KEY],
                category_name=name.strip(),
                description=description.strip(),
            )
        )
        if ok:
            self.display_success()
            st.session_state.pop(SELECTED_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def _render_picker() -> None:
        cats = (
            ViewFundraisingActivityCategoryController().view_all_categories()
        )
        if not cats:
            st.info("No categories yet — create one first.")
            return
        st.caption("Pick a category to update.")
        rows = [
            {
                "ID": c.fra_cat_id,
                "Name": c.category_name,
                "Description": c.description,
                "Suspended": "yes" if c.suspended else "no",
            }
            for c in cats
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
            st.session_state[SELECTED_KEY] = cats[selected[0]].fra_cat_id
            st.rerun()

    @staticmethod
    def validate_category(name: str, description: str) -> bool:
        return bool(name.strip()) and bool(description.strip())

    @staticmethod
    def display_success() -> None:
        st.success("Category updated.")

    @staticmethod
    def display_error() -> None:
        st.error("Update failed. Name and description are both required.")
