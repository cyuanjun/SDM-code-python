"""GenerateMonthlyReportPage <<Boundary>> — Sprint 4 diagram US-43."""
from __future__ import annotations

from calendar import monthrange
from datetime import date

import streamlit as st

from controller.generate_monthly_report_controller import (
    GenerateMonthlyReportController,
)


class GenerateMonthlyReportPage:
    def render(self) -> None:
        st.header("Generate monthly report")
        today = date.today()
        cols = st.columns(2)
        year = cols[0].number_input(
            "Year", min_value=2020, max_value=2099, value=today.year, step=1
        )
        month = cols[1].number_input(
            "Month", min_value=1, max_value=12, value=today.month, step=1
        )

        first = date(int(year), int(month), 1)
        last = date(int(year), int(month), monthrange(int(year), int(month))[1])

        if st.button("Generate monthly report", type="primary"):
            self.click_generate_monthly_report_button(
                first.isoformat(), last.isoformat()
            )

    def click_generate_monthly_report_button(
        self, start_date: str, end_date: str
    ) -> None:
        report = GenerateMonthlyReportController().generate_monthly_report(
            start_date, end_date
        )
        self.display_report(report)

    @staticmethod
    def display_report(report) -> None:
        st.subheader(f"Monthly report — {report.start_date} to {report.end_date}")
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
