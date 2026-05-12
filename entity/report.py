"""Report <<Entity>> — Sprint 4 (US-41 daily, US-42 weekly, US-43 monthly).

Each generate-call INSERTs a row into the `report` table and returns the
Report with the real `report_id` from the insert. This makes `reportId`
meaningful (matches the Sprint 4 class diagram, which declares it as a
field). No "view past reports" use case has been drawn yet — past rows
are inspectable through the debug page.

Scoping notes:
- `totalDonationAmount` / `totalDonationCount` are always zero because no
  donation use case exists yet (US-32/33 still deferred). Surfaced clearly
  in the boundary pages.
- `totalActivityCount` counts activities whose `start_date` falls in
  [start_date, end_date]. Fundraiser/donee counts are platform-wide totals
  because account creation time is not tracked. Diagram silent on the
  semantics; choice logged in docs/todo.md.
- `platform_manager_id` is the `user_account.account_id` of the logged-in
  PM (per Sprint 1 US-39: PMs authenticate via `UserAccount.login`).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from persistence.db import get_connection


@dataclass
class Report:
    report_type: str
    start_date: str
    end_date: str
    total_donation_amount: float = 0.0
    total_donation_count: int = 0
    total_activity_count: int = 0
    total_fundraiser_count: int = 0
    total_donee_count: int = 0
    platform_manager_id: Optional[int] = None
    report_id: int = 0
    generated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def generate_daily_report(
        cls, start_date: str, end_date: str, platform_manager_id: Optional[int]
    ) -> "Report":
        return cls._generate("daily", start_date, end_date, platform_manager_id)

    @classmethod
    def generate_weekly_report(
        cls, start_date: str, end_date: str, platform_manager_id: Optional[int]
    ) -> "Report":
        return cls._generate("weekly", start_date, end_date, platform_manager_id)

    @classmethod
    def generate_monthly_report(
        cls, start_date: str, end_date: str, platform_manager_id: Optional[int]
    ) -> "Report":
        return cls._generate("monthly", start_date, end_date, platform_manager_id)

    @classmethod
    def _generate(
        cls,
        report_type: str,
        start_date: str,
        end_date: str,
        platform_manager_id: Optional[int],
    ) -> "Report":
        generated_at = datetime.now()
        with get_connection() as conn:
            activity_count = conn.execute(
                "SELECT COUNT(*) AS c FROM fundraising_activity "
                "WHERE start_date BETWEEN ? AND ?",
                (start_date, end_date),
            ).fetchone()["c"]
            fundraiser_count = conn.execute(
                "SELECT COUNT(*) AS c FROM user_account ua "
                "JOIN user_profile up ON ua.profile_id = up.profile_id "
                "WHERE up.role = 'fundraiser'"
            ).fetchone()["c"]
            donee_count = conn.execute(
                "SELECT COUNT(*) AS c FROM user_account ua "
                "JOIN user_profile up ON ua.profile_id = up.profile_id "
                "WHERE up.role = 'donee'"
            ).fetchone()["c"]
            cursor = conn.execute(
                "INSERT INTO report (report_type, start_date, end_date, "
                "generated_at, platform_manager_id, total_donation_amount, "
                "total_donation_count, total_activity_count, "
                "total_fundraiser_count, total_donee_count) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    report_type,
                    start_date,
                    end_date,
                    generated_at.isoformat(),
                    platform_manager_id,
                    0.0,
                    0,
                    int(activity_count),
                    int(fundraiser_count),
                    int(donee_count),
                ),
            )
            report_id = cursor.lastrowid

        return cls(
            report_id=report_id,
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            generated_at=generated_at,
            total_donation_amount=0.0,
            total_donation_count=0,
            total_activity_count=int(activity_count),
            total_fundraiser_count=int(fundraiser_count),
            total_donee_count=int(donee_count),
            platform_manager_id=platform_manager_id,
        )
