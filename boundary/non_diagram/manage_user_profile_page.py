"""ManageUserProfilePage <<Boundary>>."""
from __future__ import annotations

import streamlit as st

from controller.create_profile_controller import CreateProfileController
from controller.search_user_profile_controller import (
    SearchUserProfileController,
)
from controller.suspend_user_profile_controller import (
    SuspendUserProfileController,
)
from controller.non_diagram.unsuspend_user_profile_controller import (
    UnsuspendUserProfileController,
)
from controller.update_user_profile_controller import (
    UpdateUserProfileController,
)
from controller.non_diagram.view_profiles_controller import ViewProfilesController
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
            in_edit = bool(st.session_state.get(EDIT_MODE_KEY))
            title = "Update User Profile" if in_edit else "View User Profile"
            self._render_detail_header(title)
            self._render_detail()
            return

        col_title, col_create = st.columns([4, 1])
        with col_title:
            st.header("Manage User Profiles")
        with col_create:
            st.write("")
            if st.button(
                "+ Create new user profile",
                key="manage_profile_create_btn",
                use_container_width=True,
            ):
                st.session_state[CREATE_MODE_KEY] = True
                st.rerun()
        self._render_list()

    def _render_create(self) -> None:
        st.header("Create User Profile")

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
            col_submit, col_cancel, _ = st.columns([1, 1, 4])
            with col_submit:
                submitted = st.form_submit_button(
                    "Create", use_container_width=True
                )
            with col_cancel:
                cancel = st.form_submit_button(
                    "Cancel", use_container_width=True
                )

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
        if new_profile is None:
            st.error("A profile with that role already exists.")
            return
        st.session_state[JUST_CREATED_KEY] = new_profile
        st.rerun()

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

        self._render_bottom_bar()

    def _render_detail_header(self, title: str) -> None:
        msg = st.session_state.get(ACTION_MSG_KEY)
        if not msg:
            st.header(title)
            return
        st.markdown(
            f'<div style="display:flex; align-items:center; gap:1rem; '
            f'flex-wrap:wrap; margin:0 0 1rem 0;">'
            f'<h2 style="margin:0; padding:0;">{title}</h2>'
            f'<div style="background-color:rgba(45,195,99,0.18); '
            f'color:rgb(73,197,100); padding:0.5rem 1rem; '
            f'border-radius:0.5rem; font-size:1rem; '
            f'text-align:center; white-space:nowrap;">{msg}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    def _render_bottom_bar(self) -> None:
        in_edit = bool(st.session_state.get(EDIT_MODE_KEY))
        st.divider()
        cols = st.columns([1, 1, 4])
        with cols[0]:
            label = "← Back to profile" if in_edit else "← Back to list"
            if st.button(
                label,
                key=f"manage_profile_back_{in_edit}",
                use_container_width=True,
            ):
                st.session_state.pop(EDIT_MODE_KEY, None)
                st.session_state.pop(ACTION_MSG_KEY, None)
                if not in_edit:
                    st.session_state.pop(SELECTED_KEY, None)
                st.rerun()

    def _render_view(self, profile) -> None:
        st.write(f"**Profile ID:** {profile.profile_id}")
        st.write(f"**Role:** {profile.role}")
        st.write(f"**Description:** {profile.description or '(none)'}")
        st.write(f"**Suspended:** {'yes' if profile.suspended else 'no'}")

        col_update, col_suspend, _ = st.columns([1, 1, 4])
        with col_update:
            if st.button("✏️ Update", use_container_width=True):
                st.session_state[EDIT_MODE_KEY] = True
                st.session_state.pop(ACTION_MSG_KEY, None)
                st.rerun()
        with col_suspend:
            if profile.suspended:
                if st.button("✅ Unsuspend", use_container_width=True):
                    ok = (
                        UnsuspendUserProfileController()
                        .unsuspend_user_profile(profile.profile_id)
                    )
                    if ok:
                        st.session_state[ACTION_MSG_KEY] = "Profile unsuspended"
                        st.rerun()
                    else:
                        st.error("Could not unsuspend profile.")
            else:
                if st.button("🚫 Suspend", use_container_width=True):
                    ok = SuspendUserProfileController().suspend_user_profile(
                        profile.profile_id
                    )
                    if ok:
                        st.session_state[ACTION_MSG_KEY] = "Profile suspended"
                        st.rerun()
                    else:
                        st.error("Could not suspend profile.")

    def _render_edit_form(self, profile) -> None:
        st.write(f"**Editing:** {profile.profile_id}")
        is_completed = ACTION_MSG_KEY in st.session_state

        with st.form("manage_profile_edit_form"):
            role = st.text_input(
                "Role", value=profile.role, disabled=is_completed
            )
            description = st.text_area(
                "Description", value=profile.description, disabled=is_completed
            )
            col_save, col_cancel, _ = st.columns([1, 1, 4])
            with col_save:
                submitted = st.form_submit_button(
                    "Save changes",
                    use_container_width=True,
                    disabled=is_completed,
                )
            with col_cancel:
                cancel = st.form_submit_button(
                    "Cancel",
                    use_container_width=True,
                    disabled=is_completed,
                )

        if is_completed:
            return

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
                suspended=profile.suspended,
            ),
        )
        if ok:
            st.session_state[ACTION_MSG_KEY] = "Profile updated"
            st.rerun()
        else:
            st.error("Update failed.")

    @staticmethod
    def _validate_create(role: str, description: str) -> bool:
        return bool(role.strip()) and bool(description.strip())

    @staticmethod
    def _validate_update(role: str, description: str) -> bool:
        return bool(role.strip()) and bool(description.strip())
