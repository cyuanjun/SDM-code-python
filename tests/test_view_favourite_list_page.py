"""Smoke tests for ViewFavouriteListPage (US-24)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.view_favourite_list_page import ViewFavouriteListPage


def test_page_class_is_importable_and_has_render() -> None:
    assert callable(ViewFavouriteListPage().render)


def test_render_does_not_raise_when_not_logged_in() -> None:
    script = """
from boundary.view_favourite_list_page import ViewFavouriteListPage
ViewFavouriteListPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_logged_in_with_no_favourites() -> None:
    script = """
import streamlit as st
from datetime import date
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from boundary.view_favourite_list_page import ViewFavouriteListPage

profile = UserProfile.create_profile(role="donee", description="r")
account = UserAccount.create_account(
    email="d@x.com", password="p", name="D", dob=date(1990, 1, 1),
    phone_num="0400000034", profile_id=profile.profile_id,
)
st.session_state["user"] = account
ViewFavouriteListPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_render_does_not_raise_when_logged_in_with_favourites() -> None:
    script = """
import streamlit as st
from datetime import date
from decimal import Decimal
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from entity.fundraising_activity import FundraisingActivity
from entity.favourite import Favourite
from boundary.view_favourite_list_page import ViewFavouriteListPage

donee_profile = UserProfile.create_profile(role="donee", description="r")
donee = UserAccount.create_account(
    email="d@x.com", password="p", name="D", dob=date(1990, 1, 1),
    phone_num="0400000058", profile_id=donee_profile.profile_id,
)
fr_profile = UserProfile.create_profile(role="fundraiser", description="r")
fr = UserAccount.create_account(
    email="f@x.com", password="p", name="F", dob=date(1990, 1, 1),
    phone_num="0400000063", profile_id=fr_profile.profile_id,
)
activity = FundraisingActivity.create_fundraising_activity(
    title="A", description="d", target_amount=Decimal("100"),
    fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
    owner_account_id=fr.account_id,
)
Favourite.save_fundraising_activity(
    account_id=donee.account_id, fra_id=activity.fra_id
)
st.session_state["user"] = donee
ViewFavouriteListPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
