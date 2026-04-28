"""CreateAccountPage <<Boundary>> — Sprint 1 diagram US-6.

Format validation happens here; existence check (email already taken)
returns None from the Entity, which we render as display_error().
"""
from __future__ import annotations

import re
from datetime import date

import streamlit as st

from controller.create_account_controller import CreateAccountController
from controller.view_profiles_controller import ViewProfilesController

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class CreateAccountPage:
    def render(self) -> None:
        st.header("Create user account")

        profiles = ViewProfilesController().view_all_profiles()
        if not profiles:
            st.warning(
                "No profiles exist yet. Create a user profile first "
                "before creating an account."
            )
            return

        labels = {self._label(p): p.profile_id for p in profiles}

        with st.form("create_account_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            name = st.text_input("Name")
            dob = st.date_input("Date of birth", min_value=date(1900, 1, 1))
            phone_num = st.text_input("Phone number")
            profile_label = st.selectbox("Profile", list(labels.keys()))
            submitted = st.form_submit_button("Create account")

        if not submitted:
            return

        if not self._validate(email, password, name, phone_num):
            return

        account = CreateAccountController().create_account(
            email=email,
            password=password,
            name=name,
            dob=str(dob),
            phone_num=phone_num,
            profile_id=int(labels[profile_label]),
        )
        if account is not None:
            self.display_success()
        else:
            self.display_error()

    @staticmethod
    def _label(profile) -> str:
        desc_preview = (profile.description or "")[:50]
        return f"#{profile.profile_id} — {profile.role}: {desc_preview}"

    @staticmethod
    def _validate(email: str, password: str, name: str, phone_num: str) -> bool:
        if not all([email, password, name, phone_num]):
            st.error("All fields are required.")
            return False
        if not EMAIL_PATTERN.match(email):
            st.error("Email format is invalid.")
            return False
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
            return False
        if not phone_num.replace("+", "").replace(" ", "").isdigit():
            st.error("Phone number must contain digits only.")
            return False
        return True

    @staticmethod
    def display_success() -> None:
        st.success("Account created.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not create account (email may already exist).")
