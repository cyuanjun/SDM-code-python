"""UpdateMyFundraisingActivityController <<Controller>> — Sprint 2 US-15.

Pure delegator. Forwards (owner_account_id, fra_id, updated_activity) to
FundraisingActivity.update_fundraiser_activity. Ownership is enforced at
the entity layer.
"""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class UpdateMyFundraisingActivityController:
    def update_fundraiser_activity(
        self,
        owner_account_id: str,
        fra_id: str,
        updated_activity: FundraisingActivity,
    ) -> bool:
        return FundraisingActivity.update_fundraiser_activity(
            owner_account_id=owner_account_id,
            fra_id=fra_id,
            updated_activity=updated_activity,
        )
