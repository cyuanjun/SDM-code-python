"""ViewFundraisingActivityController <<Controller>> — pure delegator, see Sprint 1 diagram US-21.

Note: `view_all_fundraising_activities` is not on the Sprint 1 class diagram.
Added so the Donee can pick from a list before triggering
selectFundraisingActivity(activityID). Class diagram needs updating for marking.
"""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class ViewFundraisingActivityController:
    def view_fundraising_activity_details(
        self, activity_id: str
    ) -> Optional[FundraisingActivity]:
        return FundraisingActivity.view_fundraising_activity_details(activity_id)

    def view_all_fundraising_activities(self) -> list[FundraisingActivity]:
        return FundraisingActivity.view_all_fundraising_activities()
