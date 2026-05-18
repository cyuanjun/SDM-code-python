"""ViewFundraisingActivityController <<Controller>>."""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class ViewFundraisingActivityController:
    def view_fundraising_activity(
        self, activity_id: str
    ) -> Optional[FundraisingActivity]:
        return FundraisingActivity.view_fundraising_activity(activity_id)

    def view_all_fundraising_activities(self) -> list[FundraisingActivity]:
        return FundraisingActivity.view_all_fundraising_activities()
