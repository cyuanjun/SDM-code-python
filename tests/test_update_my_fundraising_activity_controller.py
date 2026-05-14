"""Delegation tests for UpdateMyFundraisingActivityController (US-15)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.update_my_fundraising_activity_controller import (
    UpdateMyFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_true_when_entity_updates_a_row() -> None:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    account = UserAccount.create_account(
        email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )
    created = FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100"),
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=account.account_id,
    )
    updated = FundraisingActivity(
        title="A2", description="d2", target_amount=Decimal("200"),
        category="y", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=account.account_id,
    )

    ok = UpdateMyFundraisingActivityController().update_fundraiser_activity(
        owner_account_id=account.account_id,
        fra_id=created.fra_id,
        updated_activity=updated,
    )

    assert ok is True


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: entity returns False (wrong owner or missing)."""
    monkeypatch.setattr(
        FundraisingActivity,
        "update_fundraiser_activity",
        classmethod(
            lambda cls, owner_account_id, fra_id, updated_activity: False
        ),
    )

    result = UpdateMyFundraisingActivityController().update_fundraiser_activity(
        owner_account_id="acc_001",
        fra_id="fra_001",
        updated_activity=FundraisingActivity(
            title="x", description="x", target_amount=Decimal("1"),
            category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
            owner_account_id="acc_001",
        ),
    )
    assert result is False
