"""Smoke + validation tests for GenerateReportPage (US-41/42/43)."""
from __future__ import annotations

from datetime import date

from streamlit.testing.v1 import AppTest

from boundary.generate_report_page import GenerateReportPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(GenerateReportPage().render)


def test_validate_range_accepts_well_formed() -> None:
    assert GenerateReportPage.validate_range(
        date(2026, 1, 1), date(2026, 1, 7)
    ) is True
    assert GenerateReportPage.validate_range(
        date(2026, 1, 1), date(2026, 1, 1)
    ) is True


def test_validate_range_rejects_start_after_end() -> None:
    assert GenerateReportPage.validate_range(
        date(2026, 12, 31), date(2026, 1, 1)
    ) is False


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
    phone_num="0", profile_id=profile.profile_id,
)
st.session_state["user"] = account
GenerateReportPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
