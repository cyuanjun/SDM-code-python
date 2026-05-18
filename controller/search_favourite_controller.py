"""SearchFavouriteController <<Controller>>."""
from __future__ import annotations

from entity.favourite import Favourite


class SearchFavouriteController:
    def search_favourite(
        self, account_id: str, search_criteria: str
    ) -> list[Favourite]:
        return Favourite.search_favourite(
            account_id=account_id, search_criteria=search_criteria
        )
