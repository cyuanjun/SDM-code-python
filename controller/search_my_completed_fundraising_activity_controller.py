"""SearchMyCompletedFundraisingActivityController <<Controller>>."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class SearchMyCompletedFundraisingActivityController:
    def search_my_completed_fundraising_activity(
        self, owner_account_id: str, search_criteria: str
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.search_my_completed_fundraising_activity(
            owner_account_id=owner_account_id, search_criteria=search_criteria
        )
