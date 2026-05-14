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
from controller.update_user_profile_controller import (
    UpdateUserProfileController,
)
from controller.view_profiles_controller import ViewProfilesController
from controller.view_user_profile_controller import ViewUserProfileController
from entity.user_profile import UserProfile

SELECTED_KEY = "manage_profile_selected_id"
EDIT_MODE_KEY = "manage_profile_edit_mode"


class ManageUserProfilePage:
    def render(self) -> None:
        st.header("Manage user profiles")

        if SELECTED_KEY in st.session_state:
            self._render_detail()
        else:
            self._render_list()

    # -------- List view ------------------------------------------------------

    def _render_list(self) -> None:
        with st.expander("➕ Create new profile"):
            with st.form("manage_profile_create_form"):
                role = st.text_input("Role")
                description = st.text_area("Description")
                if st.form_submit_button("Create"):
                    if self._validate_create(role, description):
                        CreateProfileController().create_profile(
                            role=role.strip(), description=description.strip()
                        )
                        st.success("Profile created.")
                        st.rerun()
                    else:
                        st.error("Role and description are both required.")

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

    def _render_view(self, profile) -> None:
        st.subheader(profile.role)
        st.write(f"**Profile ID:** {profile.profile_id}")
        st.write(f"**Description:** {profile.description or '(none)'}")
        st.write(f"**Suspended:** {'yes' if profile.suspended else 'no'}")

        col_update, col_suspend, _ = st.columns([1, 1, 4])
        with col_update:
            if st.button("✏️ Update"):
                st.session_state[EDIT_MODE_KEY] = True
                st.rerun()
        with col_suspend:
            if not profile.suspended and st.button("🚫 Suspend"):
                ok = SuspendUserProfileController().suspend_user_profile(
                    profile.profile_id
                )
                if ok:
                    st.success("Profile suspended.")
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
            st.success("Profile updated.")
            st.session_state.pop(EDIT_MODE_KEY, None)
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
