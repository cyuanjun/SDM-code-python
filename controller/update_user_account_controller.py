"""UpdateUserAccountController <<Controller>> — pure delegator, see Sprint 2 diagram US-8."""
from __future__ import annotations

from entity.user_account import UserAccount


class UpdateUserAccountController:
    def update_user_account(
        self, account_id: str, updated_account: UserAccount
    ) -> bool:
        return UserAccount.update_user_account(account_id, updated_account)
