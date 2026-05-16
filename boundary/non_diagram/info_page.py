"""InfoPage <<Boundary>> — debug-only utility.

NOT a real use case. Bypasses the B-C-E architecture and reads the
sqlite tables directly so the dev team can inspect database state
during development.

Shows row counts at the top, one tab per table for the raw contents,
and the live schema at the bottom. Hide or remove before any recorded
demo. Logged in docs/todo.md "Debug-only artifacts".
"""
from __future__ import annotations

import streamlit as st

from persistence.db import get_connection

# Order matters for the tabs — most-touched tables first.
TABLES = (
    "user_profile",
    "user_account",
    "fundraising_activity",
    "favourite",
    "donation",
    "fundraising_activity_category",
    "report",
)


class InfoPage:
    def render(self) -> None:
        st.header(".info (debug)")
        st.caption(
            "Direct SQLite read. Bypasses the B-C-E layers. Not a use case — "
            "remove or hide before the recorded demo."
        )

        counts = self._row_counts()
        self._render_count_metrics(counts)

        st.divider()
        st.subheader("Tables")
        tabs = st.tabs(list(TABLES))
        for tab, table in zip(tabs, TABLES):
            with tab:
                self._render_table(table, counts[table])

        st.divider()
        with st.expander("Schema (sqlite_master)"):
            self._render_schema()

    # ---- helpers ----------------------------------------------------------

    @staticmethod
    def _row_counts() -> dict[str, int]:
        counts: dict[str, int] = {}
        with get_connection() as conn:
            for table in TABLES:
                row = conn.execute(
                    f"SELECT COUNT(*) AS n FROM {table}"
                ).fetchone()
                counts[table] = int(row["n"])
        return counts

    @staticmethod
    def _render_count_metrics(counts: dict[str, int]) -> None:
        cols = st.columns(len(TABLES))
        for col, table in zip(cols, TABLES):
            col.metric(table, counts[table])

    @staticmethod
    def _render_table(table: str, count: int) -> None:
        if count == 0:
            st.info(f"{table} is empty.")
            return
        with get_connection() as conn:
            cursor = conn.execute(f"SELECT * FROM {table}")
            column_names = [c[0] for c in cursor.description]
            rows = [
                {col: row[col] for col in column_names}
                for row in cursor.fetchall()
            ]
        st.caption(f"{count} row(s)")
        st.dataframe(rows, width="stretch", hide_index=True)

    @staticmethod
    def _render_schema() -> None:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT name, sql FROM sqlite_master "
                "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
                "ORDER BY name"
            ).fetchall()
        for row in rows:
            st.markdown(f"**{row['name']}**")
            st.code(row["sql"], language="sql")
