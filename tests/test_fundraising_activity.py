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


def _seed_activity(owner: UserAccount, title: str = "A") -> FundraisingActivity:
    return FundraisingActivity.create_fundraising_activity(
        title=title, description=f"{title} desc",
        target_amount=Decimal("100.00"), category="x",
        start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=owner.account_id,
    )


def test_view_fundraising_activity_returns_activity_for_existing_id() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    fetched = FundraisingActivity.view_fundraising_activity(created.fra_id)

    assert fetched is not None
    assert fetched.fra_id == created.fra_id
    assert fetched.title == created.title
    assert fetched.target_amount == created.target_amount
    assert fetched.owner_account_id == owner.account_id


def test_view_fundraising_activity_returns_none_for_missing_id() -> None:
    """Negative path: id with the right prefix but no matching row."""
    assert FundraisingActivity.view_fundraising_activity("fra_999") is None


def test_view_all_fundraising_activities_returns_empty_list_when_none_exist() -> None:
    """Negative path: caller gets [] back, not None."""
    assert FundraisingActivity.view_all_fundraising_activities() == []


def test_view_all_fundraising_activities_returns_all_in_insertion_order() -> None:
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="A")
    _seed_activity(owner, title="B")
    _seed_activity(owner, title="C")

    activities = FundraisingActivity.view_all_fundraising_activities()

    assert [a.fra_id for a in activities] == ["fra_001", "fra_002", "fra_003"]
    assert [a.title for a in activities] == ["A", "B", "C"]


def test_view_my_fundraising_activity_returns_activity_for_correct_owner() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    fetched = FundraisingActivity.view_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=created.fra_id,
    )

    assert fetched is not None
    assert fetched.fra_id == created.fra_id
    assert fetched.owner_account_id == owner.account_id


def test_view_my_fundraising_activity_returns_none_for_wrong_owner() -> None:
    """Negative path: ownership enforced — a fundraiser asking for someone
    else's activity by FRAId gets None back."""
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    # Seed a second fundraiser who doesn't own the activity.
    other_profile = UserProfile.create_profile(
        role="fundraiser", description="Other"
    )
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=other_profile.profile_id,
    )

    fetched = FundraisingActivity.view_my_fundraising_activity(
        owner_account_id=other.account_id, fra_id=created.fra_id,
    )

    assert fetched is None


def test_view_my_fundraising_activity_returns_none_for_missing_fra_id() -> None:
    """Negative path: no row matches the FRAId."""
    owner = _seed_fundraiser_account()

    assert (
        FundraisingActivity.view_my_fundraising_activity(
            owner_account_id=owner.account_id, fra_id="fra_999"
        )
        is None
    )


def test_view_my_fundraising_activities_returns_only_owners_rows() -> None:
    """Exception A list-by-owner: scopes the list to the caller's
    activities. Other fundraisers' rows are excluded."""
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="MineA")
    _seed_activity(owner, title="MineB")

    other_profile = UserProfile.create_profile(
        role="fundraiser", description="Other"
    )
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=other_profile.profile_id,
    )
    _seed_activity(other, title="Theirs")

    mine = FundraisingActivity.view_my_fundraising_activities(
        owner_account_id=owner.account_id
    )

    assert [a.title for a in mine] == ["MineA", "MineB"]


def test_view_my_fundraising_activities_returns_empty_list_for_no_owner_rows() -> None:
    """Negative path: a fundraiser with no activities gets [] back."""
    other_profile = UserProfile.create_profile(
        role="fundraiser", description="Other"
    )
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=other_profile.profile_id,
    )

    assert (
        FundraisingActivity.view_my_fundraising_activities(
            owner_account_id=other.account_id
        )
        == []
    )


def test_update_fundraiser_activity_returns_true_for_correct_owner() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    updated = FundraisingActivity(
        title="New title", description="New desc",
        target_amount=Decimal("999.99"), category="renamed",
        start_date=date(2027, 1, 1), end_date=date(2027, 12, 31),
        owner_account_id=owner.account_id,
        completed=True, suspended=False,
    )
    ok = FundraisingActivity.update_fundraiser_activity(
        owner_account_id=owner.account_id,
        fra_id=created.fra_id,
        updated_activity=updated,
    )

    assert ok is True
    fetched = FundraisingActivity.view_fundraising_activity(created.fra_id)
    assert fetched is not None
    assert fetched.title == "New title"
    assert fetched.target_amount == Decimal("999.99")
    assert fetched.completed is True


def test_update_fundraiser_activity_returns_false_for_wrong_owner() -> None:
    """Negative path: ownership enforced at the entity layer — another
    fundraiser cannot update someone else's activity even if the FRAId
    matches."""
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    other_profile = UserProfile.create_profile(
        role="fundraiser", description="Other"
    )
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=other_profile.profile_id,
    )

    updated = FundraisingActivity(
        title="Hijack", description="x", target_amount=Decimal("1"),
        category="x", start_date=date(2027, 1, 1), end_date=date(2027, 1, 2),
        owner_account_id=other.account_id,
    )
    ok = FundraisingActivity.update_fundraiser_activity(
        owner_account_id=other.account_id,
        fra_id=created.fra_id,
        updated_activity=updated,
    )

    assert ok is False
    fetched = FundraisingActivity.view_fundraising_activity(created.fra_id)
    assert fetched is not None
    assert fetched.title == "A"  # original


def test_update_fundraiser_activity_returns_false_for_missing_fra_id() -> None:
    owner = _seed_fundraiser_account()
    updated = FundraisingActivity(
        title="x", description="x", target_amount=Decimal("1"),
        category="x", start_date=date(2027, 1, 1), end_date=date(2027, 1, 2),
        owner_account_id=owner.account_id,
    )
    assert (
        FundraisingActivity.update_fundraiser_activity(
            owner_account_id=owner.account_id,
            fra_id="fra_999",
            updated_activity=updated,
        )
        is False
    )
