"""GenerateWeeklyReportController <<Controller>> — pure delegator, US-42."""
from __future__ import annotations

from entity.report import Report


class GenerateWeeklyReportController:
    def generate_weekly_report(self, start_date: str, end_date: str) -> Report:
        return Report.generate_weekly_report(start_date, end_date)
