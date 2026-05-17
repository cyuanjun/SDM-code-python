"""Smoke + validation tests for ViewMyFundraisingActivitiesPage (US-17 + US-30 + US-31)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_my_fundraising_activities_page import (
    ViewMyFundraisingActivitiesPage,
)


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewMyFundraisingActivitiesPage().render)


def test_validate_criteria_accepts_non_empty_input() -> None:
    assert ViewMyFundraisingActivitiesPage.validate_criteria("hospital") is True


def test_validate_criteria_rejects_blank_input() -> None:
    assert ViewMyFundraisingActivitiesPage.validate_criteria("") is False


def test_render_does_not_raise_when_not_logged_in() -> None:
    script = """
from boundary.view_my_fundraising_activities_page import ViewMyFundraisingActivitiesPage
ViewMyFundraisingActivitiesPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_logged_in_with_no_activities() -> None:
    script = """
import streamlit as st
from datetime import date
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from boundary.view_my_fundraising_activities_page import ViewMyFundraisingActivitiesPage

profile = UserProfile.create_profile(role="fundraiser", description="r")
account = UserAccount.create_account(
    email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
st.session_state["user"] = account
ViewMyFundraisingActivitiesPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_logged_in_with_completed_activity() -> None:
    """Covers the [Completed] tab default render (US-31 list path)."""
    script = """
import streamlit as st
from datetime import date
from decimal import Decimal
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from entity.fundraising_activity import FundraisingActivity
from boundary.view_my_fundraising_activities_page import ViewMyFundraisingActivitiesPage

profile = UserProfile.create_profile(role="fundraiser", description="r")
account = UserAccount.create_account(
    email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
activity = FundraisingActivity.create_fundraising_activity(
    title="A", description="d", target_amount=Decimal("100"),
    category="x", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
    owner_account_id=account.account_id,
)
# Flip completed = 1 directly so US-31 list returns one row.
updated = FundraisingActivity(
    title=activity.title, description=activity.description,
    target_amount=activity.target_amount, category=activity.category,
    start_date=activity.start_date, end_date=activity.end_date,
    owner_account_id=account.account_id,
    completed=True, suspended=False,
)
FundraisingActivity.update_my_fundraising_activity(
    owner_account_id=account.account_id, fra_id=activity.fra_id,
    updated_my_fra=updated,
)
st.session_state["user"] = account
ViewMyFundraisingActivitiesPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_display_my_completed_method_present() -> None:
    """US-31 method moved onto this class per 2026-05-18 diagram."""
    assert callable(ViewMyFundraisingActivitiesPage.display_my_completed_fundraising_activities)


def test_display_matching_completed_method_present() -> None:
    """US-30 method moved onto this class per 2026-05-18 diagram."""
    assert callable(ViewMyFundraisingActivitiesPage.display_matching_my_completed_fundraising_activity)
