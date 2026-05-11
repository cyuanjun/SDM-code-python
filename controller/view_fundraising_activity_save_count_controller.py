"""ViewFundraisingActivitySaveCountController <<Controller>> — pure delegator, US-29.

Diagram note: the US-29 class diagram lists the controller method as
`viewFundraisingActivityViewCount` (copy-paste from US-28). The intended name,
matching the class name and the boundary's display method, is
`viewFundraisingActivitySaveCount` — implemented here as
`view_fundraising_activity_save_count`. Logged in docs/todo.md "Sprint 4 diagram typos".
"""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class ViewFundraisingActivitySaveCountController:
    def view_fundraising_activity_save_count(self, activity_id: int) -> int:
        return FundraisingActivity.view_fundraising_activity_save_count(activity_id)
