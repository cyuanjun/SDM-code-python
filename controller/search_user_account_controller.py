"""SearchUserAccountController <<Controller>> — pure delegator, US-10."""
from __future__ import annotations

from entity.user_account import UserAccount


class SearchUserAccountController:
    def submit_search_criteria(self, search_criteria: str) -> list[UserAccount]:
        return UserAccount.submit_search_criteria(search_criteria)
