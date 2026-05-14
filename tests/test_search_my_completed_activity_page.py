"""Smoke + validation tests for SearchMyCompletedActivityPage (US-30)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.search_my_completed_activity_page import (
    SearchMyCompletedActivityPage,
)


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(SearchMyCompletedActivityPage().render)


def test_validate_criteria_accepts_non_empty_input() -> None:
    assert SearchMyCompletedActivityPage.validate_criteria("hospital") is True


def test_validate_criteria_rejects_blank_input() -> None:
    assert SearchMyCompletedActivityPage.validate_criteria("") is False


def test_render_does_not_raise_when_not_logged_in() -> None:
    script = """
from boundary.search_my_completed_activity_page import SearchMyCompletedActivityPage
SearchMyCompletedActivityPage().render()
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
from boundary.search_my_completed_activity_page import SearchMyCompletedActivityPage

profile = UserProfile.create_profile(role="fundraiser", description="r")
account = UserAccount.create_account(
    email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
st.session_state["user"] = account
SearchMyCompletedActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
