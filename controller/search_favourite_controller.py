"""SearchFavouriteController <<Controller>> — pure delegator, US-25.

The boundary supplies the donee's account_id from session so the search is
scoped to their own favourites.
"""
from __future__ import annotations

from typing import Optional

from entity.favourite_list import FavouriteList


class SearchFavouriteController:
    def submit_search_criteria(
        self, search_criteria: str, account_id: Optional[int] = None
    ) -> list[FavouriteList]:
        return FavouriteList.submit_search_criteria(search_criteria, account_id)
