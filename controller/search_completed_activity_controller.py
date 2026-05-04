"""SearchCompletedActivityController <<Controller>> — pure delegator, US-30.

Boundary passes the fundraiser's account_id and status='completed'.
"""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class SearchCompletedActivityController:
    def submit_search_criteria(
        self,
        search_criteria: str,
        owner_account_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.submit_search_criteria(
            search_criteria, owner_account_id, status
        )
