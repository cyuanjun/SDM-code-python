"""Report <<Entity>> — Sprint 4 US-41 / US-42 / US-43.

Diagram contracts:
    US-41: + generateDailyReport(startDate: Date, endDate: Date): Report
    US-42: + generateWeeklyReport(startDate: Date, endDate: Date): Report
    US-43: + generateMonthlyReport(startDate: Date, endDate: Date): Report

Implementation adds `platform_manager_id` as a 3rd parameter — the entity
declares `platformManagerId: String` as an attribute, but the method
signatures don't accept it. Logged in docs/diagram_typos.md.

Each `generate_*` method inserts a `report` row capturing aggregate
statistics over the [start_date, end_date] window and returns the
persisted Report.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from persistence.db import get_connection
from persistence.ids import format_id, parse_id


@dataclass
class Report:
    report_type: str
    start_date: date
    end_date: date
    generated_at: datetime
    platform_manager_id: str
    total_donation_amount: Decimal = Decimal("0")
    total_donation_count: int = 0
    total_activity_count: int = 0
    total_fundraiser_count: int = 0
    total_donee_count: int = 0
    report_id: Optional[str] = None

    @classmethod
    def generate_daily_report(
        cls, start_date: date, end_date: date, platform_manager_id: str
    ) -> "Report":
        return cls._generate(
            "daily", start_date, end_date, platform_manager_id
        )

    @classmethod
    def generate_weekly_report(
        cls, start_date: date, end_date: date, platform_manager_id: str
    ) -> "Report":
        return cls._generate(
            "weekly", start_date, end_date, platform_manager_id
        )

    @classmethod
    def generate_monthly_report(
        cls, start_date: date, end_date: date, platform_manager_id: str
    ) -> "Report":
        return cls._generate(
            "monthly", start_date, end_date, platform_manager_id
        )

    @classmethod
    def _generate(
        cls,
        report_type: str,
        start_date: date,
        end_date: date,
        platform_manager_id: str,
    ) -> "Report":
        pm_rowid = parse_id(platform_manager_id)
        stats = cls._aggregate_stats(start_date, end_date)
        generated_at = datetime.now()

        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO report ("
                "  report_type, start_date, end_date, generated_at, "
                "  platform_manager_id, total_donation_amount, "
                "  total_donation_count, total_activity_count, "
                "  total_fundraiser_count, total_donee_count"
                ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    report_type,
                    start_date.isoformat(),
                    end_date.isoformat(),
                    generated_at.isoformat(),
                    pm_rowid,
                    str(stats["total_donation_amount"]),
                    stats["total_donation_count"],
                    stats["total_activity_count"],
                    stats["total_fundraiser_count"],
                    stats["total_donee_count"],
                ),
            )
            rowid = cursor.lastrowid

        return cls(
            report_id=format_id("rep", rowid),
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            generated_at=generated_at,
            platform_manager_id=platform_manager_id,
            **stats,
        )

    @staticmethod
    def _aggregate_stats(start_date: date, end_date: date) -> dict:
        with get_connection() as conn:
            donation_row = conn.execute(
                "SELECT COUNT(*) AS n, COALESCE(SUM(CAST(amount AS REAL)), 0) AS total "
                "FROM donation WHERE donation_date BETWEEN ? AND ?",
                (start_date.isoformat(), end_date.isoformat()),
            ).fetchone()
            activity_row = conn.execute(
                "SELECT COUNT(*) AS n FROM fundraising_activity"
            ).fetchone()
            fundraiser_row = conn.execute(
                "SELECT COUNT(*) AS n FROM user_account a "
                "JOIN user_profile p ON p.profile_id = a.profile_id "
                "WHERE p.role = 'fundraiser'"
            ).fetchone()
            donee_row = conn.execute(
                "SELECT COUNT(*) AS n FROM user_account a "
                "JOIN user_profile p ON p.profile_id = a.profile_id "
                "WHERE p.role = 'donee'"
            ).fetchone()
        return {
            "total_donation_amount": Decimal(
                f"{donation_row['total']:.2f}"
            ),
            "total_donation_count": int(donation_row["n"]),
            "total_activity_count": int(activity_row["n"]),
            "total_fundraiser_count": int(fundraiser_row["n"]),
            "total_donee_count": int(donee_row["n"]),
        }
