"""GenerateDailyReportController <<Controller>> — pure delegator, US-41."""
from __future__ import annotations

from entity.report import Report


class GenerateDailyReportController:
    def generate_daily_report(self, start_date: str, end_date: str) -> Report:
        return Report.generate_daily_report(start_date, end_date)
