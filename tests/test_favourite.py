"""Tests for the Favourite entity (US-22, US-24).

Diagram contracts:
    US-22.jpg: + saveFundraisingActivity(accountId: String, FRAId: String): Boolean
    US-24.jpg: + viewFavouriteList(accountId: String): List<Favourite>
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from entity.favourite import Favourite
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_donee() -> UserAccount:
    profile = UserProfile.create_profile(role="donee", description="r")
    return UserAccount.create_account(
        email="d@x.com", password="p", name="D", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )


_activity_counter = [0]


def _seed_fundraiser() -> UserAccount:
    """Idempotent: reuses the singleton fundraiser profile on subsequent
    calls (role is UNIQUE per the schema). Returns a new account each call
    via a different email."""
    _activity_counter[0] += 1
    n = _activity_counter[0]
    profiles = UserProfile.search_user_profile("fundraiser")
    profile = profiles[0] if profiles else UserProfile.create_profile(
        role="fundraiser", description="r",
    )
    return UserAccount.create_account(
        email=f"f{n}@x.com", password="p", name="F", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )


def _seed_activity() -> FundraisingActivity:
    fr = _seed_fundraiser()
    return FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100"),
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=fr.account_id,
    )


def test_save_fundraising_activity_returns_true_on_first_save() -> None:
    donee = _seed_donee()
    activity = _seed_activity()

    ok = Favourite.save_fundraising_activity(
        account_id=donee.account_id, fra_id=activity.fra_id
    )

    assert ok is True

    favourites = Favourite.view_favourite_list(donee.account_id)
    assert len(favourites) == 1
    assert favourites[0].account_id == donee.account_id
    assert favourites[0].fra_id == activity.fra_id


def test_save_fundraising_activity_returns_false_on_duplicate() -> None:
    """Negative path: composite PK (account_id, fra_id) — second save of
    the same pair returns False rather than raising."""
    donee = _seed_donee()
    activity = _seed_activity()

    first = Favourite.save_fundraising_activity(
        account_id=donee.account_id, fra_id=activity.fra_id
    )
    second = Favourite.save_fundraising_activity(
        account_id=donee.account_id, fra_id=activity.fra_id
    )

    assert first is True
    assert second is False


def test_save_fundraising_activity_raises_on_nonexistent_account() -> None:
    """Negative path: FK violation on account_id."""
    import sqlite3

    activity = _seed_activity()
    with pytest.raises(sqlite3.IntegrityError):
        Favourite.save_fundraising_activity(
            account_id="acc_999", fra_id=activity.fra_id
        )


def test_save_fundraising_activity_raises_on_nonexistent_activity() -> None:
    """Negative path: FK violation on fra_id."""
    import sqlite3

    donee = _seed_donee()
    with pytest.raises(sqlite3.IntegrityError):
        Favourite.save_fundraising_activity(
            account_id=donee.account_id, fra_id="fra_999"
        )


def test_view_favourite_list_returns_empty_list_when_donee_has_none() -> None:
    """Negative path: donee with no favourites gets [] back, not None."""
    donee = _seed_donee()

    assert Favourite.view_favourite_list(donee.account_id) == []


def test_view_favourite_list_scopes_to_the_account() -> None:
    """A second donee's favourites must not appear in the first donee's list."""
    first = _seed_donee()
    profile = UserProfile.view_user_profile(first.profile_id)
    assert profile is not None
    second = UserAccount.create_account(
        email="d2@x.com", password="p", name="D2",
        dob=date(1990, 1, 1), phone_num="0",
        profile_id=first.profile_id,
    )
    activity_a = _seed_activity()
    activity_b = _seed_activity()  # creates a new fundraiser + activity

    Favourite.save_fundraising_activity(
        account_id=first.account_id, fra_id=activity_a.fra_id
    )
    Favourite.save_fundraising_activity(
        account_id=second.account_id, fra_id=activity_b.fra_id
    )

    mine = Favourite.view_favourite_list(first.account_id)
    theirs = Favourite.view_favourite_list(second.account_id)

    assert [f.fra_id for f in mine] == [activity_a.fra_id]
    assert [f.fra_id for f in theirs] == [activity_b.fra_id]


def test_remove_favourite_returns_true_when_pair_exists() -> None:
    donee = _seed_donee()
    activity = _seed_activity()
    Favourite.save_fundraising_activity(
        account_id=donee.account_id, fra_id=activity.fra_id
    )

    ok = Favourite.remove_favourite(
        fra_id=activity.fra_id, account_id=donee.account_id
    )
    assert ok is True
    assert Favourite.view_favourite_list(donee.account_id) == []


def test_remove_favourite_returns_false_when_pair_missing() -> None:
    """Negative path: removing a (account, activity) pair that was never
    favourited returns False."""
    donee = _seed_donee()
    activity = _seed_activity()

    assert (
        Favourite.remove_favourite(
            fra_id=activity.fra_id, account_id=donee.account_id
        )
        is False
    )


def test_remove_favourite_is_scoped_to_the_account() -> None:
    """Negative path: removing donee A's favourite via donee B's id leaves
    A's row untouched."""
    donee_a = _seed_donee()
    donee_b = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1990, 1, 1),
        phone_num="0", profile_id=donee_a.profile_id,
    )
    activity = _seed_activity()
    Favourite.save_fundraising_activity(
        account_id=donee_a.account_id, fra_id=activity.fra_id
    )

    ok = Favourite.remove_favourite(
        fra_id=activity.fra_id, account_id=donee_b.account_id
    )
    assert ok is False
    assert len(Favourite.view_favourite_list(donee_a.account_id)) == 1


def test_search_favourite_matches_activity_fields_for_the_donee() -> None:
    """Search returns the donee's favourites whose underlying activity
    matches the criteria (title / description / category)."""
    donee = _seed_donee()
    # Seed three activities and favourite two of them.
    fr = _seed_fundraiser()
    a1 = FundraisingActivity.create_fundraising_activity(
        title="Hospital fund", description="d",
        target_amount=Decimal("1"), category="health",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=fr.account_id,
    )
    a2 = FundraisingActivity.create_fundraising_activity(
        title="School fundraiser", description="d",
        target_amount=Decimal("1"), category="education",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=fr.account_id,
    )
    a3 = FundraisingActivity.create_fundraising_activity(
        title="Animal rescue", description="d",
        target_amount=Decimal("1"), category="animals",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=fr.account_id,
    )

    Favourite.save_fundraising_activity(donee.account_id, a1.fra_id)
    Favourite.save_fundraising_activity(donee.account_id, a2.fra_id)
    # a3 is not favourited.

    results = Favourite.search_favourite(
        account_id=donee.account_id, search_criteria="hospital"
    )
    assert [f.fra_id for f in results] == [a1.fra_id]


def test_search_favourite_returns_empty_for_no_match() -> None:
    donee = _seed_donee()
    activity = _seed_activity()
    Favourite.save_fundraising_activity(
        donee.account_id, activity.fra_id
    )

    assert (
        Favourite.search_favourite(
            account_id=donee.account_id, search_criteria="nothing"
        )
        == []
    )


def test_search_favourite_returns_empty_for_no_favourites() -> None:
    """Negative path: donee with no favourites gets [] regardless of criteria."""
    donee = _seed_donee()
    assert (
        Favourite.search_favourite(
            account_id=donee.account_id, search_criteria="anything"
        )
        == []
    )
