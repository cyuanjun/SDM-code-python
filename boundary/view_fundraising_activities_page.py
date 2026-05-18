"""ViewFundraisingActivitiesPage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.search_fundraising_activity_controller import (
    SearchFundraisingActivityController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)


def _category_lookup() -> dict[str, str]:
    cats = ViewFundraisingActivityCategoryController().view_all_categories()
    return {c.fra_cat_id: c.category_name for c in cats}


class ViewFundraisingActivitiesPage:
    def render(self) -> None:
        st.header("Search Fundraising Activities")

        with st.form("search_fra_form"):
            criteria = st.text_input(
                "Search criteria",
                placeholder="Title, description, or category…",
            )
            submitted = st.form_submit_button("Search")

        if not submitted:
            return

        if not self.validate_criteria(criteria):
            self.display_error()
            return

        results = (
            SearchFundraisingActivityController().search_fundraising_activity(
                criteria.strip()
            )
        )
        self.display_matching_fundraising_activities(results)

    @staticmethod
    def validate_criteria(criteria: str) -> bool:
        return bool(criteria.strip())

    @staticmethod
    def display_matching_fundraising_activities(activities) -> None:
        if not activities:
            st.info("No activities match.")
            return
        st.caption(f"{len(activities)} match")
        cat_lookup = _category_lookup()
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
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def display_error() -> None:
        st.error("Please enter a search term.")
