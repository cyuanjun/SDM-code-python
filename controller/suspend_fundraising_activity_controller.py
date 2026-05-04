"""SuspendFundraisingActivityController <<Controller>> — pure delegator, US-16."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class SuspendFundraisingActivityController:
    def suspend_fundraising_activity(self, activity_id: str) -> bool:
        return FundraisingActivity.suspend_fundraising_activity(activity_id)
