"""Smoke + validation tests for LoginPage (US-11/18/26/39)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.login_page import LoginPage


def test_login_page_class_is_importable_and_has_render() -> None:
    assert callable(LoginPage().render)


def test_validate_credentials_accepts_well_formed_input() -> None:
    assert LoginPage.validate_credentials("ada@x.com", "p") is True


def test_validate_credentials_rejects_email_without_at_symbol() -> None:
    assert LoginPage.validate_credentials("not-an-email", "p") is False


def test_validate_credentials_rejects_blank_email() -> None:
    assert LoginPage.validate_credentials("", "p") is False
    assert LoginPage.validate_credentials("   ", "p") is False


def test_validate_credentials_rejects_empty_password() -> None:
    assert LoginPage.validate_credentials("ada@x.com", "") is False


def test_render_does_not_raise_on_first_paint() -> None:
    script = """
from boundary.login_page import LoginPage
LoginPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
