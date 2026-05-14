"""SaveFundraisingActivityController <<Controller>> — Sprint 2 US-22.

Pure delegator. Forwards (account_id, fra_id) to
Favourite.save_fundraising_activity.
"""
from __future__ import annotations

from entity.favourite import Favourite


class SaveFundraisingActivityController:
    def save_fundraising_activity(
        self, account_id: str, fra_id: str
    ) -> bool:
        return Favourite.save_fundraising_activity(
            account_id=account_id, fra_id=fra_id
        )
