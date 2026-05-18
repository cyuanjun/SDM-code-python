"""SearchFundraisingActivityCategoryController <<Controller>>."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class SearchFundraisingActivityCategoryController:
    def search_fundraising_activity_category(
        self, search_criteria: str
    ) -> list[FundraisingActivityCategory]:
        return FundraisingActivityCategory.search_fundraising_activity_category(
            search_criteria
        )
