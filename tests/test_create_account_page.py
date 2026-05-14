"""Smoke + validation tests for CreateAccountPage (US-6)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.create_account_page import CreateAccountPage


def test_create_account_page_class_is_importable_and_has_render() -> None:
    assert callable(CreateAccountPage().render)


def test_validate_account_accepts_well_formed_input() -> None:
    assert CreateAccountPage.validate_account(
        "ada@example.com", "hunter2", "Ada", "0400000000"
    ) is True


def test_validate_account_rejects_email_without_at_symbol() -> None:
    assert CreateAccountPage.validate_account(
        "not-an-email", "hunter2", "Ada", "0400000000"
    ) is False


def test_validate_account_rejects_blank_email() -> None:
    assert CreateAccountPage.validate_account(
        "", "hunter2", "Ada", "0400000000"
    ) is False
    assert CreateAccountPage.validate_account(
        "   ", "hunter2", "Ada", "0400000000"
    ) is False


def test_validate_account_rejects_empty_password() -> None:
    assert CreateAccountPage.validate_account(
        "ada@example.com", "", "Ada", "0400000000"
    ) is False


def test_validate_account_rejects_blank_name() -> None:
    assert CreateAccountPage.validate_account(
        "ada@example.com", "hunter2", "   ", "0400000000"
    ) is False


def test_validate_account_rejects_blank_phone() -> None:
    assert CreateAccountPage.validate_account(
        "ada@example.com", "hunter2", "Ada", ""
    ) is False


def test_render_does_not_raise_when_no_profiles_exist() -> None:
    """Boundary should show a warning, not raise, when there are no
    profiles to select."""
    script = """
from boundary.create_account_page import CreateAccountPage
CreateAccountPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_profiles_exist() -> None:
    """Boundary mounts the form when profiles are available."""
    script = """
from entity.user_profile import UserProfile
from boundary.create_account_page import CreateAccountPage

UserProfile.create_profile(role="admin", description="a")
CreateAccountPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
