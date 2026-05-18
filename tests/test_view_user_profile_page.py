"""Smoke tests for ViewUserProfilePage (US-2)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_user_profile_page import ViewUserProfilePage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewUserProfilePage().render)


def test_render_does_not_raise_when_no_profiles_exist() -> None:
    script = """
from boundary.view_user_profile_page import ViewUserProfilePage
ViewUserProfilePage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_profiles_exist() -> None:
    script = """
from entity.user_profile import UserProfile
from boundary.view_user_profile_page import ViewUserProfilePage

UserProfile.create_profile(role="admin", description="Full access")
UserProfile.create_profile(role="donee", description="Browses campaigns")
ViewUserProfilePage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
