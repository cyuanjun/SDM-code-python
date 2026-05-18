"""Smoke + validation tests for ViewUserProfilesPage (US-5)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_user_profiles_page import ViewUserProfilesPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewUserProfilesPage().render)


def test_validate_criteria_accepts_non_empty_input() -> None:
    assert ViewUserProfilesPage.validate_criteria("admin") is True


def test_validate_criteria_rejects_blank_input() -> None:
    assert ViewUserProfilesPage.validate_criteria("") is False
    assert ViewUserProfilesPage.validate_criteria("   ") is False


def test_render_does_not_raise_on_first_paint() -> None:
    script = """
from boundary.view_user_profiles_page import ViewUserProfilesPage
ViewUserProfilesPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
