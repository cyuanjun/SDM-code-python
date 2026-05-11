"""Sprint 4 — Report entity tests (US-41 daily, US-42 weekly, US-43 monthly).

Scoping decisions (see docs/issues.md):
- Reports are generated on the fly with no `report` table — `reportId` is 0
  and `generatedAt` is set at call time.
- `totalDonationAmount` / `totalDonationCount` are always 0 because donations
  are not implemented in the system (US-32/33 remain deferred).
- `totalActivityCount` counts activities whose `start_date` falls within
  [start_date, end_date]. Fundraiser/donee counts are platform-wide totals
  because account creation time is not tracked.
"""
from entity.fundraising_activity import FundraisingActivity
from entity.platform_manager import PlatformManager
from entity.report import Report
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _make_activity(start: str, end: str = "2026-12-31") -> None:
    FundraisingActivity(
        title="t", description="d", target_amount=100.0, category="x",
        start_date=start, end_date=end, status="active",
    ).save_fundraising_activity()


def _make_account(role: str, email: str) -> None:
    profile = UserProfile.create_profile(role, "test")
    UserAccount.create_account(
        email, "pw", "N", "1990-01-01", "1", profile.profile_id
    )


def test_generate_daily_report_returns_report_with_period():
    PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "PM")
    report = Report.generate_daily_report("2026-05-01", "2026-05-01")
    assert report.report_type == "daily"
    assert report.start_date == "2026-05-01"
    assert report.end_date == "2026-05-01"
    assert report.generated_at is not None


def test_generate_weekly_report_sets_report_type():
    PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "PM")
    report = Report.generate_weekly_report("2026-05-01", "2026-05-07")
    assert report.report_type == "weekly"


def test_generate_monthly_report_sets_report_type():
    PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "PM")
    report = Report.generate_monthly_report("2026-05-01", "2026-05-31")
    assert report.report_type == "monthly"


def test_report_counts_activities_started_in_window():
    PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "PM")
    _make_activity("2026-04-30")  # before window
    _make_activity("2026-05-01")  # in window
    _make_activity("2026-05-15")  # in window
    _make_activity("2026-06-01")  # after window
    report = Report.generate_monthly_report("2026-05-01", "2026-05-31")
    assert report.total_activity_count == 2


def test_report_counts_fundraisers_and_donees():
    PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "PM")
    _make_account("fundraiser", "f1@x.com")
    _make_account("fundraiser", "f2@x.com")
    _make_account("donee", "d1@x.com")
    report = Report.generate_daily_report("2026-05-01", "2026-05-01")
    assert report.total_fundraiser_count == 2
    assert report.total_donee_count == 1


def test_report_donation_totals_are_zero_when_no_donations_table():
    PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "PM")
    report = Report.generate_daily_report("2026-05-01", "2026-05-01")
    assert report.total_donation_amount == 0.0
    assert report.total_donation_count == 0


def test_report_uses_first_platform_manager_id():
    pm = PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "PM")
    PlatformManager.create_platform_manager("pm2", "pw", "pm2@x.com", "PM Two")
    report = Report.generate_daily_report("2026-05-01", "2026-05-01")
    assert report.platform_manager_id == pm.platform_manager_id


def test_report_platform_manager_id_is_none_when_no_pm_seeded():
    """No PM rows -> the entity falls back to None rather than crashing."""
    report = Report.generate_daily_report("2026-05-01", "2026-05-01")
    assert report.platform_manager_id is None
