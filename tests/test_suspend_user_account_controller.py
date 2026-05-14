"""Delegation tests for SuspendUserAccountController (US-9)."""
from __future__ import annotations

from datetime import date

import pytest

from controller.suspend_user_account_controller import (
    SuspendUserAccountController,
)
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_true_when_entity_suspends() -> None:
    profile = UserProfile.create_profile(role="admin", description="a")
    created = UserAccount.create_account(
        email="a@x.com", password="p", name="A", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )
    assert (
        SuspendUserAccountController().suspend_user_account(created.account_id)
        is True
    )


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserAccount,
        "suspend_user_account",
        classmethod(lambda cls, account_id: False),
    )
    assert SuspendUserAccountController().suspend_user_account("x") is False
