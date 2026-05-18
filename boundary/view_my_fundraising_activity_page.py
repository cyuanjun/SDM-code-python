"""ViewMyFundraisingActivityPage <<Boundary>> — Sprint 2 US-14 + Sprint 3 US-16 + Sprint 4 US-28/29.

Diagram contracts:
    US-14.jpg: + displayMyFundraisingActivity(fundraisingActivity: FundraisingActivity): void
    US-16.jpg: + displaySuccess(): void  (suspend; class diagram names the
                                          donee's ViewFundraisingActivityPage
                                          — typo logged; this fundraiser page
                                          is the correct boundary.)
    US-28.jpg: + displayFundraisingActivityViewCount(viewCount: Integer): void
    US-29.jpg: + displayFundraisingActivitySaveCount(saveCount: Integer): void

Fundraiser-scoped. Requires login. US-16 adds the Suspend button on detail;
US-28/29 add the view/save count metrics — both pulled via their diagram-
defined controllers. Owner-scoping is implicit (this page is fundraiser-
only and only shows the caller's own activities), so no extra gate is
needed for the counts.
"""
from __future__ import annotations

import streamlit as st

from controller.suspend_my_fundraising_activity_controller import (
    SuspendMyFundraisingActivityController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_save_count_controller import (
    ViewFundraisingActivitySaveCountController,
)
from controller.view_fundraising_activity_view_count_controller import (
    ViewFundraisingActivityViewCountController,
)
from controller.view_my_fundraising_activity_controller import (
    ViewMyFundraisingActivityController,
)


def _category_lookup() -> dict[str, str]:
    cats = ViewFundraisingActivityCategoryController().view_all_categories()
    return {c.fra_cat_id: c.category_name for c in cats}

SELECTED_KEY = "view_my_fra_selected_id"


class ViewMyFundraisingActivityPage:
    def render(self) -> None:
        st.header("View My Fundraising Activity")

        if "user" not in st.session_state:
            st.warning("Please log in first.")
            return

        owner_account_id = st.session_state["user"].account_id
        controller = ViewMyFundraisingActivityController()

        if SELECTED_KEY in st.session_state:
            activity = controller.view_my_fundraising_activity(
                owner_account_id=owner_account_id,
                fra_id=st.session_state[SELECTED_KEY],
            )
            if activity is None:
                st.error(
                    "Selected activity no longer exists or is not yours."
                )
                st.session_state.pop(SELECTED_KEY, None)
            else:
                self.display_my_fundraising_activity(activity)
            if st.button("← Back to list"):
                st.session_state.pop(SELECTED_KEY, None)
                st.rerun()
            return

        activities = controller.view_my_fundraising_activities(
            owner_account_id=owner_account_id
        )
        if not activities:
            st.info("You have no fundraising activities yet.")
            return

        st.caption(f"{len(activities)} of your activities")
        cat_lookup = _category_lookup()
        rows = [
            {
                "ID": a.fra_id,
                "Title": a.title,
                "Category": cat_lookup.get(a.fra_cat_id, a.fra_cat_id),
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
        )
        selected = event.selection.rows
        if selected:
            st.session_state[SELECTED_KEY] = activities[selected[0]].fra_id
            st.rerun()

    def display_my_fundraising_activity(self, activity) -> None:
        st.subheader(activity.title)
        cat_name = _category_lookup().get(activity.fra_cat_id, activity.fra_cat_id)
        st.write(f"**FRAId:** {activity.fra_id}")
        st.write(f"**Category:** {cat_name}")
        st.write(f"**Target:** ${activity.target_amount}")
        st.write(
            f"**Runs:** {activity.start_date.isoformat()} → "
            f"{activity.end_date.isoformat()}"
        )
        st.write(f"**Completed:** {'yes' if activity.completed else 'no'}")
        st.write(f"**Suspended:** {'yes' if activity.suspended else 'no'}")
        st.write(activity.description)

        # US-28 / US-29: view and save counts, pulled via their diagram-
        # defined controllers (not read off the dataclass).
        view_count = (
            ViewFundraisingActivityViewCountController()
            .view_fundraising_activity_view_count(activity.fra_id)
        )
        save_count = (
            ViewFundraisingActivitySaveCountController()
            .view_fundraising_activity_save_count(activity.fra_id)
        )
        self.display_fundraising_activity_view_count(view_count)
        self.display_fundraising_activity_save_count(save_count)

        # US-16: suspend my activity (only when not already suspended).
        if not activity.suspended:
            user = st.session_state.get("user")
            if user is not None and st.button("🚫 Suspend"):
                ok = (
                    SuspendMyFundraisingActivityController()
                    .suspend_my_fundraising_activity(
                        owner_account_id=user.account_id,
                        fra_id=activity.fra_id,
                    )
                )
                if ok:
                    self.display_success()
                    st.rerun()
                else:
                    self.display_error()

    @staticmethod
    def display_fundraising_activity_view_count(view_count: int) -> None:
        st.metric("Views", view_count)

    @staticmethod
    def display_fundraising_activity_save_count(save_count: int) -> None:
        st.metric("Saves to favourites", save_count)

    @staticmethod
    def display_success() -> None:
        st.success("Activity suspended.")

    @staticmethod
    def display_error() -> None:
        st.error("Could not suspend activity.")
