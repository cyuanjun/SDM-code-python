"""ManageMyFundraisingActivityPage <<Boundary>> — UX consolidation.

NOT on any diagram. Combines US-13, 14, 15, 16, 17, 30, 31 into one
screen with two tabs (All / Completed). Each tab has its own search,
list, and detail view. Create form is inline above the tabs.

Logged in docs/diagram_typos.md as a UX deviation.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal, InvalidOperation

import streamlit as st

from controller.create_fundraising_activity_controller import (
    CreateFundraisingActivityController,
)
from controller.search_my_completed_fundraising_activity_controller import (
    SearchMyCompletedFundraisingActivityController,
)
from controller.search_my_fundraising_activity_controller import (
    SearchMyFundraisingActivityController,
)
from controller.suspend_my_fundraising_activity_controller import (
    SuspendMyFundraisingActivityController,
)
from controller.unsuspend_my_fundraising_activity_controller import (
    UnsuspendMyFundraisingActivityController,
)
from controller.update_my_fundraising_activity_controller import (
    UpdateMyFundraisingActivityController,
)
from controller.view_my_completed_activity_controller import (
    ViewMyCompletedActivityController,
)
from controller.view_my_fundraising_activity_controller import (
    ViewMyFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity

SELECTED_KEY = "manage_my_fra_selected_id"
EDIT_MODE_KEY = "manage_my_fra_edit_mode"
SELECTED_TAB_KEY = "manage_my_fra_selected_tab"  # "all" or "completed"
CREATE_MODE_KEY = "manage_my_fra_create_mode"
JUST_CREATED_KEY = "manage_my_fra_just_created"
ACTION_MSG_KEY = "manage_my_fra_action_msg"


class ManageMyFundraisingActivityPage:
    def render(self) -> None:
        if "user" not in st.session_state:
            st.header("Manage my fundraising activities")
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id

        if st.session_state.get(CREATE_MODE_KEY):
            self._render_create(owner_account_id)
            return

        if SELECTED_KEY in st.session_state:
            st.header("Manage my fundraising activities")
            if ACTION_MSG_KEY in st.session_state:
                self._render_action_confirmation()
                return
            self._render_detail(owner_account_id)
            return

        col_title, col_create = st.columns([4, 1])
        with col_title:
            st.header("Manage my fundraising activities")
        with col_create:
            st.write("")
            if st.button(
                "+ Create new activity",
                key="manage_my_fra_create_btn",
                use_container_width=True,
            ):
                st.session_state[CREATE_MODE_KEY] = True
                st.rerun()
        self._render_list(owner_account_id)

    # -------- Create view ----------------------------------------------------

    def _render_create(self, owner_account_id: str) -> None:
        st.header("Create fundraising activity")

        # Post-create confirmation.
        if JUST_CREATED_KEY in st.session_state:
            created = st.session_state[JUST_CREATED_KEY]
            st.success(
                "\n\n".join([
                    f"**Activity created: {created.fra_id}**",
                    f"**Title:** {created.title}",
                    f"**Description:** {created.description}",
                    f"**Target:** ${created.target_amount}",
                    f"**Category:** {created.category}",
                    f"**Runs:** {created.start_date.isoformat()} → "
                    f"{created.end_date.isoformat()}",
                    f"**Owner:** {created.owner_account_id}",
                    f"**Completed:** {'yes' if created.completed else 'no'}",
                    f"**Suspended:** {'yes' if created.suspended else 'no'}",
                ])
            )
            if st.button("← Back to my activities"):
                st.session_state.pop(CREATE_MODE_KEY, None)
                st.session_state.pop(JUST_CREATED_KEY, None)
                st.rerun()
            return

        with st.form("manage_my_fra_create_form"):
            title = st.text_input("Title")
            description = st.text_area("Description")
            target_amount_str = st.text_input("Target amount", value="0.00")
            category = st.text_input("Category")
            start_date = st.date_input("Start date", value=date.today())
            end_date = st.date_input("End date", value=date.today())
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
        if not self._validate_create(
            title, description, target_amount_str,
            category, start_date, end_date,
        ):
            st.error(
                "All fields required; target must be positive; "
                "start date must be on/before end date."
            )
            return

        new_activity = (
            CreateFundraisingActivityController().create_fundraising_activity(
                title=title.strip(),
                description=description.strip(),
                target_amount=Decimal(target_amount_str),
                category=category.strip(),
                start_date=start_date,
                end_date=end_date,
                owner_account_id=owner_account_id,
            )
        )
        st.session_state[JUST_CREATED_KEY] = new_activity
        st.rerun()

    # -------- List view ------------------------------------------------------

    def _render_list(self, owner_account_id: str) -> None:
        all_tab, completed_tab = st.tabs(["All", "Completed"])
        with all_tab:
            self._render_tab(owner_account_id, completed_only=False)
        with completed_tab:
            self._render_tab(owner_account_id, completed_only=True)

    def _render_tab(
        self, owner_account_id: str, completed_only: bool
    ) -> None:
        key_prefix = "completed" if completed_only else "all"
        search_term = st.text_input(
            "Search activities",
            placeholder="Title, description, or category…",
            key=f"manage_my_fra_search_{key_prefix}",
        )

        if completed_only:
            if search_term.strip():
                activities = (
                    SearchMyCompletedFundraisingActivityController()
                    .search_my_completed_fra(
                        owner_account_id=owner_account_id,
                        search_criteria=search_term.strip(),
                    )
                )
            else:
                all_mine = (
                    ViewMyFundraisingActivityController()
                    .view_my_fundraising_activities(
                        owner_account_id=owner_account_id
                    )
                )
                activities = [a for a in all_mine if a.completed]
        else:
            if search_term.strip():
                activities = (
                    SearchMyFundraisingActivityController()
                    .search_my_fundraising_activity(
                        owner_account_id=owner_account_id,
                        search_criteria=search_term.strip(),
                    )
                )
            else:
                activities = (
                    ViewMyFundraisingActivityController()
                    .view_my_fundraising_activities(
                        owner_account_id=owner_account_id
                    )
                )

        if not activities:
            st.info("No activities to show.")
            return

        st.caption(f"{len(activities)} activity(s) — click a row to view")
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": a.category,
                "Target": f"${a.target_amount}",
                "Start": a.start_date.isoformat(),
                "End": a.end_date.isoformat(),
                "Completed": "yes" if a.completed else "no",
                "Suspended": "yes" if a.suspended else "no",
            }
            for a in activities
        ]
        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key=f"manage_my_fra_table_{key_prefix}",
        )
        selected = event.selection.rows
        if selected:
            st.session_state[SELECTED_KEY] = activities[selected[0]].fra_id
            st.session_state[SELECTED_TAB_KEY] = (
                "completed" if completed_only else "all"
            )
            st.rerun()

    # -------- Detail view ----------------------------------------------------

    def _render_detail(self, owner_account_id: str) -> None:
        fra_id = st.session_state[SELECTED_KEY]
        tab = st.session_state.get(SELECTED_TAB_KEY, "all")

        if tab == "completed":
            current = (
                ViewMyCompletedActivityController()
                .view_my_completed_activity(
                    owner_account_id=owner_account_id, fra_id=fra_id,
                )
            )
        else:
            current = (
                ViewMyFundraisingActivityController()
                .view_my_fundraising_activity(
                    owner_account_id=owner_account_id, fra_id=fra_id,
                )
            )

        if current is None:
            st.error("Activity is not yours or no longer exists.")
            st.session_state.pop(SELECTED_KEY, None)
            return

        if st.session_state.get(EDIT_MODE_KEY):
            self._render_edit_form(current, owner_account_id)
        else:
            self._render_view(current, owner_account_id)

        if st.button("← Back to list"):
            st.session_state.pop(SELECTED_KEY, None)
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.session_state.pop(SELECTED_TAB_KEY, None)
            st.rerun()

    def _render_action_confirmation(self) -> None:
        st.success(st.session_state[ACTION_MSG_KEY])
        if st.button("← Back"):
            st.session_state.pop(ACTION_MSG_KEY, None)
            st.rerun()

    def _render_view(self, activity, owner_account_id: str) -> None:
        st.subheader(activity.title)
        st.write(f"**FRAId:** {activity.fra_id}")
        st.write(f"**Category:** {activity.category}")
        st.write(f"**Target:** ${activity.target_amount}")
        st.write(
            f"**Runs:** {activity.start_date.isoformat()} → "
            f"{activity.end_date.isoformat()}"
        )
        st.write(f"**Completed:** {'yes' if activity.completed else 'no'}")
        st.write(f"**Suspended:** {'yes' if activity.suspended else 'no'}")
        st.write(activity.description)

        col_metrics = st.columns(2)
        col_metrics[0].metric("Views", activity.view_count)
        col_metrics[1].metric("Saves", activity.save_count)

        col_update, col_suspend, _ = st.columns([1, 1, 4])
        with col_update:
            if (
                not activity.completed
                and st.button("✏️ Update", use_container_width=True)
            ):
                st.session_state[EDIT_MODE_KEY] = True
                st.rerun()
        with col_suspend:
            if activity.completed:
                pass  # completed activities aren't suspendable
            elif activity.suspended:
                if st.button(
                    "✅ Unsuspend donations", use_container_width=True
                ):
                    ok = (
                        UnsuspendMyFundraisingActivityController()
                        .unsuspend_my_fundraising_activity(
                            owner_account_id=owner_account_id,
                            fra_id=activity.fra_id,
                        )
                    )
                    if ok:
                        st.session_state[ACTION_MSG_KEY] = "Activity unsuspended."
                        st.rerun()
                    else:
                        st.error("Could not unsuspend.")
            else:
                if st.button(
                    "🚫 Suspend donations", use_container_width=True
                ):
                    ok = (
                        SuspendMyFundraisingActivityController()
                        .suspend_my_fundraising_activity(
                            owner_account_id=owner_account_id,
                            fra_id=activity.fra_id,
                        )
                    )
                    if ok:
                        st.session_state[ACTION_MSG_KEY] = "Activity suspended."
                        st.rerun()
                    else:
                        st.error("Could not suspend.")

    def _render_edit_form(self, activity, owner_account_id: str) -> None:
        st.subheader(activity.title)
        st.caption(f"Editing {activity.fra_id}")
        with st.form("manage_my_fra_edit_form"):
            title = st.text_input("Title", value=activity.title)
            description = st.text_area("Description", value=activity.description)
            target_amount_str = st.text_input(
                "Target amount", value=str(activity.target_amount)
            )
            category = st.text_input("Category", value=activity.category)
            start_date = st.date_input("Start date", value=activity.start_date)
            end_date = st.date_input("End date", value=activity.end_date)
            completed = st.checkbox("Completed", value=activity.completed)
            col_save, col_cancel, _ = st.columns([1, 1, 4])
            with col_save:
                submitted = st.form_submit_button(
                    "Save changes", use_container_width=True
                )
            with col_cancel:
                cancel = st.form_submit_button(
                    "Cancel", use_container_width=True
                )

        if cancel:
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.rerun()
            return
        if not submitted:
            return
        if not self._validate_create(
            title, description, target_amount_str, category, start_date, end_date,
        ):
            st.error("Invalid input.")
            return

        ok = UpdateMyFundraisingActivityController().update_fundraiser_activity(
            owner_account_id=owner_account_id,
            fra_id=activity.fra_id,
            updated_activity=FundraisingActivity(
                title=title.strip(),
                description=description.strip(),
                target_amount=Decimal(target_amount_str),
                category=category.strip(),
                start_date=start_date,
                end_date=end_date,
                owner_account_id=owner_account_id,
                completed=completed,
                suspended=activity.suspended,
            ),
        )
        if ok:
            st.session_state.pop(EDIT_MODE_KEY, None)
            st.session_state[ACTION_MSG_KEY] = "Activity updated."
            st.rerun()
        else:
            st.error("Update failed.")

    # -------- Validators -----------------------------------------------------

    @staticmethod
    def _validate_create(
        title: str, description: str, target_amount_str: str,
        category: str, start_date: date, end_date: date,
    ) -> bool:
        if not title.strip() or not description.strip() or not category.strip():
            return False
        try:
            amount = Decimal(target_amount_str)
        except (InvalidOperation, ValueError):
            return False
        return amount > 0 and start_date <= end_date
