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

from data.seed import (
    DEFAULT_PASSWORD,
    TC_DONEE_EMAIL,
    TC_DONEE_PHONE,
    TC_FUNDRAISER_EMAIL,
    TC_FUNDRAISER_PHONE,
)
from entity.donation import Donation
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_donee_and_activity() -> tuple[UserAccount, FundraisingActivity]:
    donee_profile = UserProfile.create_profile(role="donee", description="r")
    donee = UserAccount.create_account(
        email=TC_DONEE_EMAIL, password=DEFAULT_PASSWORD, name="TC - Donee",
        dob=date(2000, 1, 1), phone_num=TC_DONEE_PHONE,
        profile_id=donee_profile.profile_id,
    )
    fr_profile = UserProfile.create_profile(role="fundraiser", description="r")
    fr = UserAccount.create_account(
        email=TC_FUNDRAISER_EMAIL, password=DEFAULT_PASSWORD, name="TC - Fundraiser",
        dob=date(2000, 1, 1), phone_num=TC_FUNDRAISER_PHONE,
        profile_id=fr_profile.profile_id,
    )
    activity = FundraisingActivity.create_fundraising_activity(
        title="TC - Active hospital fund", description="medical aid",
        target_amount=Decimal("1000"), fra_cat_id="cat_001",
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


def test_search_my_donation_history_matches_activity_fields_for_the_donee() -> None:
    donee, hospital = _seed_donee_and_activity()
    # Create a second activity with a different title, owned by the same
    # fundraiser (the singleton fundraiser profile rules out a second one).
    school = FundraisingActivity.create_fundraising_activity(
        title="TC - Completed school fund", description="education",
        target_amount=Decimal("100"), fra_cat_id="cat_001",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=hospital.owner_account_id,
    )
    _seed_donation(donee, hospital, amount="100.00")
    _seed_donation(donee, school, amount="200.00")

    results = Donation.search_my_donation_history(
        account_id=donee.account_id, search_criteria="hospital"
    )
    assert [d.fra_id for d in results] == [hospital.fra_id]


def test_search_my_donation_history_returns_empty_for_no_match() -> None:
    donee, activity = _seed_donee_and_activity()
    _seed_donation(donee, activity)

    assert (
        Donation.search_my_donation_history(
            account_id=donee.account_id, search_criteria="nothing"
        )
        == []
    )


def test_search_my_donation_history_returns_empty_for_no_donations() -> None:
    donee, _ = _seed_donee_and_activity()
    assert (
        Donation.search_my_donation_history(
            account_id=donee.account_id, search_criteria="anything"
        )
        == []
    )


def test_view_my_donation_histories_returns_list_for_the_donee() -> None:
    donee, activity = _seed_donee_and_activity()
    a = _seed_donation(donee, activity, amount="75.50")
    b = _seed_donation(donee, activity, amount="20.00")

    results = Donation.view_my_donation_histories(account_id=donee.account_id)

    assert {d.donation_id for d in results} == {a.donation_id, b.donation_id}


def test_view_my_donation_histories_excludes_other_donees() -> None:
    """Negative path: donee A's donations don't appear in donee B's list."""
    donee_a, activity = _seed_donee_and_activity()
    _seed_donation(donee_a, activity)

    donee_b = UserAccount.create_account(
        email="other-d@a.com", password=DEFAULT_PASSWORD, name="Other Donee",
        dob=date(2000, 1, 1), phone_num="0411111111",
        profile_id=donee_a.profile_id,
    )

    assert (
        Donation.view_my_donation_histories(account_id=donee_b.account_id)
        == []
    )


def test_view_my_donation_histories_returns_empty_list_for_no_donations() -> None:
    """Negative path: donee with no donations gets []."""
    donee, _ = _seed_donee_and_activity()
    assert (
        Donation.view_my_donation_histories(account_id=donee.account_id)
        == []
    )