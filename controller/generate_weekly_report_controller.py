"""GenerateWeeklyReportController <<Controller>>."""
from __future__ import annotations

from datetime import date

from entity.report import Report


class GenerateWeeklyReportController:
    def generate_weekly_report(
        self, start_date: date, end_date: date, platform_manager_id: str
    ) -> Report:
        return Report.generate_weekly_report(
            start_date=start_date,
            end_date=end_date,
            platform_manager_id=platform_manager_id,
        )
