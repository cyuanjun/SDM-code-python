"""Streamlit entry point. Sprint 1 pages are wired in here as each user
story is rebuilt against the reworked diagrams.
"""
from __future__ import annotations

import streamlit as st

from boundary.create_account_page import CreateAccountPage
from boundary.create_fundraising_activity_page import (
    CreateFundraisingActivityPage,
)
from boundary.create_profile_page import CreateProfilePage
from boundary.login_page import LoginPage
from boundary.logout_page import LogoutPage
from boundary.update_my_fundraising_activity_page import (
    UpdateMyFundraisingActivityPage,
)
from boundary.view_my_completed_activity_page import (
    ViewMyCompletedActivityPage,
)
from boundary.view_my_fundraising_activities_page import (
    ViewMyFundraisingActivitiesPage,
)
from boundary.search_favourite_page import SearchFavouritePage
from boundary.search_my_completed_activity_page import (
    SearchMyCompletedActivityPage,
)
from boundary.view_favourite_page import ViewFavouritePage
from boundary.view_fundraising_activities_page import (
    ViewFundraisingActivitiesPage,
)
from boundary.view_fundraising_activity_page import (
    ViewFundraisingActivityPage,
)
from boundary.update_user_account_page import UpdateUserAccountPage
from boundary.update_user_profile_page import UpdateUserProfilePage
from boundary.view_my_fundraising_activity_page import (
    ViewMyFundraisingActivityPage,
)
from boundary.view_user_account_page import ViewUserAccountPage
from boundary.view_user_accounts_page import ViewUserAccountsPage
from boundary.view_user_profile_page import ViewUserProfilePage
from boundary.view_user_profiles_page import ViewUserProfilesPage
from data.seed import seed_default_admin
from persistence.db import init_db

PAGES: dict = {
    "Log in": LoginPage,
    "Log out": LogoutPage,
    "[Admin] Create user profile": CreateProfilePage,
    "[Admin] View user profile": ViewUserProfilePage,
    "[Admin] Update user profile": UpdateUserProfilePage,
    "[Admin] Search user profiles": ViewUserProfilesPage,
    "[Admin] Create user account": CreateAccountPage,
    "[Admin] View user account": ViewUserAccountPage,
    "[Admin] Update user account": UpdateUserAccountPage,
    "[Admin] Search user accounts": ViewUserAccountsPage,
    "[Fundraiser] Create fundraising activity": CreateFundraisingActivityPage,
    "[Fundraiser] View my fundraising activity": ViewMyFundraisingActivityPage,
    "[Fundraiser] Update my fundraising activity": UpdateMyFundraisingActivityPage,
    "[Fundraiser] Search my fundraising activities": ViewMyFundraisingActivitiesPage,
    "[Fundraiser] Search my completed activities": SearchMyCompletedActivityPage,
    "[Fundraiser] View my completed activity": ViewMyCompletedActivityPage,
    "[Donee] View fundraising activity": ViewFundraisingActivityPage,
    "[Donee] Search fundraising activities": ViewFundraisingActivitiesPage,
    "[Donee] My favourites": ViewFavouritePage,
    "[Donee] Search my favourites": SearchFavouritePage,
}


def main() -> None:
    st.set_page_config(page_title="SDM Fundraising", layout="wide")
    init_db()
    seed_default_admin()

    st.sidebar.title("SDM Fundraising")
    if "user" in st.session_state:
        user = st.session_state["user"]
        st.sidebar.success(
            f"Signed in as\n\n**{user.name}**\n\n{user.email}"
        )
    else:
        st.sidebar.info("Not signed in")

    selection = st.sidebar.radio("Page", list(PAGES.keys()))
    PAGES[selection]().render()


if __name__ == "__main__":
    main()
