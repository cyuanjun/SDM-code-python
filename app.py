"""Streamlit entry point. Drives navigation through st.session_state.

Sprint 2 expanded the page count significantly. Pages are grouped by actor
in the sidebar with a leading bracket prefix so non-relevant pages are easy
to skip. Role-based menu gating remains a deferred decision (see docs/todo.md).
"""
from __future__ import annotations

import streamlit as st

from boundary.create_account_page import CreateAccountPage
from boundary.create_fundraising_activity_page import CreateFundraisingActivityPage
from boundary.create_profile_page import CreateProfilePage
from boundary.delete_favourite_page import DeleteFavouritePage
from boundary.delete_user_profile_page import DeleteUserProfilePage
from boundary.info_page import InfoPage
from boundary.login_page import LoginPage
from boundary.logout_page import LogoutPage
from boundary.save_fundraiser_activity_page import SaveFundraiserActivityPage
from boundary.search_completed_activity_page import SearchCompletedActivityPage
from boundary.search_favourite_page import SearchFavouritePage
from boundary.search_fundraiser_activity_page import SearchFundraiserActivityPage
from boundary.search_fundraising_activity_page import SearchFundraisingActivityPage
from boundary.search_user_account_page import SearchUserAccountPage
from boundary.search_user_profile_page import SearchUserProfilePage
from boundary.suspend_fundraising_activity_page import (
    SuspendFundraisingActivityPage,
)
from boundary.suspend_user_account_page import SuspendUserAccountPage
from boundary.update_fundraiser_activity_page import UpdateFundraiserActivityPage
from boundary.update_user_account_page import UpdateUserAccountPage
from boundary.update_user_profile_page import UpdateUserProfilePage
from boundary.view_completed_activity_page import ViewCompletedActivityPage
from boundary.view_favourite_list_page import ViewFavouriteListPage
from boundary.view_fundraiser_activity_page import ViewFundraiserActivityPage
from boundary.view_fundraising_activity_page import ViewFundraisingActivityPage
from boundary.view_user_account_page import ViewUserAccountPage
from boundary.view_user_profile_page import ViewUserProfilePage
from persistence.db import init_db

PAGES = {
    "Log in": LoginPage,
    "Log out": LogoutPage,
    "[Admin] Create user profile": CreateProfilePage,
    "[Admin] View user profile": ViewUserProfilePage,
    "[Admin] Update user profile": UpdateUserProfilePage,
    "[Admin] Delete user profile": DeleteUserProfilePage,
    "[Admin] Search user profiles": SearchUserProfilePage,
    "[Admin] Create user account": CreateAccountPage,
    "[Admin] View user account": ViewUserAccountPage,
    "[Admin] Update user account": UpdateUserAccountPage,
    "[Admin] Suspend user account": SuspendUserAccountPage,
    "[Admin] Search user accounts": SearchUserAccountPage,
    "[Fundraiser] Create fundraising activity": CreateFundraisingActivityPage,
    "[Fundraiser] View my fundraising activity": ViewFundraiserActivityPage,
    "[Fundraiser] Update my fundraising activity": UpdateFundraiserActivityPage,
    "[Fundraiser] Suspend my fundraising activity": SuspendFundraisingActivityPage,
    "[Fundraiser] Search my fundraising activities": SearchFundraisingActivityPage,
    "[Fundraiser] Search my completed activities": SearchCompletedActivityPage,
    "[Fundraiser] View my completed activities": ViewCompletedActivityPage,
    "[Donee] View fundraising activity": ViewFundraisingActivityPage,
    "[Donee] Search fundraising activities": SearchFundraiserActivityPage,
    "[Donee] Save to favourites": SaveFundraiserActivityPage,
    "[Donee] View my favourites": ViewFavouriteListPage,
    "[Donee] Search my favourites": SearchFavouritePage,
    "[Donee] Delete a favourite": DeleteFavouritePage,
    ".info (debug)": InfoPage,
}


def main() -> None:
    st.set_page_config(page_title="SDM Fundraising", layout="wide")
    init_db()

    st.sidebar.title("SDM Fundraising")
    if "user" in st.session_state:
        st.sidebar.success(f"Signed in as {st.session_state['user'].email}")
    else:
        st.sidebar.info("Not signed in")

    selection = st.sidebar.radio("Page", list(PAGES.keys()))
    page_cls = PAGES[selection]
    page_cls().render()


if __name__ == "__main__":
    main()
