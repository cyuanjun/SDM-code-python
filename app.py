"""Streamlit entry point. Drives navigation through st.session_state.

Routing is intentionally simple for Sprint 1: a sidebar lets the user pick a page.
Sprint 2+ will add role-based menus once admin/fundraiser/donee/manager flows diverge.
"""
from __future__ import annotations

import streamlit as st

from boundary.create_account_page import CreateAccountPage
from boundary.create_fundraising_activity_page import CreateFundraisingActivityPage
from boundary.create_profile_page import CreateProfilePage
from boundary.info_page import InfoPage
from boundary.login_page import LoginPage
from boundary.logout_page import LogoutPage
from boundary.view_fundraising_activity_page import ViewFundraisingActivityPage
from persistence.db import init_db

PAGES = {
    "Log in": LoginPage,
    "Log out": LogoutPage,
    "Create user profile": CreateProfilePage,
    "Create user account": CreateAccountPage,
    "Create fundraising activity": CreateFundraisingActivityPage,
    "View fundraising activity": ViewFundraisingActivityPage,
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
