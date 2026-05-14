"""ViewUserAccountController <<Controller>> — Sprint 2 US-7.

Pure delegator. Hosts both view_user_account (per diagram) and
view_all_user_accounts (Exception A) so the boundary can show a list
before the admin picks one.
"""
from __future__ import annotations

from typing import Optional

from entity.user_account import UserAccount


class ViewUserAccountController:
    def view_user_account(self, account_id: str) -> Optional[UserAccount]:
        return UserAccount.view_user_account(account_id)

    def view_all_user_accounts(self) -> list[UserAccount]:
        return UserAccount.view_all_user_accounts()
