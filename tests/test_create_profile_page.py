"""Smoke test for CreateProfilePage (US-1).

Streamlit UIs are hard to unit-test; per CLAUDE.md "TDD expectations" boundary
pages get smoke tests only. The streamlit.testing.v1 AppTest harness is
enough to confirm render() doesn't raise and the validation branch fires
on empty input.
"""
from __future__ import annotations

import pytest
from streamlit.testing.v1 import AppTest

from boundary.create_profile_page import CreateProfilePage


def test_create_profile_page_class_is_importable_and_has_render() -> None:
    page = CreateProfilePage()
    assert callable(page.render)


def test_validate_profile_accepts_non_empty_inputs() -> None:
    assert CreateProfilePage.validate_profile("admin", "Full access") is True


def test_validate_profile_rejects_empty_role() -> None:
    assert CreateProfilePage.validate_profile("", "Full access") is False
    assert CreateProfilePage.validate_profile("   ", "Full access") is False


def test_validate_profile_rejects_empty_description() -> None:
    assert CreateProfilePage.validate_profile("admin", "") is False
    assert CreateProfilePage.validate_profile("admin", "   ") is False


def test_render_does_not_raise_on_first_paint() -> None:
    """Smoke: AppTest mounts the page; the form is shown without submitting."""
    script = """
from boundary.create_profile_page import CreateProfilePage
CreateProfilePage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
