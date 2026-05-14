"""Smoke + validation tests for ViewUserAccountsPage (US-10)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_user_accounts_page import ViewUserAccountsPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewUserAccountsPage().render)


def test_validate_criteria_accepts_non_empty_input() -> None:
    assert ViewUserAccountsPage.validate_criteria("ada") is True


def test_validate_criteria_rejects_blank_input() -> None:
    assert ViewUserAccountsPage.validate_criteria("") is False
    assert ViewUserAccountsPage.validate_criteria("   ") is False


def test_render_does_not_raise_on_first_paint() -> None:
    script = """
from boundary.view_user_accounts_page import ViewUserAccountsPage
ViewUserAccountsPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
