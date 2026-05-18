"""Smoke tests for the seven UX-consolidated boundary pages.

These pages are NOT on any diagram — they combine multiple US flows
per the 2026-05-15 sketch. Smoke coverage only; the underlying
controllers + entities are tested in detail elsewhere.
"""
from __future__ import annotations

from datetime import date

from streamlit.testing.v1 import AppTest

from boundary.non_diagram.browse_fundraising_activity_page import (
    BrowseFundraisingActivityPage,
)
from boundary.non_diagram.manage_fundraising_activity_category_page import (
    ManageFundraisingActivityCategoryPage,
)
from boundary.non_diagram.manage_my_fundraising_activity_page import (
    ManageMyFundraisingActivityPage,
)
from boundary.non_diagram.manage_user_account_page import ManageUserAccountPage
from boundary.non_diagram.manage_user_profile_page import ManageUserProfilePage
from boundary.non_diagram.my_donations_page import MyDonationsPage
from boundary.non_diagram.my_favourites_page import MyFavouritesPage


def test_combined_pages_are_importable_and_have_render() -> None:
    for cls in (
        ManageUserProfilePage,
        ManageUserAccountPage,
        ManageMyFundraisingActivityPage,
        BrowseFundraisingActivityPage,
        MyFavouritesPage,
        MyDonationsPage,
        ManageFundraisingActivityCategoryPage,
    ):
        assert callable(cls().render)


def _run(script: str) -> None:
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_manage_user_profile_page_renders_when_empty() -> None:
    _run(
        "from boundary.non_diagram.manage_user_profile_page import ManageUserProfilePage\n"
        "ManageUserProfilePage().render()\n"
    )


def test_manage_user_profile_page_renders_with_a_profile() -> None:
    _run(
        "from entity.user_profile import UserProfile\n"
        "from boundary.non_diagram.manage_user_profile_page import ManageUserProfilePage\n"
        "UserProfile.create_profile(role='admin', description='a')\n"
        "ManageUserProfilePage().render()\n"
    )


def test_manage_user_account_page_renders_when_empty() -> None:
    _run(
        "from boundary.non_diagram.manage_user_account_page import ManageUserAccountPage\n"
        "ManageUserAccountPage().render()\n"
    )


def test_manage_my_fundraising_activity_page_renders_when_not_logged_in() -> None:
    _run(
        "from boundary.non_diagram.manage_my_fundraising_activity_page import ManageMyFundraisingActivityPage\n"
        "ManageMyFundraisingActivityPage().render()\n"
    )


def test_manage_my_fundraising_activity_page_renders_when_logged_in() -> None:
    _run(
        "import streamlit as st\n"
        "from datetime import date\n"
        "from entity.user_profile import UserProfile\n"
        "from entity.user_account import UserAccount\n"
        "from boundary.non_diagram.manage_my_fundraising_activity_page import ManageMyFundraisingActivityPage\n"
        "profile = UserProfile.create_profile(role='fundraiser', description='r')\n"
        "account = UserAccount.create_account(\n"
        "    email='o@x.com', password='p', name='O', dob=date(1990, 1, 1),\n"
        "    phone_num='0', profile_id=profile.profile_id,\n"
        ")\n"
        "st.session_state['user'] = account\n"
        "ManageMyFundraisingActivityPage().render()\n"
    )


def test_browse_fundraising_activity_page_renders_when_empty() -> None:
    _run(
        "from boundary.non_diagram.browse_fundraising_activity_page import BrowseFundraisingActivityPage\n"
        "BrowseFundraisingActivityPage().render()\n"
    )


def test_my_favourites_page_renders_when_not_logged_in() -> None:
    _run(
        "from boundary.non_diagram.my_favourites_page import MyFavouritesPage\n"
        "MyFavouritesPage().render()\n"
    )


def test_my_favourites_page_renders_when_logged_in() -> None:
    _run(
        "import streamlit as st\n"
        "from datetime import date\n"
        "from entity.user_profile import UserProfile\n"
        "from entity.user_account import UserAccount\n"
        "from boundary.non_diagram.my_favourites_page import MyFavouritesPage\n"
        "profile = UserProfile.create_profile(role='donee', description='r')\n"
        "account = UserAccount.create_account(\n"
        "    email='d@x.com', password='p', name='D', dob=date(1990, 1, 1),\n"
        "    phone_num='0', profile_id=profile.profile_id,\n"
        ")\n"
        "st.session_state['user'] = account\n"
        "MyFavouritesPage().render()\n"
    )


def test_my_donations_page_renders_when_logged_in() -> None:
    _run(
        "import streamlit as st\n"
        "from datetime import date\n"
        "from entity.user_profile import UserProfile\n"
        "from entity.user_account import UserAccount\n"
        "from boundary.non_diagram.my_donations_page import MyDonationsPage\n"
        "profile = UserProfile.create_profile(role='donee', description='r')\n"
        "account = UserAccount.create_account(\n"
        "    email='d@x.com', password='p', name='D', dob=date(1990, 1, 1),\n"
        "    phone_num='0', profile_id=profile.profile_id,\n"
        ")\n"
        "st.session_state['user'] = account\n"
        "MyDonationsPage().render()\n"
    )


def test_manage_fra_category_page_renders_when_empty() -> None:
    _run(
        "from boundary.non_diagram.manage_fundraising_activity_category_page import ManageFundraisingActivityCategoryPage\n"
        "ManageFundraisingActivityCategoryPage().render()\n"
    )
