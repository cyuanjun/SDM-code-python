"""Tests for the FundraisingActivity entity (US-13).

Diagram contract (US-13.jpg, 2026-05-18 set):
    + createFundraisingActivity(
        title: String, description: String, targetAmount: Decimal,
        FRACatId: String, startDate: Date, endDate: Date,
        ownerAccountId: String,
      ): FundraisingActivity

The 2026-05-18 diagram replaced `category: String` with `FRACatId: String`
(an FK to `FundraisingActivityCategory`). Search methods JOIN against the
category table and match against `category_name`. A default "Test"
category (id `cat_001`) is seeded by `tests/conftest.py` so most tests
that don't care about the category can pass `fra_cat_id="cat_001"`.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from entity.fundraising_activity import FundraisingActivity
from entity.fundraising_activity_category import FundraisingActivityCategory
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
        fra_cat_id="cat_001",
        start_date=date(2026, 6, 1),
        end_date=date(2026, 12, 31),
        owner_account_id=owner.account_id,
    )

    assert activity.fra_id == "fra_001"
    assert activity.title == "Hospital fund"
    assert activity.description == "Save the local clinic"
    assert activity.target_amount == Decimal("5000.00")
    assert activity.fra_cat_id == "cat_001"
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
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )
    second = FundraisingActivity.create_fundraising_activity(
        title="B", description="b", target_amount=Decimal("2.00"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
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
            target_amount=Decimal("1.00"), fra_cat_id="cat_001",
            start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
            owner_account_id="acc_999",
        )


def test_create_fundraising_activity_preserves_decimal_precision() -> None:
    """Negative path: target_amount is Decimal per the diagram (not Float).
    Persisting via TEXT and re-reading must not lose precision."""
    owner = _seed_fundraiser_account()

    activity = FundraisingActivity.create_fundraising_activity(
        title="Precise fund", description="d",
        target_amount=Decimal("12345.67"), fra_cat_id="cat_001",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )

    assert activity.target_amount == Decimal("12345.67")
    assert isinstance(activity.target_amount, Decimal)


def _seed_activity(owner: UserAccount, title: str = "A") -> FundraisingActivity:
    """Seeds an *ongoing* activity (end_date in the future), so the derived
    `completed` property stays False unless the test explicitly changes
    end_date to a past value."""
    return FundraisingActivity.create_fundraising_activity(
        title=title, description=f"{title} desc",
        target_amount=Decimal("100.00"), fra_cat_id="cat_001",
        start_date=date(2099, 1, 1), end_date=date(2099, 2, 1),
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


def test_view_all_fundraising_activities_hides_suspended_from_donees() -> None:
    """Negative path of the donee-visible rule: a suspended activity is
    hidden from the browse list. Only the owner sees it (via
    view_my_fundraising_activities)."""
    owner = _seed_fundraiser_account()
    visible = _seed_activity(owner, title="Visible")
    hidden = _seed_activity(owner, title="Hidden")
    FundraisingActivity.suspend_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=hidden.fra_id,
    )

    activities = FundraisingActivity.view_all_fundraising_activities()

    assert [a.fra_id for a in activities] == [visible.fra_id]
    # Owner-scoped view still shows both — confirms suspended activities
    # remain visible to their owner.
    mine = FundraisingActivity.view_my_fundraising_activities(
        owner_account_id=owner.account_id
    )
    assert {a.fra_id for a in mine} == {visible.fra_id, hidden.fra_id}


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
    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=owner.profile_id,
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

    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=owner.profile_id,
    )
    _seed_activity(other, title="Theirs")

    mine = FundraisingActivity.view_my_fundraising_activities(
        owner_account_id=owner.account_id
    )

    assert [a.title for a in mine] == ["MineA", "MineB"]


def test_view_my_fundraising_activities_returns_empty_list_for_no_owner_rows() -> None:
    """Negative path: a fundraiser with no activities gets [] back."""
    other = _seed_fundraiser_account()

    assert (
        FundraisingActivity.view_my_fundraising_activities(
            owner_account_id=other.account_id
        )
        == []
    )


def test_update_my_fundraising_activity_returns_true_for_correct_owner() -> None:
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    # End date in the past → derived `completed` flips to True post-update.
    ok = FundraisingActivity.update_my_fundraising_activity(
        owner_account_id=owner.account_id,
        fra_id=created.fra_id,
        title="New title",
        description="New desc",
        target_amount=Decimal("999.99"),
        fra_cat_id="cat_001",
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
    )

    assert ok is True
    fetched = FundraisingActivity.view_fundraising_activity(created.fra_id)
    assert fetched is not None
    assert fetched.title == "New title"
    assert fetched.target_amount == Decimal("999.99")
    assert fetched.completed is True  # derived from end_date < today


def test_update_my_fundraising_activity_returns_false_for_wrong_owner() -> None:
    """Negative path: ownership enforced at the entity layer — another
    fundraiser cannot update someone else's activity even if the FRAId
    matches."""
    owner = _seed_fundraiser_account()
    created = _seed_activity(owner)

    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=owner.profile_id,
    )

    ok = FundraisingActivity.update_my_fundraising_activity(
        owner_account_id=other.account_id,
        fra_id=created.fra_id,
        title="Hijack",
        description="x",
        target_amount=Decimal("1"),
        fra_cat_id="cat_001",
        start_date=date(2027, 1, 1),
        end_date=date(2027, 1, 2),
    )

    assert ok is False
    fetched = FundraisingActivity.view_fundraising_activity(created.fra_id)
    assert fetched is not None
    assert fetched.title == "A"  # original


def test_update_my_fundraising_activity_returns_false_for_missing_fra_id() -> None:
    owner = _seed_fundraiser_account()
    assert (
        FundraisingActivity.update_my_fundraising_activity(
            owner_account_id=owner.account_id,
            fra_id="fra_999",
            title="x",
            description="x",
            target_amount=Decimal("1"),
            fra_cat_id="cat_001",
            start_date=date(2027, 1, 1),
            end_date=date(2027, 1, 2),
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
    medical_cat = FundraisingActivityCategory.create_category(
        category_name="Medical equipment", description="surgical supplies",
    )
    FundraisingActivity.create_fundraising_activity(
        title="A", description="medical aid for children",
        target_amount=Decimal("1"), fra_cat_id="cat_001",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )
    FundraisingActivity.create_fundraising_activity(
        title="B", description="d", target_amount=Decimal("1"),
        fra_cat_id=medical_cat.fra_cat_id,
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=owner.account_id,
    )
    FundraisingActivity.create_fundraising_activity(
        title="C", description="d", target_amount=Decimal("1"),
        fra_cat_id="cat_001",
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


def test_search_fundraising_activity_hides_suspended_from_donees() -> None:
    """Negative path of the donee-visible rule: search results skip
    suspended activities even when the title matches."""
    owner = _seed_fundraiser_account()
    visible = _seed_activity(owner, title="School fund")
    hidden = _seed_activity(owner, title="Hidden school fund")
    FundraisingActivity.suspend_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=hidden.fra_id,
    )

    results = FundraisingActivity.search_fundraising_activity("school")

    assert [a.fra_id for a in results] == [visible.fra_id]
    # Owner-scoped search still returns the suspended one.
    mine = FundraisingActivity.search_my_fundraising_activity(
        owner_account_id=owner.account_id, search_criteria="school",
    )
    assert {a.fra_id for a in mine} == {visible.fra_id, hidden.fra_id}


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

    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=owner.profile_id,
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

    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=owner.profile_id,
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
    """Seeds a *completed* activity by setting `end_date` in the past — the
    derived `completed` property flips to True automatically. No direct
    update call needed any more."""
    return FundraisingActivity.create_fundraising_activity(
        title=title, description=f"{title} desc",
        target_amount=Decimal("100"), fra_cat_id="cat_001",
        start_date=date(2025, 1, 1), end_date=date(2025, 6, 1),
        owner_account_id=owner.account_id,
    )


def test_search_my_completed_fundraising_activity_matches_only_completed_and_owner_scoped() -> None:
    owner = _seed_fundraiser_account()
    completed = _seed_completed_activity(owner, title="Hospital fund")
    ongoing = _seed_activity(owner, title="Hospital research")  # NOT completed
    assert ongoing.completed is False
    assert completed.fra_id != ongoing.fra_id

    results = FundraisingActivity.search_my_completed_fundraising_activity(
        owner_account_id=owner.account_id, search_criteria="hospital",
    )

    assert [a.fra_id for a in results] == [completed.fra_id]


def test_search_my_completed_fundraising_activity_excludes_other_owners_completed_activities() -> None:
    owner = _seed_fundraiser_account()
    _seed_completed_activity(owner, title="Mine done")

    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=owner.profile_id,
    )
    _seed_completed_activity(other, title="Theirs done")

    results = FundraisingActivity.search_my_completed_fundraising_activity(
        owner_account_id=owner.account_id, search_criteria="done",
    )
    assert [a.title for a in results] == ["Mine done"]


def test_search_my_completed_fundraising_activity_returns_empty_for_no_matches() -> None:
    """Negative path: owner has no completed activities → []."""
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Still going")  # not completed

    assert (
        FundraisingActivity.search_my_completed_fundraising_activity(
            owner_account_id=owner.account_id, search_criteria="going"
        )
        == []
    )


def test_view_my_completed_fundraising_activities_returns_only_completed_for_owner() -> None:
    owner = _seed_fundraiser_account()
    completed_a = _seed_completed_activity(owner, title="Hospital fund")
    completed_b = _seed_completed_activity(owner, title="School fund")
    _seed_activity(owner, title="Ongoing thing")  # not completed

    results = FundraisingActivity.view_my_completed_fundraising_activities(
        owner_account_id=owner.account_id,
    )

    titles = {a.title for a in results}
    assert titles == {"Hospital fund", "School fund"}
    assert all(a.completed for a in results)
    assert {completed_a.fra_id, completed_b.fra_id} == {a.fra_id for a in results}


def test_view_my_completed_fundraising_activities_excludes_other_owners() -> None:
    owner = _seed_fundraiser_account()
    _seed_completed_activity(owner, title="Mine")

    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=owner.profile_id,
    )
    _seed_completed_activity(other, title="Theirs")

    mine = FundraisingActivity.view_my_completed_fundraising_activities(
        owner_account_id=owner.account_id,
    )
    assert {a.title for a in mine} == {"Mine"}


def test_view_my_completed_fundraising_activities_returns_empty_for_no_completed() -> None:
    owner = _seed_fundraiser_account()
    _seed_activity(owner, title="Ongoing only")  # not completed

    assert (
        FundraisingActivity.view_my_completed_fundraising_activities(
            owner_account_id=owner.account_id,
        )
        == []
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


def test_view_fundraising_activity_save_count_returns_zero_for_missing_id() -> None:
    """Negative path: missing row returns 0 rather than raising (so the
    UI can always render a number)."""
    assert (
        FundraisingActivity.view_fundraising_activity_save_count("fra_999")
        == 0
    )


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


def test_increment_save_count_returns_false_for_missing_id() -> None:
    """Negative path: no row matches."""
    assert FundraisingActivity.increment_save_count("fra_999", +1) is False
