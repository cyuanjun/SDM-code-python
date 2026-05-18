"""Smoke + validation tests for GenerateReportPage (US-41/42/43)."""
from __future__ import annotations

from datetime import date

from streamlit.testing.v1 import AppTest

from boundary.generate_report_page import GenerateReportPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(GenerateReportPage().render)


def test_window_for_daily_returns_same_day_twice() -> None:
    picked = date(2026, 5, 14)  # Thursday
    assert GenerateReportPage.window_for("daily", picked) == (picked, picked)


def test_window_for_weekly_returns_monday_to_sunday_of_iso_week() -> None:
    """ISO week containing 2026-05-14 (Thu) is 2026-05-11 (Mon) → 2026-05-17 (Sun)."""
    picked = date(2026, 5, 14)
    assert GenerateReportPage.window_for("weekly", picked) == (
        date(2026, 5, 11), date(2026, 5, 17),
    )


def test_window_for_weekly_when_picked_is_monday() -> None:
    """Boundary case: picking the Monday itself returns (Monday, Sunday)."""
    monday = date(2026, 5, 11)
    assert GenerateReportPage.window_for("weekly", monday) == (
        monday, date(2026, 5, 17),
    )


def test_window_for_weekly_when_picked_is_sunday() -> None:
    """Boundary case: Sunday is the last day of its ISO week — the
    window walks back six days to the previous Monday, not forward."""
    sunday = date(2026, 5, 17)
    assert GenerateReportPage.window_for("weekly", sunday) == (
        date(2026, 5, 11), sunday,
    )


def test_window_for_monthly_returns_first_to_last_day_of_month() -> None:
    assert GenerateReportPage.window_for("monthly", date(2026, 5, 14)) == (
        date(2026, 5, 1), date(2026, 5, 31),
    )


def test_window_for_monthly_february_in_leap_year() -> None:
    """Negative-shape: end-of-month math handles variable month lengths."""
    # 2024 is a leap year → February has 29 days.
    assert GenerateReportPage.window_for("monthly", date(2024, 2, 14)) == (
        date(2024, 2, 1), date(2024, 2, 29),
    )
    # 2025 is not → February has 28 days.
    assert GenerateReportPage.window_for("monthly", date(2025, 2, 14)) == (
        date(2025, 2, 1), date(2025, 2, 28),
    )


def test_render_does_not_raise_when_not_logged_in() -> None:
    script = """
from boundary.generate_report_page import GenerateReportPage
GenerateReportPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_logged_in_as_pm() -> None:
    script = """
import streamlit as st
from datetime import date
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from boundary.generate_report_page import GenerateReportPage

profile = UserProfile.create_profile(role="platform_manager", description="PM")
account = UserAccount.create_account(
    email="pm@x.com", password="p", name="PM", dob=date(1980, 1, 1),
    phone_num="0400000084", profile_id=profile.profile_id,
)
st.session_state["user"] = account
GenerateReportPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
