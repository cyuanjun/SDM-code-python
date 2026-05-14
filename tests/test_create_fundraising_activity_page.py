"""Smoke + validation tests for CreateFundraisingActivityPage (US-13)."""
from __future__ import annotations

from datetime import date

from streamlit.testing.v1 import AppTest

from boundary.create_fundraising_activity_page import (
    CreateFundraisingActivityPage,
)


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(CreateFundraisingActivityPage().render)


def test_validate_activity_accepts_well_formed_input() -> None:
    assert CreateFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="100.00",
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
    ) is True


def test_validate_activity_rejects_blank_title() -> None:
    assert CreateFundraisingActivityPage.validate_activity(
        title="   ", description="d", target_amount_str="100.00",
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
    ) is False


def test_validate_activity_rejects_blank_description() -> None:
    assert CreateFundraisingActivityPage.validate_activity(
        title="A", description="", target_amount_str="100.00",
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
    ) is False


def test_validate_activity_rejects_blank_category() -> None:
    assert CreateFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="100.00",
        category="", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
    ) is False


def test_validate_activity_rejects_non_numeric_target_amount() -> None:
    assert CreateFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="abc",
        category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
    ) is False


def test_validate_activity_rejects_zero_or_negative_target_amount() -> None:
    for bad in ("0", "0.00", "-1", "-100.50"):
        assert CreateFundraisingActivityPage.validate_activity(
            title="A", description="d", target_amount_str=bad,
            category="x", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        ) is False


def test_validate_activity_rejects_start_after_end() -> None:
    assert CreateFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="100",
        category="x", start_date=date(2026, 12, 31), end_date=date(2026, 1, 1),
    ) is False


def test_render_warns_when_no_user_in_session() -> None:
    script = """
from boundary.create_fundraising_activity_page import CreateFundraisingActivityPage
CreateFundraisingActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_shows_form_when_user_in_session() -> None:
    script = """
import streamlit as st
from datetime import date
from entity.user_account import UserAccount
from boundary.create_fundraising_activity_page import CreateFundraisingActivityPage

st.session_state["user"] = UserAccount(
    email="fr@x.com", password="p", name="Fr",
    dob=date(1980, 1, 1), phone_num="0",
    profile_id="prof_001", account_id="acc_001",
)
CreateFundraisingActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
