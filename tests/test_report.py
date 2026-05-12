"""Sprint 4 — Report entity tests (US-41 daily, US-42 weekly, US-43 monthly).

Scoping decisions (see docs/issues.md):
- Reports are persisted on every generate: `_generate` INSERTs into the
  `report` table and returns the Report with the real (non-zero) id.
- `totalDonationAmount` / `totalDonationCount` are always 0 because donations
  are not implemented in the system (US-32/33 remain deferred).
- `totalActivityCount` counts activities whose `start_date` falls within
  [start_date, end_date]. Fundraiser/donee counts are platform-wide totals
  because account creation time is not tracked.
- `platform_manager_id` is the logged-in PM's `user_account.account_id`
  (Sprint 1 US-39: PMs authenticate via `UserAccount.login`). The entity
  stores whatever the boundary passes in.
"""
from entity.fundraising_activity import FundraisingActivity
from entity.report import Report
from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from persistence.db import get_connection


def _make_activity(start: str, end: str = "2026-12-31") -> None:
    FundraisingActivity(
        title="t", description="d", target_amount=100.0, category="x",
        start_date=start, end_date=end, status="active",
    ).save_fundraising_activity()


def _make_account(role: str, email: str) -> int:
    profile = UserProfile.create_profile(role, "test")
    account = UserAccount.create_account(
        email, "pw", "N", "1990-01-01", "1", profile.profile_id
    )
    return account.account_id


def test_generate_daily_report_returns_report_with_period():
    report = Report.generate_daily_report("2026-05-01", "2026-05-01", None)
    assert report.report_type == "daily"
    assert report.start_date == "2026-05-01"
    assert report.end_date == "2026-05-01"
    assert report.generated_at is not None


def test_generate_weekly_report_sets_report_type():
    report = Report.generate_weekly_report("2026-05-01", "2026-05-07", None)
    assert report.report_type == "weekly"


def test_generate_monthly_report_sets_report_type():
    report = Report.generate_monthly_report("2026-05-01", "2026-05-31", None)
    assert report.report_type == "monthly"


def test_report_counts_activities_started_in_window():
    _make_activity("2026-04-30")  # before window
    _make_activity("2026-05-01")  # in window
    _make_activity("2026-05-15")  # in window
    _make_activity("2026-06-01")  # after window
    report = Report.generate_monthly_report("2026-05-01", "2026-05-31", None)
    assert report.total_activity_count == 2


def test_report_counts_fundraisers_and_donees():
    _make_account("fundraiser", "f1@x.com")
    _make_account("fundraiser", "f2@x.com")
    _make_account("donee", "d1@x.com")
    report = Report.generate_daily_report("2026-05-01", "2026-05-01", None)
    assert report.total_fundraiser_count == 2
    assert report.total_donee_count == 1


def test_report_donation_totals_are_zero_when_no_donations_table():
    report = Report.generate_daily_report("2026-05-01", "2026-05-01", None)
    assert report.total_donation_amount == 0.0
    assert report.total_donation_count == 0


def test_report_stores_passed_platform_manager_id():
    pm_account_id = _make_account("platform_manager", "pm@x.com")
    report = Report.generate_daily_report("2026-05-01", "2026-05-01", pm_account_id)
    assert report.platform_manager_id == pm_account_id


def test_report_accepts_none_platform_manager_id():
    """No logged-in PM -> the entity stores None rather than fabricating one."""
    report = Report.generate_daily_report("2026-05-01", "2026-05-01", None)
    assert report.platform_manager_id is None


def test_report_is_persisted_with_real_id():
    """Every generate writes a row and the returned Report carries the real PK."""
    report = Report.generate_daily_report("2026-05-01", "2026-05-01", None)
    assert report.report_id > 0

    with get_connection() as conn:
        row = conn.execute(
            "SELECT report_type, start_date, end_date, generated_at FROM report "
            "WHERE report_id = ?",
            (report.report_id,),
        ).fetchone()
    assert row is not None
    assert row["report_type"] == "daily"
    assert row["start_date"] == "2026-05-01"
    assert row["generated_at"] == report.generated_at.isoformat()


def test_each_generate_creates_a_new_row():
    Report.generate_daily_report("2026-05-01", "2026-05-01", None)
    Report.generate_weekly_report("2026-05-01", "2026-05-07", None)
    Report.generate_monthly_report("2026-05-01", "2026-05-31", None)
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM report").fetchone()["c"]
    assert count == 3
