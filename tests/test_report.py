"""Tests for the Report entity (US-41 / US-42 / US-43).

Diagram contracts:
    US-41: generateDailyReport(startDate: Date, endDate: Date): Report
    US-42: generateWeeklyReport(startDate: Date, endDate: Date): Report
    US-43: generateMonthlyReport(startDate: Date, endDate: Date): Report

Implementation adds `platform_manager_id` as a 3rd param so the column
gets populated (typo logged).
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
    TC_PM_EMAIL,
    TC_PM_PHONE,
)
from entity.donation import Donation
from entity.fundraising_activity import FundraisingActivity
from entity.report import Report
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_pm() -> UserAccount:
    profile = UserProfile.create_profile(
        role="platform_manager", description="PM"
    )
    return UserAccount.create_account(
        email=TC_PM_EMAIL, password=DEFAULT_PASSWORD, name="TC - Platform Manager",
        dob=date(2000, 1, 1), phone_num=TC_PM_PHONE,
        profile_id=profile.profile_id,
    )


def _seed_fundraiser() -> UserAccount:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    return UserAccount.create_account(
        email=TC_FUNDRAISER_EMAIL, password=DEFAULT_PASSWORD, name="TC - Fundraiser",
        dob=date(2000, 1, 1), phone_num=TC_FUNDRAISER_PHONE,
        profile_id=profile.profile_id,
    )


def _seed_donee() -> UserAccount:
    profile = UserProfile.create_profile(role="donee", description="d")
    return UserAccount.create_account(
        email=TC_DONEE_EMAIL, password=DEFAULT_PASSWORD, name="TC - Donee",
        dob=date(2000, 1, 1), phone_num=TC_DONEE_PHONE,
        profile_id=profile.profile_id,
    )


def test_generate_daily_report_persists_with_prefixed_id_and_correct_type() -> None:
    pm = _seed_pm()

    report = Report.generate_daily_report(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 1),
        platform_manager_id=pm.account_id,
    )

    assert report.report_id == "rep_001"
    assert report.report_type == "daily"
    assert report.start_date == date(2026, 1, 1)
    assert report.end_date == date(2026, 1, 1)
    assert report.platform_manager_id == pm.account_id


def test_generate_weekly_report_records_correct_type() -> None:
    pm = _seed_pm()
    report = Report.generate_weekly_report(
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 7),
        platform_manager_id=pm.account_id,
    )
    assert report.report_type == "weekly"


def test_generate_weekly_report_zero_amount_when_no_donations() -> None:
    """Negative path: empty week aggregates to zero, mirroring the daily case."""
    pm = _seed_pm()
    report = Report.generate_weekly_report(
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 7),
        platform_manager_id=pm.account_id,
    )
    assert report.total_donation_amount == Decimal("0.00")
    assert report.total_donation_count == 0


def test_generate_monthly_report_records_correct_type() -> None:
    pm = _seed_pm()
    report = Report.generate_monthly_report(
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 31),
        platform_manager_id=pm.account_id,
    )
    assert report.report_type == "monthly"


def test_generate_monthly_report_zero_amount_when_no_donations() -> None:
    """Negative path: empty month aggregates to zero, mirroring the daily case."""
    pm = _seed_pm()
    report = Report.generate_monthly_report(
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 31),
        platform_manager_id=pm.account_id,
    )
    assert report.total_donation_amount == Decimal("0.00")
    assert report.total_donation_count == 0


def test_generate_report_aggregates_donations_in_window() -> None:
    pm = _seed_pm()
    donee = _seed_donee()
    fr = _seed_fundraiser()
    activity = FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=fr.account_id,
    )
    # In-window donations
    Donation.create_donation(
        account_id=donee.account_id, fra_id=activity.fra_id,
        amount=Decimal("50.00"), donation_date=date(2026, 1, 5),
    )
    Donation.create_donation(
        account_id=donee.account_id, fra_id=activity.fra_id,
        amount=Decimal("25.00"), donation_date=date(2026, 1, 6),
    )
    # Out-of-window donation — must be excluded
    Donation.create_donation(
        account_id=donee.account_id, fra_id=activity.fra_id,
        amount=Decimal("99.99"), donation_date=date(2025, 12, 31),
    )

    report = Report.generate_daily_report(
        start_date=date(2026, 1, 5), end_date=date(2026, 1, 6),
        platform_manager_id=pm.account_id,
    )

    assert report.total_donation_amount == Decimal("75.00")
    assert report.total_donation_count == 2


def test_generate_report_counts_users_and_activities() -> None:
    pm = _seed_pm()
    _seed_fundraiser()
    _seed_donee()

    report = Report.generate_daily_report(
        start_date=date(2026, 1, 1), end_date=date(2026, 12, 31),
        platform_manager_id=pm.account_id,
    )

    assert report.total_activity_count == 0  # no activities seeded yet
    assert report.total_fundraiser_count == 1
    assert report.total_donee_count == 1


def test_generate_report_raises_on_nonexistent_platform_manager() -> None:
    """Negative path: FK violation on platform_manager_id."""
    import sqlite3

    with pytest.raises(sqlite3.IntegrityError):
        Report.generate_daily_report(
            start_date=date(2026, 1, 1), end_date=date(2026, 1, 1),
            platform_manager_id="acc_999",
        )


def test_generate_report_zero_amount_when_no_donations() -> None:
    """Negative path: empty result window returns 0 / 0.00."""
    pm = _seed_pm()
    report = Report.generate_daily_report(
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 1),
        platform_manager_id=pm.account_id,
    )
    assert report.total_donation_amount == Decimal("0")
    assert report.total_donation_count == 0
