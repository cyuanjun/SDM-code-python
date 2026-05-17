"""Smoke tests for ViewFundraisingActivityPage (US-21)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_fundraising_activity_page import (
    ViewFundraisingActivityPage,
)


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewFundraisingActivityPage().render)


def test_render_does_not_raise_when_no_activities_exist() -> None:
    script = """
from boundary.view_fundraising_activity_page import ViewFundraisingActivityPage
ViewFundraisingActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_activities_exist() -> None:
    script = """
from datetime import date
from decimal import Decimal
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from entity.fundraising_activity import FundraisingActivity
from boundary.view_fundraising_activity_page import ViewFundraisingActivityPage

profile = UserProfile.create_profile(role="fundraiser", description="r")
account = UserAccount.create_account(
    email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
    phone_num="0", profile_id=profile.profile_id,
)
FundraisingActivity.create_fundraising_activity(
    title="A", description="d", target_amount=Decimal("100.00"),
    fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
    owner_account_id=account.account_id,
)
ViewFundraisingActivityPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
