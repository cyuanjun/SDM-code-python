"""Delegation tests for CreateAccountController (US-6)."""
from __future__ import annotations

from datetime import date

import pytest

from controller.create_account_controller import CreateAccountController
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_the_user_account_entity_returns() -> None:
    profile = UserProfile.create_profile(role="admin", description="a")

    account = CreateAccountController().create_account(
        email="ada@x.com", password="p", name="Ada", dob=date(1990, 1, 15),
        phone_num="0", profile_id=profile.profile_id,
    )

    assert isinstance(account, UserAccount)
    assert account.account_id == "acc_001"
    assert account.email == "ada@x.com"


def test_controller_forwards_entity_return_value_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sentinel = UserAccount(
        email="s@x.com", password="p", name="S", dob=date(2000, 1, 1),
        phone_num="0", profile_id="prof_999", account_id="acc_999",
    )
    monkeypatch.setattr(
        UserAccount,
        "create_account",
        classmethod(
            lambda cls, email, password, name, dob, phone_num, profile_id: sentinel
        ),
    )

    result = CreateAccountController().create_account(
        email="x", password="x", name="x", dob=date(2000, 1, 1),
        phone_num="x", profile_id="x",
    )

    assert result is sentinel


def test_controller_forwards_none_when_entity_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: when the entity rejects a duplicate email
    by returning None, the controller forwards None unchanged."""
    monkeypatch.setattr(
        UserAccount,
        "create_account",
        classmethod(
            lambda cls, email, password, name, dob, phone_num, profile_id: None
        ),
    )

    result = CreateAccountController().create_account(
        email="dup@x.com", password="x", name="x", dob=date(2000, 1, 1),
        phone_num="x", profile_id="x",
    )

    assert result is None
