"""ViewCompletedActivityController <<Controller>> — pure delegator, US-31."""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class ViewCompletedActivityController:
    def view_completed_activity(
        self, activity_id: str
    ) -> Optional[FundraisingActivity]:
        return FundraisingActivity.view_completed_activity(activity_id)
