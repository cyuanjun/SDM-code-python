"""CreateAccountController <<Controller>> — pure delegator, see Sprint 1 diagram US-6."""
from __future__ import annotations

from typing import Optional

from entity.user_account import UserAccount


class CreateAccountController:
    def create_account(
        self,
        email: str,
        password: str,
        name: str,
        dob: str,
        phone_num: str,
        profile_id: int,
    ) -> Optional[UserAccount]:
        return UserAccount.create_account(email, password, name, dob, phone_num, profile_id)
