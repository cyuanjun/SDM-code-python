"""Smoke tests for ViewUserAccountPage (US-7)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_user_account_page import ViewUserAccountPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewUserAccountPage().render)


def test_render_does_not_raise_when_no_accounts_exist() -> None:
    script = """
from boundary.view_user_account_page import ViewUserAccountPage
ViewUserAccountPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_accounts_exist() -> None:
    script = """
from datetime import date
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from boundary.view_user_account_page import ViewUserAccountPage

profile = UserProfile.create_profile(role="admin", description="a")
UserAccount.create_account(
    email="a@x.com", password="p", name="A", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
ViewUserAccountPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
