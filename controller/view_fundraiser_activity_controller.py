"""ViewFundraiserActivityController <<Controller>> — pure delegator, see Sprint 2 diagram US-14."""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity import FundraisingActivity


class ViewFundraiserActivityController:
    def view_fundraiser_activity(
        self, activity_id: str
    ) -> Optional[FundraisingActivity]:
        return FundraisingActivity.view_fundraiser_activity(activity_id)

    def view_activities_by_owner(
        self, owner_account_id: int
    ) -> list[FundraisingActivity]:
        """Powers the fundraiser's own-FSAs list view. Not in diagram —
        logged in todo.md for diagram catchup."""
        return FundraisingActivity.view_activities_by_owner(owner_account_id)
