"""GenerateMonthlyReportController <<Controller>> — pure delegator, US-43."""
from __future__ import annotations

from typing import Optional

from entity.report import Report


class GenerateMonthlyReportController:
    def generate_monthly_report(
        self, start_date: str, end_date: str, platform_manager_id: Optional[int]
    ) -> Report:
        return Report.generate_monthly_report(start_date, end_date, platform_manager_id)
