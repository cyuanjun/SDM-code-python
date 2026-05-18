"""GenerateDailyReportController <<Controller>>."""
from __future__ import annotations

from datetime import date

from entity.report import Report


class GenerateDailyReportController:
    def generate_daily_report(
        self, start_date: date, end_date: date, platform_manager_id: str
    ) -> Report:
        return Report.generate_daily_report(
            start_date=start_date,
            end_date=end_date,
            platform_manager_id=platform_manager_id,
        )
