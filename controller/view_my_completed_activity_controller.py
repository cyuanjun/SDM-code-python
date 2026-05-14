"""ViewMyCompletedActivityController — Sprint 3 US-31.

Pure delegator.
"""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class ViewMyCompletedActivityController:
    def view_my_completed_activity(
        self, owner_account_id: str, fra_id: str
    ) -> Optional[FundraisingActivity]:
        return FundraisingActivity.view_my_completed_activity(
            owner_account_id=owner_account_id, fra_id=fra_id
        )
