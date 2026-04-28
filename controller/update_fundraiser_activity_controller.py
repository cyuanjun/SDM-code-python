"""UpdateFundraiserActivityController <<Controller>> — pure delegator, see Sprint 2 diagram US-15."""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class UpdateFundraiserActivityController:
    def update_fundraiser_activity(
        self, activity_id: str, updated_fundraiser: FundraisingActivity
    ) -> bool:
        return FundraisingActivity.update_fundraiser_activity(
            activity_id, updated_fundraiser
        )
