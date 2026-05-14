"""Delegation tests for ViewMyFundraisingActivityController (US-14)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.view_my_fundraising_activity_controller import (
    ViewMyFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_owner_and_activity() -> tuple[UserAccount, FundraisingActivity]:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    account = UserAccount.create_account(
        email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )
    activity = FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100"),
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=account.account_id,
    )
    return account, activity


def test_view_my_returns_activity_when_entity_returns_one() -> None:
    owner, created = _seed_owner_and_activity()

    result = ViewMyFundraisingActivityController().view_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=created.fra_id,
    )

    assert isinstance(result, FundraisingActivity)
    assert result.fra_id == created.fra_id


def test_view_my_returns_none_when_entity_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: entity returns None (wrong owner or missing)."""
    monkeypatch.setattr(
        FundraisingActivity,
        "view_my_fundraising_activity",
        classmethod(lambda cls, owner_account_id, fra_id: None),
    )

    assert (
        ViewMyFundraisingActivityController().view_my_fundraising_activity(
            owner_account_id="acc_001", fra_id="fra_001"
        )
        is None
    )


def test_view_my_list_returns_entity_list_unchanged() -> None:
    owner, _ = _seed_owner_and_activity()

    rows = ViewMyFundraisingActivityController().view_my_fundraising_activities(
        owner_account_id=owner.account_id
    )

    assert [a.fra_id for a in rows] == ["fra_001"]


def test_view_my_list_returns_empty_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_my_fundraising_activities",
        classmethod(lambda cls, owner_account_id: []),
    )

    assert (
        ViewMyFundraisingActivityController().view_my_fundraising_activities(
            owner_account_id="acc_001"
        )
        == []
    )
