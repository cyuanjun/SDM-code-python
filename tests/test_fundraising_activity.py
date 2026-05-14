"""Tests for the FundraisingActivity entity (US-13).

Diagram contract (US-13.jpg):
    + createFundraisingActivity(
        title: String, description: String, targetAmount: Decimal,
        category: String, startDate: Date, endDate: Date,
      ): FundraisingActivity

Implementation adds `owner_account_id` (the logged-in fundraiser's id) as
an additional parameter — the diagram lists ownerAccountId as an entity
attribute but the createFundraisingActivity signature does not include
it, which would leave the column unset. Logged in docs/todo.md as a
Sprint 1 typo: createFundraisingActivity needs ownerAccountId.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_fundraiser_account() -> UserAccount:
    profile = UserProfile.create_profile(role="fundraiser", description="Runs campaigns")
    return UserAccount.create_account(
        email="fr@x.com", password="p", name="Fr", dob=date(1980, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )


def test_create_fundraising_activity_persists_and_returns_with_prefixed_id() -> None:
    owner = _seed_fundraiser_account()

    activity = FundraisingActivity.create_fundraising_activity(
        title="Hospital fund",
        description="Save the local clinic",
        target_amount=Decimal("5000.00"),
        category="health",
        start_date=date(2026, 6, 1),
        end_date=date(2026, 12, 31),
        owner_account_id=owner.account_id,
    )

    assert activity.fra_id == "fra_001"
    assert activity.title == "Hospital fund"
    assert activity.description == "Save the local clinic"
    assert activity.target_amount == Decimal("5000.00")
    assert activity.category == "health"
    assert activity.start_date == date(2026, 6, 1)
    assert activity.end_date == date(2026, 12, 31)
    assert activity.owner_account_id == owner.account_id
    assert activity.completed is False
    assert activity.suspended is False
    assert activity.view_count == 0
    assert activity.save_count == 0


def test_create_fundraising_activity_assigns_sequential_ids() -> None:
    owner = _seed_fundraiser_account()

    first = FundraisingActivity.create_fundraising_activity(
        title="A", description="a", target_amount=Decimal("1.00"),
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )
    second = FundraisingActivity.create_fundraising_activity(
        title="B", description="b", target_amount=Decimal("2.00"),
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )

    assert first.fra_id == "fra_001"
    assert second.fra_id == "fra_002"


def test_create_fundraising_activity_raises_on_nonexistent_owner_account_id() -> None:
    """Negative path: owner_account_id is a FK to user_account.account_id.
    A bogus owner must fail loudly."""
    import sqlite3

    with pytest.raises(sqlite3.IntegrityError):
        FundraisingActivity.create_fundraising_activity(
            title="Ghost campaign", description="d",
            target_amount=Decimal("1.00"), category="x",
            start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
            owner_account_id="acc_999",
        )


def test_create_fundraising_activity_preserves_decimal_precision() -> None:
    """Negative path: target_amount is Decimal per the diagram (not Float).
    Persisting via TEXT and re-reading must not lose precision."""
    owner = _seed_fundraiser_account()

    activity = FundraisingActivity.create_fundraising_activity(
        title="Precise fund", description="d",
        target_amount=Decimal("12345.67"), category="x",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )

    assert activity.target_amount == Decimal("12345.67")
    assert isinstance(activity.target_amount, Decimal)
