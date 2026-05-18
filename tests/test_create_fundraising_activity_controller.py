"""Delegation tests for CreateFundraisingActivityController (US-13)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.create_fundraising_activity_controller import (
    CreateFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _owner_account_id() -> str:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    account = UserAccount.create_account(
        email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
        phone_num="0400000021", profile_id=profile.profile_id,
    )
    return account.account_id


def test_controller_returns_the_fundraising_activity_entity_returns() -> None:
    owner_id = _owner_account_id()

    activity = CreateFundraisingActivityController().create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100.00"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=owner_id,
    )

    assert isinstance(activity, FundraisingActivity)
    assert activity.fra_id == "fra_001"


def test_controller_forwards_entity_return_value_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sentinel = FundraisingActivity(
        title="S", description="d", target_amount=Decimal("1.00"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id="acc_999", fra_id="fra_999",
    )

    def fake_create(cls, **kwargs):
        return sentinel

    monkeypatch.setattr(
        FundraisingActivity,
        "create_fundraising_activity",
        classmethod(fake_create),
    )

    result = CreateFundraisingActivityController().create_fundraising_activity(
        title="x", description="x", target_amount=Decimal("0"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id="x",
    )

    assert result is sentinel
