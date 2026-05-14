"""Streamlit entry point.

The sidebar wires the UX-consolidated boundary pages (one per actor area,
each combining the diagram-defined per-US Boundary classes via search /
list / detail / inline create). The per-US classes still exist as
testable artifacts and as the diagram's 1:1 mapping — they're just not
sidebar entries.

The consolidation is logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

import streamlit as st

from boundary.browse_fundraising_activity_page import (
    BrowseFundraisingActivityPage,
)
from boundary.generate_report_page import GenerateReportPage
from boundary.info_page import InfoPage
from boundary.login_page import LoginPage
from boundary.logout_page import LogoutPage
from boundary.manage_fundraising_activity_category_page import (
    ManageFundraisingActivityCategoryPage,
)
from boundary.manage_my_fundraising_activity_page import (
    ManageMyFundraisingActivityPage,
)
from boundary.manage_user_account_page import ManageUserAccountPage
from boundary.manage_user_profile_page import ManageUserProfilePage
from boundary.my_donations_page import MyDonationsPage
from boundary.my_favourites_page import MyFavouritesPage
from data.seed import (
    seed_default_admin,
    seed_default_donee,
    seed_default_fundraiser,
    seed_default_platform_manager,
    seed_demo_donations,
)
from persistence.db import init_db

PAGES: dict = {
    "Log in": LoginPage,
    "Log out": LogoutPage,
    "[Admin] Manage user profiles": ManageUserProfilePage,
    "[Admin] Manage user accounts": ManageUserAccountPage,
    "[Fundraiser] Manage my fundraising activities": ManageMyFundraisingActivityPage,
    "[Donee] Browse fundraising activities": BrowseFundraisingActivityPage,
    "[Donee] My favourites": MyFavouritesPage,
    "[Donee] My donations": MyDonationsPage,
    "[PM] Manage FRA categories": ManageFundraisingActivityCategoryPage,
    "[PM] Generate report": GenerateReportPage,
    ".info (debug)": InfoPage,
}


def main() -> None:
    st.set_page_config(page_title="SDM Fundraising", layout="wide")
    init_db()
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()
    seed_demo_donations()

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
