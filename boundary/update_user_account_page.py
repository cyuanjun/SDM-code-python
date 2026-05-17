"""UpdateUserAccountPage <<Boundary>> — Sprint 2 US-8.

Diagram contract (US-08.jpg):
    + displaySuccess(): void
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from controller.update_user_account_controller import (
    UpdateUserAccountController,
)
from controller.non_diagram.view_profiles_controller import ViewProfilesController
from controller.view_user_account_controller import ViewUserAccountController
from entity.user_account import UserAccount

SELECTED_KEY = "update_account_selected_id"


class UpdateUserAccountPage:
    def render(self) -> None:
        st.header("Update User Account")

        if SELECTED_KEY not in st.session_state:
            self._render_picker()
            return

        controller = ViewUserAccountController()
        current = controller.view_user_account(st.session_state[SELECTED_KEY])
        if current is None:
            st.error("Selected account no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        profiles = ViewProfilesController().view_all_profiles()
        profile_options = {
            f"{p.profile_id} — {p.role}": p.profile_id for p in profiles
        }
        current_label = next(
            (label for label, pid in profile_options.items()
             if pid == current.profile_id),
            list(profile_options.keys())[0] if profile_options else None,
        )

        with st.form("update_account_form"):
            st.write(f"**Editing:** {current.account_id}")
            email = st.text_input("Email", value=current.email)
            password = st.text_input(
                "Password", value=current.password, type="password"
            )
            name = st.text_input("Name", value=current.name)
            dob = st.date_input(
                "Date of birth",
                value=current.dob,
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            phone_num = st.text_input("Phone number", value=current.phone_num)
            profile_label = st.selectbox(
                "Profile",
                list(profile_options.keys()),
                index=list(profile_options.keys()).index(current_label)
                if current_label in profile_options else 0,
            )
            suspended = st.checkbox("Suspended", value=current.suspended)

            col_a, col_b = st.columns(2)
            with col_a:
                submitted = st.form_submit_button("Save changes")
            with col_b:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state.pop(SELECTED_KEY, None)
            st.rerun()
            return

        if not submitted:
            return

        if not self.validate_account(email, password, name, phone_num):
            self.display_error()
            return

        ok = UpdateUserAccountController().update_user_account(
            st.session_state[SELECTED_KEY],
            UserAccount(
                email=email.strip(),
                password=password,
                name=name.strip(),
                dob=dob,
                phone_num=phone_num.strip(),
                profile_id=profile_options[profile_label],
                suspended=suspended,
            ),
        )
        if ok:
            self.display_success()
            st.session_state.pop(SELECTED_KEY, None)
        else:
            self.display_error()

    @staticmethod
    def _render_picker() -> None:
        accounts = ViewUserAccountController().view_all_user_accounts()
        if not accounts:
            st.info("No user accounts yet — create one first.")
            return

        st.caption("Pick an account to update.")
        rows = [
            {
                "ID": a.account_id,
                "Email": a.email,
                "Name": a.name,
                "Profile": a.profile_id,
                "Suspended": "yes" if a.suspended else "no",
            }
            for a in accounts
        ]
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
        )
        selected = event.selection.rows
        if selected:
            st.session_state[SELECTED_KEY] = accounts[selected[0]].account_id
            st.rerun()

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
    def display_success() -> None:
        st.success("Account updated.")

    @staticmethod
    def display_error() -> None:
        st.error(
            "Update failed. Email must contain '@', and email, password, "
            "name, and phone number are all required."
        )
