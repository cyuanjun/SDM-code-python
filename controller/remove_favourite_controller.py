"""RemoveFavouriteController <<Controller>>."""
from __future__ import annotations

from entity.favourite import Favourite


class RemoveFavouriteController:
    def remove_favourite(self, fra_id: str, account_id: str) -> bool:
        return Favourite.remove_favourite(fra_id=fra_id, account_id=account_id)
