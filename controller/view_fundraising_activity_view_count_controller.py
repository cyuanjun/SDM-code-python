"""ViewFundraisingActivityViewCountController <<Controller>> — Sprint 4 US-28.

Pure delegator.
"""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class ViewFundraisingActivityViewCountController:
    def view_fundraising_activity_view_count(self, fra_id: str) -> int:
        return FundraisingActivity.view_fundraising_activity_view_count(fra_id)
