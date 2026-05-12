"""GenerateWeeklyReportController <<Controller>> — pure delegator, US-42."""
from __future__ import annotations

from typing import Optional

from entity.report import Report


class GenerateWeeklyReportController:
    def generate_weekly_report(
        self, start_date: str, end_date: str, platform_manager_id: Optional[int]
    ) -> Report:
        return Report.generate_weekly_report(start_date, end_date, platform_manager_id)
