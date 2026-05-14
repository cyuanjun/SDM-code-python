"""Smoke + validation tests for UpdateUserAccountPage (US-8)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.update_user_account_page import UpdateUserAccountPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(UpdateUserAccountPage().render)


def test_validate_account_accepts_well_formed_input() -> None:
    assert UpdateUserAccountPage.validate_account(
        "ada@x.com", "p", "Ada", "0400000000"
    ) is True


def test_validate_account_rejects_email_without_at_symbol() -> None:
    assert UpdateUserAccountPage.validate_account(
        "not-an-email", "p", "Ada", "0"
    ) is False


def test_validate_account_rejects_empty_password() -> None:
    assert UpdateUserAccountPage.validate_account(
        "ada@x.com", "", "Ada", "0"
    ) is False


def test_validate_account_rejects_blank_name() -> None:
    assert UpdateUserAccountPage.validate_account(
        "ada@x.com", "p", "", "0"
    ) is False


def test_validate_account_rejects_blank_phone() -> None:
    assert UpdateUserAccountPage.validate_account(
        "ada@x.com", "p", "Ada", ""
    ) is False


def test_render_does_not_raise_when_no_accounts_exist() -> None:
    script = """
from boundary.update_user_account_page import UpdateUserAccountPage
UpdateUserAccountPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_accounts_exist() -> None:
    script = """
from datetime import date
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from boundary.update_user_account_page import UpdateUserAccountPage

profile = UserProfile.create_profile(role="admin", description="a")
UserAccount.create_account(
    email="a@x.com", password="p", name="A", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
UpdateUserAccountPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
