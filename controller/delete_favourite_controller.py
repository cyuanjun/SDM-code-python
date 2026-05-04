"""DeleteFavouriteController <<Controller>> — pure delegator, US-23."""
from __future__ import annotations

from entity.favourite_list import FavouriteList


class DeleteFavouriteController:
    def delete_favourite(self, activity_id, account_id) -> bool:
        return FavouriteList.delete_favourite(activity_id, account_id)
