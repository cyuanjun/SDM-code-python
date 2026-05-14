"""LoginController <<Controller>> — Sprint 1 US-11/18/26/39.

Pure delegator. Used by all four actors (User admin, Fundraiser, Donee,
Platform manager) — the diagrams across US-11/18/26/39 all show the same
LoginPage + LoginController + UserAccount.login chain, just with
different actor stick-figures.
"""
from __future__ import annotations

from typing import Optional

from entity.user_account import UserAccount


class LoginController:
    def login(self, email: str, password: str) -> Optional[UserAccount]:
        return UserAccount.login(email, password)
