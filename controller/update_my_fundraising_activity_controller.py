"""UpdateMyFundraisingActivityController <<Controller>> — Sprint 2 US-15.

Pure delegator. Forwards (owner_account_id, fra_id, updated_my_fra) to
FundraisingActivity.update_my_fundraising_activity. Ownership is enforced
at the entity layer.
"""
from __future__ import annotations

from entity.fundraising_activity import FundraisingActivity


class UpdateMyFundraisingActivityController:
    def update_my_fundraising_activity(
        self,
        owner_account_id: str,
        fra_id: str,
        updated_my_fra: FundraisingActivity,
    ) -> bool:
        return FundraisingActivity.update_my_fundraising_activity(
            owner_account_id=owner_account_id,
            fra_id=fra_id,
            updated_my_fra=updated_my_fra,
        )
