"""Delegation tests for LoginController (US-11/18/26/39)."""
from __future__ import annotations

from datetime import date

import pytest

from controller.login_controller import LoginController
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_user_account_on_match() -> None:
    profile = UserProfile.create_profile(role="admin", description="a")
    UserAccount.create_account(
        email="ada@x.com", password="p", name="Ada", dob=date(1990, 1, 15),
        phone_num="0400000017", profile_id=profile.profile_id,
    )

    result = LoginController().login("ada@x.com", "p")

    assert isinstance(result, UserAccount)
    assert result.email == "ada@x.com"


def test_controller_returns_none_when_entity_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: when UserAccount.login returns None, the
    controller must forward None unchanged."""
    monkeypatch.setattr(
        UserAccount, "login", classmethod(lambda cls, email, password: None)
    )

    assert LoginController().login("x", "y") is None
