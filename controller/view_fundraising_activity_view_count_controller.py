"""ViewFundraisingActivityViewCountController <<Controller>> — pure delegator, US-28."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class ViewFundraisingActivityViewCountController:
    def view_fundraising_activity_view_count(self, activity_id: int) -> int:
        return FundraisingActivity.view_fundraising_activity_view_count(activity_id)
