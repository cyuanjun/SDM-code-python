"""Smoke tests for ViewMyFundraisingActivityPage (US-14)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_my_fundraising_activity_page import (
    ViewMyFundraisingActivityPage,
)


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewMyFundraisingActivityPage().render)


def test_render_does_not_raise_when_not_logged_in() -> None:
    script = """
from boundary.view_my_fundraising_activity_page import ViewMyFundraisingActivityPage
ViewMyFundraisingActivityPage().render()
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
from boundary.view_my_fundraising_activity_page import ViewMyFundraisingActivityPage

profile = UserProfile.create_profile(role="fundraiser", description="r")
account = UserAccount.create_account(
    email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
st.session_state["user"] = account
ViewMyFundraisingActivityPage().render()
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
from boundary.view_my_fundraising_activity_page import ViewMyFundraisingActivityPage

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
ViewMyFundraisingActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
