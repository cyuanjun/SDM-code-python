"""Smoke + validation tests for ViewMyFundraisingActivitiesPage (US-17)."""
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


def test_render_does_not_raise_when_logged_in() -> None:
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
