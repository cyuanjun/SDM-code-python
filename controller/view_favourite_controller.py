"""ViewFavouriteController <<Controller>> — Sprint 2 US-24.

Pure delegator. The diagram lists `viewFavourite(accountId): Favourite`
but the user story is "view ALL my favourites", so the implementation
returns List<Favourite>. Sprint 2 typo logged in docs/todo.md.
"""
from __future__ import annotations

from entity.favourite import Favourite


class ViewFavouriteController:
    def view_favourites(self, account_id: str) -> list[Favourite]:
        return Favourite.view_favourites(account_id)
