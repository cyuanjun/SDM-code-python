"""SuspendUserAccountController <<Controller>> — pure delegator, US-9."""
from __future__ import annotations

from entity.user_account import UserAccount


class SuspendUserAccountController:
    def suspend_user_account(self, account_id: str) -> bool:
        return UserAccount.suspend_user_account(account_id)
