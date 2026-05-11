"""SearchFundraisingActivityCategoryController <<Controller>> — pure delegator, US-37."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class SearchFundraisingActivityCategoryController:
    def submit_search_criteria(
        self, search_criteria: str
    ) -> list[FundraisingActivityCategory]:
        return FundraisingActivityCategory.submit_search_criteria(search_criteria)
