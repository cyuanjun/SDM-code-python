"""Delegation tests for UpdateUserAccountController (US-8)."""
from __future__ import annotations

from datetime import date

import pytest

from controller.update_user_account_controller import (
    UpdateUserAccountController,
)
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_true_when_entity_updates_a_row() -> None:
    profile = UserProfile.create_profile(role="admin", description="a")
    created = UserAccount.create_account(
        email="a@x.com", password="p", name="A", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )

    updated = UserAccount(
        email="a-new@x.com", password="new", name="A2",
        dob=date(1990, 1, 1), phone_num="9",
        profile_id=profile.profile_id,
    )

    assert (
        UpdateUserAccountController().update_user_account(
            created.account_id, updated
        )
        is True
    )


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: when the entity returns False (no match), the
    controller must forward False unchanged."""
    monkeypatch.setattr(
        UserAccount,
        "update_user_account",
        classmethod(lambda cls, account_id, updated_account: False),
    )

    result = UpdateUserAccountController().update_user_account(
        "anything",
        UserAccount(
            email="x", password="x", name="x", dob=date(2000, 1, 1),
            phone_num="x", profile_id="prof_001",
        ),
    )
    assert result is False
