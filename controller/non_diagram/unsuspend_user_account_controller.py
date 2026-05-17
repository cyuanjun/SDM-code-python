"""UnsuspendUserAccountController — Exception A (UX). Pure delegator."""
from __future__ import annotations

from entity.user_account import UserAccount


class UnsuspendUserAccountController:
    def unsuspend_user_account(self, account_id: str) -> bool:
        return UserAccount.unsuspend_user_account(account_id)
