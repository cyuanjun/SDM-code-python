"""Report <<Entity>> — Sprint 4 (US-41 daily, US-42 weekly, US-43 monthly).

Reports are generated on the fly: no `report` table exists, `reportId` is
left at 0, and `generatedAt` is set to `datetime.now()` at call time. See
docs/issues.md "Reports are generated on the fly with no `report` table"
for the open question.

Scoping notes:
- `totalDonationAmount` / `totalDonationCount` are always zero because no
  donation use case exists yet (US-32/33 still deferred). Surfaced clearly
  in the boundary pages.
- `totalActivityCount` counts activities whose `start_date` falls in
  [start_date, end_date]. Fundraiser/donee counts are platform-wide totals
  because account creation time is not tracked. Diagram silent on the
  semantics; choice logged in docs/todo.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from entity.platform_manager import PlatformManager
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
    def generate_daily_report(cls, start_date: str, end_date: str) -> "Report":
        return cls._generate("daily", start_date, end_date)

    @classmethod
    def generate_weekly_report(cls, start_date: str, end_date: str) -> "Report":
        return cls._generate("weekly", start_date, end_date)

    @classmethod
    def generate_monthly_report(cls, start_date: str, end_date: str) -> "Report":
        return cls._generate("monthly", start_date, end_date)

    @classmethod
    def _generate(cls, report_type: str, start_date: str, end_date: str) -> "Report":
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

        pms = PlatformManager.view_all_platform_managers()
        platform_manager_id = pms[0].platform_manager_id if pms else None

        return cls(
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            total_donation_amount=0.0,
            total_donation_count=0,
            total_activity_count=int(activity_count),
            total_fundraiser_count=int(fundraiser_count),
            total_donee_count=int(donee_count),
            platform_manager_id=platform_manager_id,
        )
