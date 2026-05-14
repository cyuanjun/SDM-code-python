"""UpdateUserAccountController <<Controller>> — Sprint 2 US-8.

Pure delegator. Forwards Boundary input to UserAccount.update_user_account.
"""
from __future__ import annotations

from entity.user_account import UserAccount


class UpdateUserAccountController:
    def update_user_account(
        self, account_id: str, updated_account: UserAccount
    ) -> bool:
        return UserAccount.update_user_account(account_id, updated_account)
