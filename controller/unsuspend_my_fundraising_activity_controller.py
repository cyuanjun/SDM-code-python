"""UnsuspendMyFundraisingActivityController — Exception A (UX). Pure delegator."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class UnsuspendMyFundraisingActivityController:
    def unsuspend_my_fundraising_activity(
        self, owner_account_id: str, fra_id: str
    ) -> bool:
        return FundraisingActivity.unsuspend_my_fundraising_activity(
            owner_account_id=owner_account_id, fra_id=fra_id
        )
