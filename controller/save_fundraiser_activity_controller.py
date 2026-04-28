"""SaveFundraiserActivityController <<Controller>> — pure delegator, see Sprint 2 diagram US-22."""
from __future__ import annotations

from entity.favourite_list import FavouriteList


class SaveFundraiserActivityController:
    def save_fundraising_activity(self, account_id, activity_id) -> bool:
        return FavouriteList.save_fundraising_activity(account_id, activity_id)
