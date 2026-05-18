"""SearchFundraisingActivityController <<Controller>>."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class SearchFundraisingActivityController:
    def search_fundraising_activity(
        self, search_criteria: str
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.search_fundraising_activity(search_criteria)
