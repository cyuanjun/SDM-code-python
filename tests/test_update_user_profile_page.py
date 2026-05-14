"""Smoke + validation tests for UpdateUserProfilePage (US-3)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.update_user_profile_page import UpdateUserProfilePage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(UpdateUserProfilePage().render)


def test_validate_profile_accepts_well_formed_input() -> None:
    assert UpdateUserProfilePage.validate_profile("admin", "Full") is True


def test_validate_profile_rejects_blank_role() -> None:
    assert UpdateUserProfilePage.validate_profile("", "Full") is False
    assert UpdateUserProfilePage.validate_profile("  ", "Full") is False


def test_validate_profile_rejects_blank_description() -> None:
    assert UpdateUserProfilePage.validate_profile("admin", "") is False


def test_render_does_not_raise_when_no_profiles_exist() -> None:
    script = """
from boundary.update_user_profile_page import UpdateUserProfilePage
UpdateUserProfilePage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_profiles_exist() -> None:
    script = """
from entity.user_profile import UserProfile
from boundary.update_user_profile_page import UpdateUserProfilePage

UserProfile.create_profile(role="admin", description="Full access")
UpdateUserProfilePage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
