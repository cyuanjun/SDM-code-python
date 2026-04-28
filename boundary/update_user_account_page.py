"""UpdateUserAccountPage <<Boundary>> — Sprint 2 diagram US-8."""
from __future__ import annotations

import re
from datetime import date

import streamlit as st

from controller.update_user_account_controller import UpdateUserAccountController
from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_account_controller import ViewUserAccountController
from entity.user_account import UserAccount

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
EDIT_KEY = "editing_account_id"


class UpdateUserAccountPage:
    def render(self) -> None:
        st.header("Update user account")

        controller = ViewUserAccountController()
        accounts = controller.view_all_user_accounts()
        if not accounts:
            st.info("No accounts to update.")
            return

        if EDIT_KEY not in st.session_state:
            st.caption("Select an account to edit:")
            labels = {f"#{a.account_id} — {a.email}": a.account_id for a in accounts}
            choice = st.selectbox("Account", list(labels.keys()))
            if st.button("Edit", key="click_edit_option_account"):
                self.click_edit_option(str(labels[choice]))
                st.rerun()
            return

        self.display_update_page()

    def display_update_page(self) -> None:
        account_id = st.session_state[EDIT_KEY]
        current = ViewUserAccountController().view_user_account(account_id)
        if current is None:
            st.error("Account not found.")
            st.session_state.pop(EDIT_KEY, None)
            return

        profiles = ViewProfilesController().view_all_profiles()
        profile_labels = {f"#{p.profile_id} — {p.role}": p.profile_id for p in profiles}
        try:
            current_profile_label = next(
                lbl for lbl, pid in profile_labels.items() if pid == current.profile_id
            )
        except StopIteration:
            current_profile_label = next(iter(profile_labels))

        try:
            dob_value = date.fromisoformat(current.dob) if current.dob else date(2000, 1, 1)
        except ValueError:
            dob_value = date(2000, 1, 1)

        with st.form("update_account_form"):
            email = st.text_input("Email", value=current.email)
            password = st.text_input("Password", value=current.password)
            name = st.text_input("Name", value=current.name)
            dob = st.date_input("Date of birth", value=dob_value, min_value=date(1900, 1, 1))
            phone_num = st.text_input("Phone number", value=current.phone_num or "")
            profile_label = st.selectbox(
                "Profile",
                list(profile_labels.keys()),
                index=list(profile_labels.keys()).index(current_profile_label),
            )
            suspended = st.checkbox("Suspended", value=current.suspended)
            cols = st.columns(2)
            submitted = cols[0].form_submit_button("Save changes", type="primary")
            cancelled = cols[1].form_submit_button("Cancel")

        if cancelled:
            st.session_state.pop(EDIT_KEY, None)
            st.rerun()
            return

        if not submitted:
            return

        if not self._validate(email, password, name, phone_num):
            return

        updated = UserAccount(
            email=email,
            password=password,
            name=name,
            dob=str(dob),
            phone_num=phone_num,
            profile_id=int(profile_labels[profile_label]),
            account_id=int(account_id),
            suspended=suspended,
        )
        success = UpdateUserAccountController().update_user_account(account_id, updated)
        if success:
            self.display_success()
            st.session_state.pop(EDIT_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def click_edit_option(account_id: str) -> None:
        st.session_state[EDIT_KEY] = account_id

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
        st.success("Account updated.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not update account.")
