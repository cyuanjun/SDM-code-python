"""LoginController <<Controller>>."""
from __future__ import annotations

from typing import Optional

from entity.user_account import UserAccount


class LoginController:
    def login(self, email: str, password: str) -> Optional[UserAccount]:
        return UserAccount.login(email, password)
