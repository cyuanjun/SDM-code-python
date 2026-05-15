"""ManageFundraisingActivityCategoryPage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines US-34, 35, 36, 37, 38 (FRA category CRUD)
into one Search/List/Detail/Update/Suspend screen with an inline Create
form at the top.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

import streamlit as st

from controller.create_fundraising_activity_category_controller import (
    CreateFundraisingActivityCategoryController,
)
from controller.search_fundraising_activity_category_controller import (
    SearchFundraisingActivityCategoryController,
)
from controller.suspend_fundraising_activity_category_controller import (
    SuspendFundraisingActivityCategoryController,
)
from controller.unsuspend_fundraising_activity_category_controller import (
    UnsuspendFundraisingActivityCategoryController,
)
from controller.update_fundraising_activity_category_controller import (
    UpdateFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)
from entity.fundraising_activity_category import FundraisingActivityCategory

SELECTED_KEY = "manage_fra_cat_selected_id"
EDIT_MODE_KEY = "manage_fra_cat_edit_mode"
CREATE_MODE_KEY = "manage_fra_cat_create_mode"
JUST_CREATED_KEY = "manage_fra_cat_just_created"
ACTION_MSG_KEY = "manage_fra_cat_action_msg"
PENDING_ACTION_KEY = "manage_fra_cat_pending_action"


@st.dialog("Confirm")
def _confirm_suspend_dialog(action: str, fra_cat_id: str) -> None:
    """Popup confirmation for suspend / unsuspend on an FRA category."""
    verb = action
    st.write(f"Are you sure you want to **{verb}** category `{fra_cat_id}`?")
    col_cancel, col_confirm = st.columns(2)
    with col_cancel:
        if st.button(
            "Cancel",
            use_container_width=True,
            key=f"_cat_dlg_cancel_{action}",
        ):
            st.session_state.pop(PENDING_ACTION_KEY, None)
            st.rerun()
    with col_confirm:
        if st.button(
            "Confirm",
            type="primary",
            use_container_width=True,
            key=f"_cat_dlg_confirm_{action}",
        ):
            if action == "suspend":
                ok = (
                    SuspendFundraisingActivityCategoryController()
                    .suspend_fundraising_activity_category(fra_cat_id)
                )
                msg = "Category suspended."
            else:
                ok = (
                    UnsuspendFundraisingActivityCategoryController()
                    .unsuspend_fundraising_activity_category(fra_cat_id)
                )
                msg = "Category unsuspended."
            st.session_state.pop(PENDING_ACTION_KEY, None)
            if ok:
                st.session_state[ACTION_MSG_KEY] = msg
            st.rerun()


class ManageFundraisingActivityCategoryPage:
    def render(self) -> None:
        if st.session_state.get(CREATE_MODE_KEY):
            self._render_create()
            return

        if SELECTED_KEY in st.session_state:
            st.header("Manage fundraising activity categories")
            if (
                ACTION_MSG_KEY in st.session_state
                and not st.session_state.get(EDIT_MODE_KEY)
            ):
                self._render_action_confirmation()
                return
            self._render_detail()
            pending = st.session_state.get(PENDING_ACTION_KEY)
            if pending:
                _confirm_suspend_dialog(
                    pending, st.session_state[SELECTED_KEY]
                )
            return

        col_title, col_create = st.columns([4, 1])
        with col_title:
            st.header("Manage fundraising activity categories")
        with col_create:
            st.write("")
            if st.button(
                "+ Create new category",
                key="manage_fra_cat_create_btn",
                use_container_width=True,
            ):
                st.session_state[CREATE_MODE_KEY] = True
                st.rerun()
        self._render_list()

    def _render_create(self) -> None:
        st.header("Create fundraising activity category")

        # Post-create confirmation.
        if JUST_CREATED_KEY in st.session_state:
            created = st.session_state[JUST_CREATED_KEY]
            st.success(
                "\n\n".join([
                    f"**Category created: {created.fra_cat_id}**",
                    f"**Name:** {created.category_name}",
                    f"**Description:** {created.description or '(none)'}",
                    f"**Suspended:** {'yes' if created.suspended else 'no'}",
                ])
            )
            if st.button("← Back to categories"):
                st.session_state.pop(CREATE_MODE_KEY, None)
                st.session_state.pop(JUST_CREATED_KEY, None)
                st.rerun()
            return

        with st.form("manage_fra_cat_create_form"):
            name = st.text_input("Category name")
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
        if not self._validate(name, description):
            st.error("Both category name and description are required.")
            return

        new_category = (
            CreateFundraisingActivityCategoryController().create_category(
                category_name=name.strip(),
                description=description.strip(),
            )
        )
        st.session_state[JUST_CREATED_KEY] = new_category
        st.rerun()

    def _render_list(self) -> None:
        search_term = st.text_input(
            "Search categories", placeholder="Name or description…"
        )
        view_controller = ViewFundraisingActivityCategoryController()
        if search_term.strip():
            cats = (
                SearchFundraisingActivityCategoryController()
                .search_fundraising_activity_category(search_term.strip())
            )
        else:
            cats = view_controller.view_all_categories()

        if not cats:
            st.info(
                "No categories match." if search_term.strip()
                else "No categories yet."
            )
            return

        st.caption(f"{len(cats)} category(s) — click a row to view")
        rows = [
            {
                "ID": c.fra_cat_id,
                "Name": c.category_name,
                "Description": c.description,
                "Suspended": "yes" if c.suspended else "no",
            }
            for c in cats
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
            st.session_state[SELECTED_KEY] = cats[selected[0]].fra_cat_id
            st.rerun()

    def _render_detail(self) -> None:
        fra_cat_id = st.session_state[SELECTED_KEY]
        current = (
            ViewFundraisingActivityCategoryController()
            .view_fundraising_activity_category(fra_cat_id)
        )
        if current is None:
            st.error("Category no longer exists.")
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

    def _render_view(self, category) -> None:
        st.subheader(category.category_name)
        st.write(f"**ID:** {category.fra_cat_id}")
        st.write(f"**Description:** {category.description or '(none)'}")
        st.write(f"**Suspended:** {'yes' if category.suspended else 'no'}")

        col_update, col_suspend, _ = st.columns([1, 1, 4])
        with col_update:
            if st.button("✏️ Update", use_container_width=True):
                st.session_state[EDIT_MODE_KEY] = True
                st.rerun()
        with col_suspend:
            if category.suspended:
                if st.button("✅ Unsuspend", use_container_width=True):
                    st.session_state[PENDING_ACTION_KEY] = "unsuspend"
                    st.rerun()
            else:
                if st.button("🚫 Suspend", use_container_width=True):
                    st.session_state[PENDING_ACTION_KEY] = "suspend"
                    st.rerun()

    def _render_edit_form(self, category) -> None:
        st.subheader(category.category_name)
        st.caption(f"Editing {category.fra_cat_id}")
        is_completed = ACTION_MSG_KEY in st.session_state

        with st.form("manage_fra_cat_edit_form"):
            name = st.text_input(
                "Category name",
                value=category.category_name,
                disabled=is_completed,
            )
            description = st.text_area(
                "Description",
                value=category.description,
                disabled=is_completed,
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
            st.success(st.session_state[ACTION_MSG_KEY])
            if st.button("← Back", key="manage_fra_cat_edit_back"):
                st.session_state.pop(EDIT_MODE_KEY, None)
                st.session_state.pop(ACTION_MSG_KEY, None)
                st.rerun()
            return

        if cancel:
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.rerun()
            return
        if not submitted:
            return
        if not self._validate(name, description):
            st.error("Both name and description are required.")
            return

        ok = (
            UpdateFundraisingActivityCategoryController()
            .update_fundraising_activity_category(
                fra_cat_id=category.fra_cat_id,
                updated_category=FundraisingActivityCategory(
                    category_name=name.strip(),
                    description=description.strip(),
                    suspended=category.suspended,
                ),
            )
        )
        if ok:
            st.session_state[ACTION_MSG_KEY] = "Category updated."
            st.rerun()
        else:
            st.error("Update failed.")

    @staticmethod
    def _validate(name: str, description: str) -> bool:
        return bool(name.strip()) and bool(description.strip())
