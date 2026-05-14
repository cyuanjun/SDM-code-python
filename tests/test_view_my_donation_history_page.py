"""Smoke tests for ViewMyDonationHistoryPage (US-33)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_my_donation_history_page import ViewMyDonationHistoryPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewMyDonationHistoryPage().render)


def test_render_does_not_raise_when_not_logged_in() -> None:
    script = """
from boundary.view_my_donation_history_page import ViewMyDonationHistoryPage
ViewMyDonationHistoryPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_logged_in_with_no_donations() -> None:
    script = """
import streamlit as st
from datetime import date
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from boundary.view_my_donation_history_page import ViewMyDonationHistoryPage

profile = UserProfile.create_profile(role="donee", description="r")
account = UserAccount.create_account(
    email="d@x.com", password="p", name="D", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
st.session_state["user"] = account
ViewMyDonationHistoryPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
