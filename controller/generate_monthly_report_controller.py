"""GenerateMonthlyReportController <<Controller>> — pure delegator, US-43."""
from __future__ import annotations

from entity.report import Report


class GenerateMonthlyReportController:
    def generate_monthly_report(self, start_date: str, end_date: str) -> Report:
        return Report.generate_monthly_report(start_date, end_date)
