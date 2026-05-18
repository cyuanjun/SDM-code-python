"""Streamlit entry point."""
from __future__ import annotations

import streamlit as st

from boundary.generate_report_page import GenerateReportPage
from boundary.login_page import LoginPage
from boundary.logout_page import LogoutPage
from boundary.non_diagram.browse_fundraising_activity_page import (
    BrowseFundraisingActivityPage,
)
from boundary.non_diagram.info_page import InfoPage
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
from controller.view_user_profile_controller import ViewUserProfileController
from data.seed import (
    seed_bulk_all,
    seed_default_admin,
    seed_default_donee,
    seed_default_fundraiser,
    seed_default_platform_manager,
    seed_demo_donations,
)
from entity.fundraising_activity import FundraisingActivity
from persistence.db import init_db

PAGES: dict = {
    "Log In": LoginPage,
    "Log Out": LogoutPage,
    "[Admin] Manage User Profiles": ManageUserProfilePage,
    "[Admin] Manage User Accounts": ManageUserAccountPage,
    "[Fundraiser] Manage My Fundraising Activities": ManageMyFundraisingActivityPage,
    "[Donee] Browse Fundraising Activities": BrowseFundraisingActivityPage,
    "[Donee] My Favourites": MyFavouritesPage,
    "[Donee] My Donations": MyDonationsPage,
    "[PM] Manage FRA Categories": ManageFundraisingActivityCategoryPage,
    "[PM] Generate Report": GenerateReportPage,
    ".info (debug)": InfoPage,
}

PAGES_BY_ROLE: dict[str | None, list[str]] = {
    None: [
        "Log In",
        ".info (debug)",
    ],
    "admin": [
        "Log Out",
        "[Admin] Manage User Profiles",
        "[Admin] Manage User Accounts",
        ".info (debug)",
    ],
    "fundraiser": [
        "Log Out",
        "[Fundraiser] Manage My Fundraising Activities",
        ".info (debug)",
    ],
    "donee": [
        "Log Out",
        "[Donee] Browse Fundraising Activities",
        "[Donee] My Favourites",
        "[Donee] My Donations",
        ".info (debug)",
    ],
    "platform_manager": [
        "Log Out",
        "[PM] Manage FRA Categories",
        "[PM] Generate Report",
        ".info (debug)",
    ],
}


def _current_role() -> str | None:
    user = st.session_state.get("user")
    if user is None:
        return None
    profile = ViewUserProfileController().view_user_profile(user.profile_id)
    return profile.role if profile is not None else None


def main() -> None:
    st.set_page_config(page_title="SDM Fundraising", layout="wide")
    init_db()
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()
    seed_demo_donations()
    seed_bulk_all()
    FundraisingActivity.refresh_completed_flags()

    role = _current_role()
    allowed_labels = PAGES_BY_ROLE.get(role, PAGES_BY_ROLE[None])

    st.sidebar.title("SDM Fundraising")
    if role is not None:
        user = st.session_state["user"]
        st.sidebar.success(
            f"Signed in as\n\n**{user.name}** ({role})\n\n{user.email}"
        )
    else:
        st.sidebar.info("Not signed in")

    selection = st.sidebar.radio("Page", allowed_labels)
    PAGES[selection]().render()


if __name__ == "__main__":
    main()
