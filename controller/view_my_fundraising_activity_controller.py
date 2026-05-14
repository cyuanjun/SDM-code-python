"""ViewMyFundraisingActivityController <<Controller>> — Sprint 2 US-14.

Pure delegator. Both methods are ownership-scoped:
- view_my_fundraising_activity: per US-14 diagram.
- view_my_fundraising_activities: Exception A list-by-owner.
"""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class ViewMyFundraisingActivityController:
    def view_my_fundraising_activity(
        self, owner_account_id: str, fra_id: str
    ) -> Optional[FundraisingActivity]:
        return FundraisingActivity.view_my_fundraising_activity(
            owner_account_id=owner_account_id, fra_id=fra_id
        )

    def view_my_fundraising_activities(
        self, owner_account_id: str
    ) -> list[FundraisingActivity]:
        return FundraisingActivity.view_my_fundraising_activities(
            owner_account_id=owner_account_id
        )
