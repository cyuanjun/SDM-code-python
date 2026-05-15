"""ManageUserAccountPage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines US-6, 7, 8, 9, 10 (account CRUD + suspend
+ search) into one Search / List / Detail / Update / Suspend screen, with
a Create form expanded inline at the top. Per the 2026-05-15 sketch.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from controller.create_account_controller import CreateAccountController
from controller.search_user_account_controller import (
    SearchUserAccountController,
)
from controller.suspend_user_account_controller import (
    SuspendUserAccountController,
)
from controller.unsuspend_user_account_controller import (
    UnsuspendUserAccountController,
)
from controller.update_user_account_controller import (
    UpdateUserAccountController,
)
from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_account_controller import ViewUserAccountController
from entity.user_account import UserAccount

SELECTED_KEY = "manage_account_selected_id"
EDIT_MODE_KEY = "manage_account_edit_mode"
CREATE_MODE_KEY = "manage_account_create_mode"
JUST_CREATED_ID_KEY = "manage_account_just_created_id"


class ManageUserAccountPage:
    def render(self) -> None:
        if st.session_state.get(CREATE_MODE_KEY):
            self._render_create()
            return

        if SELECTED_KEY in st.session_state:
            st.header("Manage user accounts")
            self._render_detail()
            return

        col_title, col_create = st.columns([4, 1])
        with col_title:
            st.header("Manage user accounts")
        with col_create:
            st.write("")
            if st.button("➕ Create new account", key="manage_account_create_btn"):
                st.session_state[CREATE_MODE_KEY] = True
                st.rerun()
        self._render_list()

    # -------- Create view ----------------------------------------------------

    def _render_create(self) -> None:
        st.header("Create user account")

        # Post-create confirmation.
        if JUST_CREATED_ID_KEY in st.session_state:
            new_id = st.session_state[JUST_CREATED_ID_KEY]
            st.success(f"Account created: {new_id}")
            if st.button("← Back to accounts"):
                st.session_state.pop(CREATE_MODE_KEY, None)
                st.session_state.pop(JUST_CREATED_ID_KEY, None)
                st.rerun()
            return

        profiles = ViewProfilesController().view_all_profiles()

        if not profiles:
            st.warning(
                "No profiles exist yet. Create a user profile first."
            )
            if st.button("← Back"):
                st.session_state.pop(CREATE_MODE_KEY, None)
                st.rerun()
            return

        with st.form("manage_account_create_form"):
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
            profile_options = {
                f"{p.profile_id} — {p.role}": p.profile_id for p in profiles
            }
            profile_label = st.selectbox(
                "Profile", list(profile_options.keys())
            )
            col_submit, col_cancel = st.columns(2)
            with col_submit:
                submitted = st.form_submit_button("Create")
            with col_cancel:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state.pop(CREATE_MODE_KEY, None)
            st.rerun()
            return
        if not submitted:
            return
        if not self._validate_create(email, password, name, phone_num):
            st.error(
                "Email must contain '@', and email, password, name, "
                "and phone are all required."
            )
            return

        new_account = CreateAccountController().create_account(
            email=email.strip(), password=password, name=name.strip(),
            dob=dob, phone_num=phone_num.strip(),
            profile_id=profile_options[profile_label],
        )
        st.session_state[JUST_CREATED_ID_KEY] = new_account.account_id
        st.rerun()

    # -------- List view ------------------------------------------------------

    def _render_list(self) -> None:
        search_term = st.text_input(
            "Search accounts", placeholder="Email or name…"
        )
        if search_term.strip():
            accounts = SearchUserAccountController().search_user_account(
                search_term.strip()
            )
        else:
            accounts = ViewUserAccountController().view_all_user_accounts()

        if not accounts:
            st.info("No accounts match." if search_term.strip() else "No accounts yet.")
            return

        st.caption(f"{len(accounts)} account(s) — click a row to view details")
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

    # -------- Detail view ----------------------------------------------------

    def _render_detail(self) -> None:
        account_id = st.session_state[SELECTED_KEY]
        current = ViewUserAccountController().view_user_account(account_id)
        if current is None:
            st.error("Account no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        if st.session_state.get(EDIT_MODE_KEY):
            self._render_edit_form(current)
        else:
            self._render_view(current)

        if st.button("← Back to list"):
            st.session_state.pop(SELECTED_KEY, None)
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.rerun()

    def _render_view(self, account) -> None:
        st.subheader(account.name)
        st.write(f"**Account ID:** {account.account_id}")
        st.write(f"**Email:** {account.email}")
        st.write(f"**Date of birth:** {account.dob.isoformat()}")
        st.write(f"**Phone:** {account.phone_num}")
        st.write(f"**Profile:** {account.profile_id}")
        st.write(f"**Suspended:** {'yes' if account.suspended else 'no'}")

        col_update, col_suspend, _ = st.columns([1, 1, 4])
        with col_update:
            if st.button("✏️ Update"):
                st.session_state[EDIT_MODE_KEY] = True
                st.rerun()
        with col_suspend:
            if account.suspended:
                if st.button("✅ Unsuspend"):
                    ok = (
                        UnsuspendUserAccountController()
                        .unsuspend_user_account(account.account_id)
                    )
                    if ok:
                        st.success("Account unsuspended.")
                        st.rerun()
                    else:
                        st.error("Could not unsuspend account.")
            else:
                if st.button("🚫 Suspend"):
                    ok = SuspendUserAccountController().suspend_user_account(
                        account.account_id
                    )
                    if ok:
                        st.success("Account suspended.")
                        st.rerun()
                    else:
                        st.error("Could not suspend account.")

    def _render_edit_form(self, account) -> None:
        profiles = ViewProfilesController().view_all_profiles()
        profile_options = {
            f"{p.profile_id} — {p.role}": p.profile_id for p in profiles
        }
        current_label = next(
            (label for label, pid in profile_options.items()
             if pid == account.profile_id),
            list(profile_options.keys())[0] if profile_options else None,
        )

        with st.form("manage_account_edit_form"):
            st.write(f"**Editing:** {account.account_id}")
            email = st.text_input("Email", value=account.email)
            password = st.text_input(
                "Password", value=account.password, type="password"
            )
            name = st.text_input("Name", value=account.name)
            dob = st.date_input(
                "Date of birth", value=account.dob,
                min_value=date(1900, 1, 1), max_value=date.today(),
            )
            phone_num = st.text_input("Phone number", value=account.phone_num)
            profile_label = st.selectbox(
                "Profile",
                list(profile_options.keys()),
                index=list(profile_options.keys()).index(current_label)
                if current_label in profile_options else 0,
            )
            suspended = st.checkbox("Suspended", value=account.suspended)
            col_save, col_cancel = st.columns(2)
            with col_save:
                submitted = st.form_submit_button("Save changes")
            with col_cancel:
                cancel = st.form_submit_button("Cancel")

        if cancel:
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.rerun()
            return
        if not submitted:
            return
        if not self._validate_update(email, password, name, phone_num):
            st.error("Invalid input.")
            return

        ok = UpdateUserAccountController().update_user_account(
            account.account_id,
            UserAccount(
                email=email.strip(), password=password, name=name.strip(),
                dob=dob, phone_num=phone_num.strip(),
                profile_id=profile_options[profile_label],
                suspended=suspended,
            ),
        )
        if ok:
            st.success("Account updated.")
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.rerun()
        else:
            st.error("Update failed.")

    # -------- Validators -----------------------------------------------------

    @staticmethod
    def _validate_create(
        email: str, password: str, name: str, phone_num: str
    ) -> bool:
        if not email.strip() or "@" not in email:
            return False
        return bool(password) and bool(name.strip()) and bool(phone_num.strip())

    @staticmethod
    def _validate_update(
        email: str, password: str, name: str, phone_num: str
    ) -> bool:
        if not email.strip() or "@" not in email:
            return False
        return bool(password) and bool(name.strip()) and bool(phone_num.strip())
