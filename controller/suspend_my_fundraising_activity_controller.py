"""SuspendMyFundraisingActivityController <<Controller>>."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class SuspendMyFundraisingActivityController:
    def suspend_my_fundraising_activity(
        self, owner_account_id: str, fra_id: str
    ) -> bool:
        return FundraisingActivity.suspend_my_fundraising_activity(
            owner_account_id=owner_account_id, fra_id=fra_id
        )
