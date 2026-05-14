"""Streamlit entry point. Sprint 1 pages are wired in here as each user
story is rebuilt against the reworked diagrams.
"""
from __future__ import annotations

import streamlit as st

from boundary.create_account_page import CreateAccountPage
from boundary.create_profile_page import CreateProfilePage
from persistence.db import init_db

PAGES: dict = {
    "[Admin] Create user profile": CreateProfilePage,
    "[Admin] Create user account": CreateAccountPage,
}


def main() -> None:
    st.set_page_config(page_title="SDM Fundraising", layout="wide")
    init_db()

    st.sidebar.title("SDM Fundraising")
    st.sidebar.info("Revamp branch — no pages wired yet")

    st.title("SDM Online Fundraising System")
    st.write(
        "This branch is rebuilding from reworked diagrams. "
        "Pages will appear in the sidebar as each user story lands."
    )

    if PAGES:
        selection = st.sidebar.radio("Page", list(PAGES.keys()))
        PAGES[selection]().render()


if __name__ == "__main__":
    main()
