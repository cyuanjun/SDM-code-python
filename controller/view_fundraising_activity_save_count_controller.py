"""ViewFundraisingActivitySaveCountController <<Controller>> — Sprint 4 US-29.

Pure delegator.
"""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class ViewFundraisingActivitySaveCountController:
    def view_fundraising_activity_save_count(self, fra_id: str) -> int:
        return FundraisingActivity.view_fundraising_activity_save_count(fra_id)
