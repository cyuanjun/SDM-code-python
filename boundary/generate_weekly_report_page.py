"""GenerateWeeklyReportPage <<Boundary>> — Sprint 4 diagram US-42."""
from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from controller.generate_weekly_report_controller import GenerateWeeklyReportController


class GenerateWeeklyReportPage:
    def render(self) -> None:
        st.header("Generate weekly report")
        if "user" not in st.session_state:
            st.warning("Log in to generate a report.")
            return
        today = date.today()
        default_start = today - timedelta(days=6)
        cols = st.columns(2)
        start_date = cols[0].date_input("Start date", value=default_start)
        end_date = cols[1].date_input("End date", value=today)

        if start_date > end_date:
            st.error("Start date must be on or before end date.")
            return

        if st.button("Generate weekly report", type="primary"):
            self.click_generate_weekly_report_button(
                start_date.isoformat(),
                end_date.isoformat(),
                st.session_state["user"].account_id,
            )

    def click_generate_weekly_report_button(
        self, start_date: str, end_date: str, platform_manager_id: int
    ) -> None:
        report = GenerateWeeklyReportController().generate_weekly_report(
            start_date, end_date, platform_manager_id
        )
        self.display_report(report)

    @staticmethod
    def display_report(report) -> None:
        st.subheader(f"Weekly report — {report.start_date} to {report.end_date}")
        st.caption(
            f"Generated at {report.generated_at:%Y-%m-%d %H:%M:%S} "
            f"by platform manager #{report.platform_manager_id}"
        )
        cols = st.columns(3)
        cols[0].metric("Activities (started)", report.total_activity_count)
        cols[1].metric("Fundraisers", report.total_fundraiser_count)
        cols[2].metric("Donees", report.total_donee_count)
        cols2 = st.columns(2)
        cols2[0].metric("Donations ($)", f"{report.total_donation_amount:,.2f}")
        cols2[1].metric("Donations (count)", report.total_donation_count)
        if report.total_donation_count == 0:
            st.caption(
                "Donation figures are 0 because no donate use case exists yet "
                "(US-32 / US-33 deferred — see docs/issues.md)."
            )
