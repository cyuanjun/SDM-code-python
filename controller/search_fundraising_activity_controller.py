"""SearchFundraisingActivityController <<Controller>> — pure delegator, US-17.

Distinct from SearchFundraiserActivityController (donee, US-20) — same entity
method, different actor scope. Boundary supplies owner_account_id from session.
"""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class SearchFundraisingActivityController:
    def submit_search_criteria(
        self,
        search_criteria: str,
        owner_account_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.submit_search_criteria(
            search_criteria, owner_account_id, status
        )
