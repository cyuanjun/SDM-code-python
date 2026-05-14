"""Tests for the Favourite entity (US-22, US-24).

Diagram contracts:
    US-22.jpg: + saveFundraisingActivity(accountId: String, FRAId: String): Boolean
    US-24.jpg: + viewFavourites(accountId: String): List<Favourite>
               (diagram shows `viewFavourite(...): Favourite` — typo logged
               in docs/todo.md; the user story is "view ALL my favourites".)
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


def _seed_activity() -> FundraisingActivity:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    fr = UserAccount.create_account(
        email="f@x.com", password="p", name="F", dob=date(1990, 1, 1),
        phone_num="0", profile_id=profile.profile_id,
    )
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

    favourites = Favourite.view_favourites(donee.account_id)
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


def test_view_favourites_returns_empty_list_when_donee_has_none() -> None:
    """Negative path: donee with no favourites gets [] back, not None."""
    donee = _seed_donee()

    assert Favourite.view_favourites(donee.account_id) == []


def test_view_favourites_scopes_to_the_account() -> None:
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

    mine = Favourite.view_favourites(first.account_id)
    theirs = Favourite.view_favourites(second.account_id)

    assert [f.fra_id for f in mine] == [activity_a.fra_id]
    assert [f.fra_id for f in theirs] == [activity_b.fra_id]
