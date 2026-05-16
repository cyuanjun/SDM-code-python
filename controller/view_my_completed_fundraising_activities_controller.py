"""ViewMyCompletedFundraisingActivitiesController — Sprint 3 US-31.

Pure delegator.
"""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class ViewMyCompletedFundraisingActivitiesController:
    def view_my_completed_fundraising_activities(
        self, owner_account_id: str
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.view_my_completed_fundraising_activities(
            owner_account_id=owner_account_id
        )
