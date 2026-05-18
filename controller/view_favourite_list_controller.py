"""ViewFavouriteListController <<Controller>>."""
from __future__ import annotations

from entity.favourite import Favourite


class ViewFavouriteListController:
    def view_favourite_list(self, account_id: str) -> list[Favourite]:
        return Favourite.view_favourite_list(account_id)
