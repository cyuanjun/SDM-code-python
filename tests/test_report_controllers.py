"""Delegation tests for the three report controllers (US-41/42/43)."""
from __future__ import annotations

from datetime import date

import pytest

from controller.generate_daily_report_controller import (
    GenerateDailyReportController,
)
from controller.generate_monthly_report_controller import (
    GenerateMonthlyReportController,
)
from controller.generate_weekly_report_controller import (
    GenerateWeeklyReportController,
)
from entity.report import Report


def test_daily_controller_forwards(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        Report,
        "generate_daily_report",
        classmethod(
            lambda cls, start_date, end_date, platform_manager_id: "sentinel"
        ),
    )
    assert (
        GenerateDailyReportController().generate_daily_report(
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 1),
            platform_manager_id="acc_001",
        )
        == "sentinel"
    )


def test_weekly_controller_forwards(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        Report,
        "generate_weekly_report",
        classmethod(
            lambda cls, start_date, end_date, platform_manager_id: "sentinel"
        ),
    )
    assert (
        GenerateWeeklyReportController().generate_weekly_report(
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 7),
            platform_manager_id="acc_001",
        )
        == "sentinel"
    )


def test_monthly_controller_forwards(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        Report,
        "generate_monthly_report",
        classmethod(
            lambda cls, start_date, end_date, platform_manager_id: "sentinel"
        ),
    )
    assert (
        GenerateMonthlyReportController().generate_monthly_report(
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 31),
            platform_manager_id="acc_001",
        )
        == "sentinel"
    )
