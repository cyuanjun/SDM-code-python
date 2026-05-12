"""GenerateDailyReportPage <<Boundary>> — Sprint 4 diagram US-41."""
from __future__ import annotations

from datetime import date

import streamlit as st

from controller.generate_daily_report_controller import GenerateDailyReportController


class GenerateDailyReportPage:
    def render(self) -> None:
        st.header("Generate daily report")
        if "user" not in st.session_state:
            st.warning("Log in to generate a report.")
            return
        today = date.today()
        report_date = st.date_input("Report date", value=today)

        if st.button("Generate daily report", type="primary"):
            self.click_generate_daily_report_button(
                report_date.isoformat(),
                report_date.isoformat(),
                st.session_state["user"].account_id,
            )

    def click_generate_daily_report_button(
        self, start_date: str, end_date: str, platform_manager_id: int
    ) -> None:
        report = GenerateDailyReportController().generate_daily_report(
            start_date, end_date, platform_manager_id
        )
        self.display_report(report)

    @staticmethod
    def display_report(report) -> None:
        st.subheader(f"Daily report — {report.start_date}")
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
