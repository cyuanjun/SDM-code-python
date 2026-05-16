"""Tests for the Donation entity (US-32, US-33).

Diagram contracts:
    US-32.jpg: + searchDonationHistory(searchCriteria: String, accountId: String): List<Donation>
               (class diagram types accountId as Integer — typo logged in
               docs/todo.md; implementation uses String.)
    US-33.jpg: + viewMyDonationHistory(accountId: String, donationId: String): Donation
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from entity.donation import Donation
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_donee_and_activity() -> tuple[UserAccount, FundraisingActivity]:
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
        title="Hospital fund", description="medical aid",
        target_amount=Decimal("1000"), category="health",
        start_date=date(2026, 1, 1), end_date=date(2026, 6, 1),
        owner_account_id=fr.account_id,
    )
    return donee, activity


def _seed_donation(
    donee: UserAccount, activity: FundraisingActivity,
    amount: str = "100.00", donation_date: date = date(2026, 3, 15),
) -> Donation:
    return Donation.create_donation(
        account_id=donee.account_id,
        fra_id=activity.fra_id,
        amount=Decimal(amount),
        donation_date=donation_date,
    )


def test_create_donation_persists_and_returns_with_prefixed_id() -> None:
    donee, activity = _seed_donee_and_activity()

    donation = _seed_donation(donee, activity)

    assert donation.donation_id == "don_001"
    assert donation.account_id == donee.account_id
    assert donation.fra_id == activity.fra_id
    assert donation.amount == Decimal("100.00")
    assert donation.donation_date == date(2026, 3, 15)


def test_create_donation_raises_on_unknown_account_id() -> None:
    """Negative path: FK violation on account_id."""
    import sqlite3

    _, activity = _seed_donee_and_activity()
    with pytest.raises(sqlite3.IntegrityError):
        Donation.create_donation(
            account_id="acc_999", fra_id=activity.fra_id,
            amount=Decimal("1"), donation_date=date(2026, 1, 1),
        )


def test_create_donation_raises_on_unknown_fra_id() -> None:
    """Negative path: FK violation on fra_id."""
    import sqlite3

    donee, _ = _seed_donee_and_activity()
    with pytest.raises(sqlite3.IntegrityError):
        Donation.create_donation(
            account_id=donee.account_id, fra_id="fra_999",
            amount=Decimal("1"), donation_date=date(2026, 1, 1),
        )


def test_search_donation_history_matches_activity_fields_for_the_donee() -> None:
    donee, hospital = _seed_donee_and_activity()
    # Create a second activity with a different title.
    fr_profile = UserProfile.create_profile(role="fundraiser", description="r")
    fr2 = UserAccount.create_account(
        email="f2@x.com", password="p", name="F2", dob=date(1990, 1, 1),
        phone_num="0", profile_id=fr_profile.profile_id,
    )
    school = FundraisingActivity.create_fundraising_activity(
        title="School fund", description="education",
        target_amount=Decimal("100"), category="education",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=fr2.account_id,
    )
    _seed_donation(donee, hospital, amount="50")
    _seed_donation(donee, school, amount="20")

    results = Donation.search_donation_history(
        account_id=donee.account_id, search_criteria="school"
    )
    assert [d.fra_id for d in results] == [school.fra_id]


def test_search_donation_history_returns_empty_for_no_match() -> None:
    donee, activity = _seed_donee_and_activity()
    _seed_donation(donee, activity)

    assert (
        Donation.search_donation_history(
            account_id=donee.account_id, search_criteria="nothing"
        )
        == []
    )


def test_search_donation_history_returns_empty_for_no_donations() -> None:
    donee, _ = _seed_donee_and_activity()
    assert (
        Donation.search_donation_history(
            account_id=donee.account_id, search_criteria="anything"
        )
        == []
    )


def test_view_my_donation_history_returns_donation_for_correct_owner() -> None:
    donee, activity = _seed_donee_and_activity()
    created = _seed_donation(donee, activity, amount="75.50")

    fetched = Donation.view_my_donation_history(
        account_id=donee.account_id, donation_id=created.donation_id,
    )

    assert fetched is not None
    assert fetched.donation_id == created.donation_id
    assert fetched.amount == Decimal("75.50")


def test_view_my_donation_history_returns_none_for_wrong_owner() -> None:
    """Negative path: donee A's donation can't be fetched via donee B's id."""
    donee_a, activity = _seed_donee_and_activity()
    created = _seed_donation(donee_a, activity)

    donee_b = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1990, 1, 1),
        phone_num="0", profile_id=donee_a.profile_id,
    )

    fetched = Donation.view_my_donation_history(
        account_id=donee_b.account_id, donation_id=created.donation_id,
    )
    assert fetched is None


def test_view_my_donation_history_returns_none_for_missing_id() -> None:
    donee, _ = _seed_donee_and_activity()
    assert (
        Donation.view_my_donation_history(
            account_id=donee.account_id, donation_id="don_999"
        )
        is None
    )