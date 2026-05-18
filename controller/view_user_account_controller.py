"""ViewUserAccountController <<Controller>>."""
from __future__ import annotations

from typing import Optional

from entity.user_account import UserAccount


class ViewUserAccountController:
    def view_user_account(self, account_id: str) -> Optional[UserAccount]:
        return UserAccount.view_user_account(account_id)

    def view_all_user_accounts(self) -> list[UserAccount]:
        return UserAccount.view_all_user_accounts()
