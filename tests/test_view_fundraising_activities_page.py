"""Smoke + validation tests for ViewFundraisingActivitiesPage (US-20)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_fundraising_activities_page import (
    ViewFundraisingActivitiesPage,
)


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewFundraisingActivitiesPage().render)


def test_validate_criteria_accepts_non_empty_input() -> None:
    assert ViewFundraisingActivitiesPage.validate_criteria("medical") is True


def test_validate_criteria_rejects_blank_input() -> None:
    assert ViewFundraisingActivitiesPage.validate_criteria("") is False
    assert ViewFundraisingActivitiesPage.validate_criteria("   ") is False


def test_render_does_not_raise_on_first_paint() -> None:
    script = """
from boundary.view_fundraising_activities_page import ViewFundraisingActivitiesPage
ViewFundraisingActivitiesPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
