"""ViewFavouriteListController <<Controller>> — Sprint 2 US-24.

Pure delegator. Matches the re-exported US-24 diagram which names the
boundary `ViewFavouriteListPage`, the controller `ViewFavouriteListController`,
and the entity method `viewFavouriteList(accountId): List<Favourite>`.
"""
from __future__ import annotations

from entity.favourite import Favourite


class ViewFavouriteListController:
    def view_favourite_list(self, account_id: str) -> list[Favourite]:
        return Favourite.view_favourite_list(account_id)
