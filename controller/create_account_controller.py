"""CreateAccountController <<Controller>> — Sprint 1 US-6.

Pure delegator. Forwards Boundary input to UserAccount.create_account.
"""
from __future__ import annotations

from datetime import date

from entity.user_account import UserAccount


class CreateAccountController:
    def create_account(
        self,
        email: str,
        password: str,
        name: str,
        dob: date,
        phone_num: str,
        profile_id: str,
    ) -> UserAccount:
        return UserAccount.create_account(
            email=email,
            password=password,
            name=name,
            dob=dob,
            phone_num=phone_num,
            profile_id=profile_id,
        )
