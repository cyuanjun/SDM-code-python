"""SearchFavouriteController <<Controller>> — Sprint 3 US-25.

Pure delegator. Uses the 2-param sequence version (search_criteria,
account_id); the class diagram's viewMode is not exercised — typo
logged in docs/todo.md.
"""
from __future__ import annotations

from entity.favourite import Favourite


class SearchFavouriteController:
    def search_favourite(
        self, search_criteria: str, account_id: str
    ) -> list[Favourite]:
        return Favourite.search_favourite(
            search_criteria=search_criteria, account_id=account_id
        )
