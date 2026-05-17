"""Delegation tests for SaveFundraisingActivityController (US-22)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.save_fundraising_activity_controller import (
    SaveFundraisingActivityController,
)
from entity.favourite import Favourite
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_true_when_entity_saves() -> None:
    donee_profile = UserProfile.create_profile(role="donee", description="r")
    donee = UserAccount.create_account(
        email="d@x.com", password="p", name="D", dob=date(1990, 1, 1),
        phone_num="0", profile_id=donee_profile.profile_id,
    )
    fr_profile = UserProfile.create_profile(role="fundraiser", description="r")
    fr = UserAccount.create_account(
        email="f@x.com", password="p", name="F", dob=date(1990, 1, 1),
        phone_num="0", profile_id=fr_profile.profile_id,
    )
    activity = FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=fr.account_id,
    )

    ok = SaveFundraisingActivityController().save_fundraising_activity(
        account_id=donee.account_id, fra_id=activity.fra_id
    )
    assert ok is True


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: entity returns False on duplicate."""
    monkeypatch.setattr(
        Favourite,
        "save_fundraising_activity",
        classmethod(lambda cls, account_id, fra_id: False),
    )

    assert (
        SaveFundraisingActivityController().save_fundraising_activity(
            account_id="acc_001", fra_id="fra_001"
        )
        is False
    )
