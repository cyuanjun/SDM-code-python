"""Delegation tests for ViewFundraisingActivityController (US-21 + Exception A)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_activity() -> FundraisingActivity:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    account = UserAccount.create_account(
        email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )
    return FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100.00"),
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=account.account_id,
    )


def test_view_fundraising_activity_returns_activity_when_entity_returns_one() -> None:
    created = _seed_activity()

    result = ViewFundraisingActivityController().view_fundraising_activity(
        created.fra_id
    )

    assert isinstance(result, FundraisingActivity)
    assert result.fra_id == created.fra_id


def test_view_fundraising_activity_returns_none_when_entity_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: when the entity returns None, the controller
    forwards None unchanged."""
    monkeypatch.setattr(
        FundraisingActivity,
        "view_fundraising_activity",
        classmethod(lambda cls, activity_id: None),
    )

    assert (
        ViewFundraisingActivityController().view_fundraising_activity("anything")
        is None
    )


def test_view_all_returns_entity_list_unchanged() -> None:
    _seed_activity()

    activities = (
        ViewFundraisingActivityController().view_all_fundraising_activities()
    )

    assert [a.fra_id for a in activities] == ["fra_001"]


def test_view_all_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_all_fundraising_activities",
        classmethod(lambda cls: []),
    )

    assert (
        ViewFundraisingActivityController().view_all_fundraising_activities()
        == []
    )
