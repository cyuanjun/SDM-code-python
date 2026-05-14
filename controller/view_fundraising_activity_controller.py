"""ViewFundraisingActivityController <<Controller>> — Sprint 1 US-21.

Pure delegator. Two methods:
- view_fundraising_activity(activity_id) — per US-21 diagram.
- view_all_fundraising_activities() — Exception A (logged in docs/todo.md)
  so the boundary can show a list before the donee picks one.
"""
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
