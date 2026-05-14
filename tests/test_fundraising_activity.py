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


def test_search_fundraising_activity_matches_title_substring() -> None:
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Hospital fund")
    _seed_activity(owner, title="School fundraiser")
    _seed_activity(owner, title="Animal rescue")

    results = FundraisingActivity.search_fundraising_activity("fund")

    assert {a.title for a in results} == {"Hospital fund", "School fundraiser"}


def test_search_fundraising_activity_matches_description_or_category() -> None:
    owner = _seed_fundraiser_account()
    FundraisingActivity.create_fundraising_activity(
        title="A", description="medical aid for children",
        target_amount=Decimal("1"), category="health",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )
    FundraisingActivity.create_fundraising_activity(
        title="B", description="d", target_amount=Decimal("1"),
        category="medical-equipment",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )
    FundraisingActivity.create_fundraising_activity(
        title="C", description="d", target_amount=Decimal("1"),
        category="education",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )

    results = FundraisingActivity.search_fundraising_activity("medical")

    assert {a.title for a in results} == {"A", "B"}


def test_search_fundraising_activity_is_case_insensitive() -> None:
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Hospital fund")

    upper = FundraisingActivity.search_fundraising_activity("HOSPITAL")
    lower = FundraisingActivity.search_fundraising_activity("hospital")

    assert [a.title for a in upper] == ["Hospital fund"]
    assert [a.title for a in lower] == ["Hospital fund"]


def test_search_fundraising_activity_returns_empty_list_for_no_match() -> None:
    """Negative path: no match → []."""
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Hospital fund")

    assert FundraisingActivity.search_fundraising_activity("nothing") == []


def test_search_fundraising_activity_returns_empty_list_for_empty_db() -> None:
    """Negative path: empty DB → []."""
    assert FundraisingActivity.search_fundraising_activity("anything") == []


def test_suspend_my_fundraising_activity_returns_true_for_correct_owner() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)
    assert created.suspended is False

    ok = FundraisingActivity.suspend_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=created.fra_id,
    )

    assert ok is True
    fetched = FundraisingActivity.view_fundraising_activity(created.fra_id)
    assert fetched is not None
    assert fetched.suspended is True


def test_suspend_my_fundraising_activity_returns_false_for_wrong_owner() -> None:
    """Negative path: another fundraiser cannot suspend someone else's activity."""
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

    ok = FundraisingActivity.suspend_my_fundraising_activity(
        owner_account_id=other.account_id, fra_id=created.fra_id,
    )

    assert ok is False
    fetched = FundraisingActivity.view_fundraising_activity(created.fra_id)
    assert fetched is not None
    assert fetched.suspended is False  # untouched


def test_suspend_my_fundraising_activity_returns_false_for_missing_fra_id() -> None:
    owner = _seed_fundraiser_account()
    assert (
        FundraisingActivity.suspend_my_fundraising_activity(
            owner_account_id=owner.account_id, fra_id="fra_999"
        )
        is False
    )


def test_search_my_fundraising_activity_scopes_to_owner_and_matches_criteria() -> None:
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Hospital fund")
    _seed_activity(owner, title="School fundraiser")

    other_profile = UserProfile.create_profile(
        role="fundraiser", description="Other"
    )
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=other_profile.profile_id,
    )
    _seed_activity(other, title="Hospital research")

    mine = FundraisingActivity.search_my_fundraising_activity(
        owner_account_id=owner.account_id, search_criteria="hospital",
    )

    assert [a.title for a in mine] == ["Hospital fund"]


def test_search_my_fundraising_activity_returns_empty_for_no_match() -> None:
    """Negative path: owner has activities but none match the criteria."""
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Hospital fund")

    results = FundraisingActivity.search_my_fundraising_activity(
        owner_account_id=owner.account_id, search_criteria="nothing",
    )
    assert results == []


def test_search_my_fundraising_activity_returns_empty_for_no_activities() -> None:
    owner = _seed_fundraiser_account()
    results = FundraisingActivity.search_my_fundraising_activity(
        owner_account_id=owner.account_id, search_criteria="x",
    )
    assert results == []


def _seed_completed_activity(
    owner: UserAccount, title: str = "Done"
) -> FundraisingActivity:
    activity = FundraisingActivity.create_fundraising_activity(
        title=title, description=f"{title} desc",
        target_amount=Decimal("100"), category="x",
        start_date=date(2025, 1, 1), end_date=date(2025, 6, 1),
        owner_account_id=owner.account_id,
    )
    # Mark it completed via direct update — no "complete" use case exists.
    updated = FundraisingActivity(
        title=activity.title, description=activity.description,
        target_amount=activity.target_amount, category=activity.category,
        start_date=activity.start_date, end_date=activity.end_date,
        owner_account_id=owner.account_id,
        completed=True, suspended=False,
    )
    FundraisingActivity.update_fundraiser_activity(
        owner_account_id=owner.account_id,
        fra_id=activity.fra_id,
        updated_activity=updated,
    )
    return activity


def test_search_my_completed_fra_matches_only_completed_and_owner_scoped() -> None:
    owner = _seed_fundraiser_account()
    completed = _seed_completed_activity(owner, title="Hospital fund")
    ongoing = _seed_activity(owner, title="Hospital research")  # NOT completed
    assert ongoing.completed is False
    assert completed.fra_id != ongoing.fra_id

    results = FundraisingActivity.search_my_completed_fra(
        owner_account_id=owner.account_id, search_criteria="hospital",
    )

    assert [a.fra_id for a in results] == [completed.fra_id]


def test_search_my_completed_fra_excludes_other_owners_completed_activities() -> None:
    owner = _seed_fundraiser_account()
    _seed_completed_activity(owner, title="Mine done")

    other_profile = UserProfile.create_profile(
        role="fundraiser", description="Other"
    )
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=other_profile.profile_id,
    )
    _seed_completed_activity(other, title="Theirs done")

    results = FundraisingActivity.search_my_completed_fra(
        owner_account_id=owner.account_id, search_criteria="done",
    )
    assert [a.title for a in results] == ["Mine done"]


def test_search_my_completed_fra_returns_empty_for_no_matches() -> None:
    """Negative path: owner has no completed activities → []."""
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Still going")  # not completed

    assert (
        FundraisingActivity.search_my_completed_fra(
            owner_account_id=owner.account_id, search_criteria="going"
        )
        == []
    )


def test_view_my_completed_activity_returns_activity_for_correct_owner() -> None:
    owner = _seed_fundraiser_account()
    completed = _seed_completed_activity(owner)

    fetched = FundraisingActivity.view_my_completed_activity(
        owner_account_id=owner.account_id, fra_id=completed.fra_id,
    )
    assert fetched is not None
    assert fetched.fra_id == completed.fra_id
    assert fetched.completed is True


def test_view_my_completed_activity_returns_none_for_not_completed() -> None:
    """Negative path: ongoing activity isn't returned by the 'completed'
    view even if the caller owns it."""
    owner = _seed_fundraiser_account()
    ongoing = _seed_activity(owner)
    assert ongoing.completed is False

    assert (
        FundraisingActivity.view_my_completed_activity(
            owner_account_id=owner.account_id, fra_id=ongoing.fra_id
        )
        is None
    )


def test_view_my_completed_activity_returns_none_for_wrong_owner() -> None:
    owner = _seed_fundraiser_account()
    completed = _seed_completed_activity(owner)

    other_profile = UserProfile.create_profile(
        role="fundraiser", description="Other"
    )
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=other_profile.profile_id,
    )

    assert (
        FundraisingActivity.view_my_completed_activity(
            owner_account_id=other.account_id, fra_id=completed.fra_id
        )
        is None
    )


def test_view_fundraising_activity_view_count_returns_zero_initially() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    assert FundraisingActivity.view_fundraising_activity_view_count(
        created.fra_id
    ) == 0


def test_view_fundraising_activity_view_count_returns_zero_for_missing_id() -> None:
    """Negative path: missing FRAId returns 0, not None / raises."""
    assert (
        FundraisingActivity.view_fundraising_activity_view_count("fra_999")
        == 0
    )


def test_view_fundraising_activity_save_count_returns_zero_initially() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    assert FundraisingActivity.view_fundraising_activity_save_count(
        created.fra_id
    ) == 0


def test_increment_view_count_bumps_by_one() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    assert FundraisingActivity.increment_view_count(created.fra_id) is True
    assert FundraisingActivity.increment_view_count(created.fra_id) is True

    assert (
        FundraisingActivity.view_fundraising_activity_view_count(created.fra_id)
        == 2
    )


def test_increment_view_count_returns_false_for_missing_id() -> None:
    """Negative path: no row matches."""
    assert FundraisingActivity.increment_view_count("fra_999") is False


def test_increment_save_count_supports_positive_and_negative_delta() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    FundraisingActivity.increment_save_count(created.fra_id, +3)
    assert (
        FundraisingActivity.view_fundraising_activity_save_count(created.fra_id)
        == 3
    )
    FundraisingActivity.increment_save_count(created.fra_id, -2)
    assert (
        FundraisingActivity.view_fundraising_activity_save_count(created.fra_id)
        == 1
    )


def test_increment_save_count_floors_at_zero() -> None:
    """Negative path: decrementing past 0 floors at 0, doesn't go negative."""
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    FundraisingActivity.increment_save_count(created.fra_id, -5)
    assert (
        FundraisingActivity.view_fundraising_activity_save_count(created.fra_id)
        == 0
    )
