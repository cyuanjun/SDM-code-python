"""SearchFundraiserActivityController <<Controller>> — pure delegator, see Sprint 2 diagram US-20."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class SearchFundraiserActivityController:
    def submit_search_criteria(
        self, search_criteria: str
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.submit_search_criteria(search_criteria)
