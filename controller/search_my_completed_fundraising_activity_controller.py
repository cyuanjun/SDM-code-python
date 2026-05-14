"""SearchMyCompletedFundraisingActivityController — Sprint 3 US-30.

Pure delegator.
"""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class SearchMyCompletedFundraisingActivityController:
    def search_my_completed_fra(
        self, owner_account_id: str, search_criteria: str
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.search_my_completed_fra(
            owner_account_id=owner_account_id, search_criteria=search_criteria
        )
