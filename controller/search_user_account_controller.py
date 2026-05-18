"""SearchUserAccountController <<Controller>>."""
from __future__ import annotations

from entity.user_account import UserAccount


class SearchUserAccountController:
    def search_user_account(self, search_criteria: str) -> list[UserAccount]:
        return UserAccount.search_user_account(search_criteria)
