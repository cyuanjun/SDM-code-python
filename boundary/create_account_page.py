"""CreateAccountPage <<Boundary>>."""
from __future__ import annotations

from datetime import date

import streamlit as st

from controller.create_account_controller import CreateAccountController
from controller.non_diagram.view_profiles_controller import ViewProfilesController
from entity.user_account import UserAccount
from persistence.db import get_connection


def _which_unique_collided(email: str, phone_num: str) -> str:
    with get_connection() as conn:
        email_taken = conn.execute(
            "SELECT 1 FROM user_account WHERE email = ? LIMIT 1", (email,)
        ).fetchone() is not None
        phone_taken = conn.execute(
            "SELECT 1 FROM user_account WHERE phone_num = ? LIMIT 1",
            (phone_num,),
        ).fetchone() is not None
    if email_taken and phone_taken:
        return "email and phone number"
    if email_taken:
        return "email"
    if phone_taken:
        return "phone number"
    return "email or phone number"


class CreateAccountPage:
    def render(self) -> None:
        st.header("Create User Account")

        profiles = ViewProfilesController().view_all_profiles()
        if not profiles:
            st.warning(
                "No profiles exist yet. Create a user profile first "
                "(see the Create user profile page)."
            )
            return

        with st.form("create_account_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            name = st.text_input("Name")
            dob = st.date_input(
                "Date of birth",
                value=date(2000, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            phone_num = st.text_input("Phone number")
            profile_label_to_id = {
                f"{p.profile_id} — {p.role}": p.profile_id for p in profiles
            }
            profile_label = st.selectbox("Profile", list(profile_label_to_id.keys()))
            submitted = st.form_submit_button("Create account")

        if not submitted:
            return

        if not self.validate_account(email, password, name, phone_num):
            self.display_error()
            return

        account = CreateAccountController().create_account(
            email=email.strip(),
            password=password,
            name=name.strip(),
            dob=dob,
            phone_num=phone_num.strip(),
            profile_id=profile_label_to_id[profile_label],
        )
        if account is None:
            field = _which_unique_collided(email.strip(), phone_num.strip())
            st.error(f"An account with that {field} already exists.")
            return
        self.display_success(account)

    @staticmethod
    def validate_account(
        email: str, password: str, name: str, phone_num: str
    ) -> bool:
        if not email.strip() or "@" not in email:
            return False
        if not password:
            return False
        if not name.strip():
            return False
        if not phone_num.strip():
            return False
        return True

    @staticmethod
    def display_success(account) -> None:
        st.success(
            f"Account created: {account.account_id} ({account.email}) "
            f"linked to profile {account.profile_id}"
        )

    @staticmethod
    def display_error() -> None:
        st.error(
            "Invalid account details. Email must contain '@', and email, "
            "password, name, and phone number are all required."
        )
