"""GenerateDailyReportController <<Controller>> — pure delegator, US-41."""
from __future__ import annotations

from typing import Optional

from entity.report import Report


class GenerateDailyReportController:
    def generate_daily_report(
        self, start_date: str, end_date: str, platform_manager_id: Optional[int]
    ) -> Report:
        return Report.generate_daily_report(start_date, end_date, platform_manager_id)
