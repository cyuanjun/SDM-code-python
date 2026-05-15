"""ManageUserProfilePage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines five US into one screen per the hand-drawn
sketch (2026-05-15): Search → List → View → Update / Suspend, with a
Create form expanded inline at the top.

Diagram-defined Boundary classes for US-1/2/3/4/5 are kept as testable
artifacts. This combined page calls the same controllers directly.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

import streamlit as st

from controller.create_profile_controller import CreateProfileController
from controller.search_user_profile_controller import (
    SearchUserProfileController,
)
from controller.suspend_user_profile_controller import (
    SuspendUserProfileController,
)
from controller.unsuspend_user_profile_controller import (
    UnsuspendUserProfileController,
)
from controller.update_user_profile_controller import (
    UpdateUserProfileController,
)
from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_profile_controller import ViewUserProfileController
from entity.user_profile import UserProfile

SELECTED_KEY = "manage_profile_selected_id"
EDIT_MODE_KEY = "manage_profile_edit_mode"
CREATE_MODE_KEY = "manage_profile_create_mode"
JUST_CREATED_KEY = "manage_profile_just_created"
ACTION_MSG_KEY = "manage_profile_action_msg"


class ManageUserProfilePage:
    def render(self) -> None:
        if st.session_state.get(CREATE_MODE_KEY):
            self._render_create()
            return

        if SELECTED_KEY in st.session_state:
            st.header("Manage user profiles")
            if ACTION_MSG_KEY in st.session_state:
                self._render_action_confirmation()
                return
            self._render_detail()
            return

        # List view — title on left, Create button on right.
        col_title, col_create = st.columns([4, 1])
        with col_title:
            st.header("Manage user profiles")
        with col_create:
            st.write("")  # vertical spacer to align with the header
            if st.button(
                "+ Create new profile",
                key="manage_profile_create_btn",
                use_container_width=True,
            ):
                st.session_state[CREATE_MODE_KEY] = True
                st.rerun()
        self._render_list()

    # -------- Create view ----------------------------------------------------

    def _render_create(self) -> None:
        st.header("Create user profile")

        # Post-create confirmation: shown after a successful create.
        if JUST_CREATED_KEY in st.session_state:
            created = st.session_state[JUST_CREATED_KEY]
            st.success(
                "\n\n".join([
                    f"**Profile created: {created.profile_id}**",
                    f"**Role:** {created.role}",
                    f"**Description:** {created.description or '(none)'}",
                    f"**Suspended:** {'yes' if created.suspended else 'no'}",
                ])
            )
            if st.button("← Back to profiles"):
                st.session_state.pop(CREATE_MODE_KEY, None)
                st.session_state.pop(JUST_CREATED_KEY, None)
                st.rerun()
            return

        with st.form("manage_profile_create_form"):
            role = st.text_input("Role")
            description = st.text_area("Description")
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
        if not self._validate_create(role, description):
            st.error("Role and description are both required.")
            return

        new_profile = CreateProfileController().create_profile(
            role=role.strip(), description=description.strip()
        )
        st.session_state[JUST_CREATED_KEY] = new_profile
        st.rerun()

    # -------- List view ------------------------------------------------------

    def _render_list(self) -> None:
        search_term = st.text_input(
            "Search profiles", placeholder="Role or description…"
        )
        if search_term.strip():
            profiles = SearchUserProfileController().search_user_profile(
                search_term.strip()
            )
        else:
            profiles = ViewProfilesController().view_all_profiles()

        if not profiles:
            st.info("No profiles match." if search_term.strip() else "No profiles yet.")
            return

        st.caption(f"{len(profiles)} profile(s) — click a row to view details")
        rows = [
            {
                "ID": p.profile_id,
                "Role": p.role,
                "Description": p.description,
                "Suspended": "yes" if p.suspended else "no",
            }
            for p in profiles
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
            st.session_state[SELECTED_KEY] = profiles[selected[0]].profile_id
            st.rerun()

    # -------- Detail view ----------------------------------------------------

    def _render_detail(self) -> None:
        profile_id = st.session_state[SELECTED_KEY]
        current = ViewUserProfileController().view_user_profile(profile_id)
        if current is None:
            st.error("Profile no longer exists.")
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

    def _render_action_confirmation(self) -> None:
        st.success(st.session_state[ACTION_MSG_KEY])
        if st.button("← Back"):
            st.session_state.pop(ACTION_MSG_KEY, None)
            st.rerun()

    def _render_view(self, profile) -> None:
        st.subheader(profile.role)
        st.write(f"**Profile ID:** {profile.profile_id}")
        st.write(f"**Description:** {profile.description or '(none)'}")
        st.write(f"**Suspended:** {'yes' if profile.suspended else 'no'}")

        col_update, col_suspend, _ = st.columns([1, 1, 4])
        with col_update:
            if st.button("✏️ Update", use_container_width=True):
                st.session_state[EDIT_MODE_KEY] = True
                st.rerun()
        with col_suspend:
            if profile.suspended:
                if st.button("✅ Unsuspend", use_container_width=True):
                    ok = (
                        UnsuspendUserProfileController()
                        .unsuspend_user_profile(profile.profile_id)
                    )
                    if ok:
                        st.session_state[ACTION_MSG_KEY] = "Profile unsuspended."
                        st.rerun()
                    else:
                        st.error("Could not unsuspend profile.")
            else:
                if st.button("🚫 Suspend", use_container_width=True):
                    ok = SuspendUserProfileController().suspend_user_profile(
                        profile.profile_id
                    )
                    if ok:
                        st.session_state[ACTION_MSG_KEY] = "Profile suspended."
                        st.rerun()
                    else:
                        st.error("Could not suspend profile.")

    def _render_edit_form(self, profile) -> None:
        with st.form("manage_profile_edit_form"):
            st.write(f"**Editing:** {profile.profile_id}")
            role = st.text_input("Role", value=profile.role)
            description = st.text_area("Description", value=profile.description)
            suspended = st.checkbox("Suspended", value=profile.suspended)
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
        if not self._validate_update(role, description):
            st.error("Role and description are both required.")
            return

        ok = UpdateUserProfileController().update_user_profile(
            profile.profile_id,
            UserProfile(
                role=role.strip(),
                description=description.strip(),
                suspended=suspended,
            ),
        )
        if ok:
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.session_state[ACTION_MSG_KEY] = "Profile updated."
            st.rerun()
        else:
            st.error("Update failed.")

    # -------- Validators -----------------------------------------------------

    @staticmethod
    def _validate_create(role: str, description: str) -> bool:
        return bool(role.strip()) and bool(description.strip())

    @staticmethod
    def _validate_update(role: str, description: str) -> bool:
        return bool(role.strip()) and bool(description.strip())
