"""Delegation tests for SuspendMyFundraisingActivityController (US-16)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.suspend_my_fundraising_activity_controller import (
    SuspendMyFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_true_when_entity_suspends() -> None:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    account = UserAccount.create_account(
        email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
        phone_num="0400000021", profile_id=profile.profile_id,
    )
    created = FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=account.account_id,
    )

    ok = SuspendMyFundraisingActivityController().suspend_my_fundraising_activity(
        owner_account_id=account.account_id, fra_id=created.fra_id,
    )
    assert ok is True


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "suspend_my_fundraising_activity",
        classmethod(lambda cls, owner_account_id, fra_id: False),
    )
    assert (
        SuspendMyFundraisingActivityController().suspend_my_fundraising_activity(
            owner_account_id="x", fra_id="y"
        )
        is False
    )
