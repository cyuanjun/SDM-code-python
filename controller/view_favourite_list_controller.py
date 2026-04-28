"""ViewFavouriteListController <<Controller>> — pure delegator, see Sprint 2 diagram US-24."""
from __future__ import annotations

from entity.favourite_list import FavouriteList


class ViewFavouriteListController:
    def view_favourite_list(self, account_id: str) -> list[FavouriteList]:
        return FavouriteList.view_favourite_list(account_id)
