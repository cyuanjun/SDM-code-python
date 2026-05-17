"""Smoke + validation tests for UpdateMyFundraisingActivityPage (US-15)."""
from __future__ import annotations

from datetime import date

from streamlit.testing.v1 import AppTest

from boundary.update_my_fundraising_activity_page import (
    UpdateMyFundraisingActivityPage,
)


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(UpdateMyFundraisingActivityPage().render)


# A fixed "today" anchor — update_my treats existing past start_dates as
# legitimate (the activity may already be running) but disallows end_dates
# in the past.
_TODAY = date(2026, 1, 1)


def test_validate_activity_accepts_well_formed_input() -> None:
    assert UpdateMyFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="100",
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        today=_TODAY,
    ) is True


def test_validate_activity_rejects_blank_title() -> None:
    assert UpdateMyFundraisingActivityPage.validate_activity(
        title="", description="d", target_amount_str="100",
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        today=_TODAY,
    ) is False


def test_validate_activity_rejects_zero_target() -> None:
    assert UpdateMyFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="0",
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        today=_TODAY,
    ) is False


def test_validate_activity_rejects_non_numeric_target() -> None:
    assert UpdateMyFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="abc",
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        today=_TODAY,
    ) is False


def test_validate_activity_rejects_start_after_end() -> None:
    assert UpdateMyFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="100",
        fra_cat_id="cat_001", start_date=date(2026, 12, 31), end_date=date(2026, 6, 1),
        today=_TODAY,
    ) is False


def test_validate_activity_accepts_past_start_date_with_future_end_date() -> None:
    """Already-running activities (past start) are legitimate to update —
    the user might be extending the end date."""
    assert UpdateMyFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="100",
        fra_cat_id="cat_001",
        start_date=date(2025, 6, 1), end_date=date(2026, 6, 1),
        today=_TODAY,
    ) is True


def test_validate_activity_rejects_end_date_in_the_past() -> None:
    """Even when extending an existing activity, the new end date can't
    retroactively land before today."""
    assert UpdateMyFundraisingActivityPage.validate_activity(
        title="A", description="d", target_amount_str="100",
        fra_cat_id="cat_001",
        start_date=date(2025, 6, 1), end_date=date(2025, 12, 31),
        today=_TODAY,
    ) is False


def test_render_does_not_raise_when_not_logged_in() -> None:
    script = """
from boundary.update_my_fundraising_activity_page import UpdateMyFundraisingActivityPage
UpdateMyFundraisingActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_logged_in_with_activities() -> None:
    script = """
import streamlit as st
from datetime import date
from decimal import Decimal
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from entity.fundraising_activity import FundraisingActivity
from boundary.update_my_fundraising_activity_page import UpdateMyFundraisingActivityPage

profile = UserProfile.create_profile(role="fundraiser", description="r")
account = UserAccount.create_account(
    email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
FundraisingActivity.create_fundraising_activity(
    title="A", description="d", target_amount=Decimal("100"),
    fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
    owner_account_id=account.account_id,
)
st.session_state["user"] = account
UpdateMyFundraisingActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
