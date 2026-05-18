"""ViewFundraisingActivityCategoryPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.suspend_fundraising_activity_category_controller import (
    SuspendFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)

SELECTED_KEY = "selected_fra_cat_id"


class ViewFundraisingActivityCategoryPage:
    def render(self) -> None:
        st.header("View Fundraising Activity Category")
        controller = ViewFundraisingActivityCategoryController()

        if SELECTED_KEY in st.session_state:
            cat = controller.view_fundraising_activity_category(
                st.session_state[SELECTED_KEY]
            )
            if cat is None:
                st.error("Selected category no longer exists.")
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_fundraising_activity_category(cat)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        cats = controller.view_all_categories()
        if not cats:
            st.info("No categories yet.")
            return

        st.caption(f"{len(cats)} categories — click a row to view details")
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

    def display_fundraising_activity_category(self, category) -> None:
        st.subheader(category.category_name)
        st.write(f"**ID:** {category.fra_cat_id}")
        st.write(f"**Description:** {category.description or '(none)'}")
        st.write(f"**Suspended:** {'yes' if category.suspended else 'no'}")

        if not category.suspended:
            if st.button("🚫 Suspend this category"):
                ok = (
                    SuspendFundraisingActivityCategoryController()
                    .suspend_fundraising_activity_category(category.fra_cat_id)
                )
                if ok:
                    self.display_success()
                    st.rerun()
                else:
                    self.display_error()

    @staticmethod
    def display_success() -> None:
        st.success("Category suspended.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not suspend category.")
