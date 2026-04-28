"""InfoPage — DEVELOPMENT/DEBUG UTILITY ONLY.

This page is NOT part of the B-C-E design and is NOT in any sequence diagram.
It exists purely so the team can inspect (and now mutate) the SQLite contents
during development.

Because it's a debug tool, it deliberately bypasses the Controller/Entity layers
and reads/writes the database directly. Do NOT model future features after this file.

Remove or hide this page before the final live demo.
"""
from __future__ import annotations

import sqlite3

import streamlit as st

from persistence.db import DB_PATH, get_connection

TABLES = ("user_profile", "user_account", "fundraising_activity")
PK_COLS = {
    "user_profile": "profile_id",
    "user_account": "email",
    "fundraising_activity": "activity_id",
}


class InfoPage:
    def render(self) -> None:
        st.header("Database inspector")
        st.warning(
            "Development utility — not part of the B-C-E design. "
            "Hide this page before the final demo."
        )
        st.caption(f"DB file: `{DB_PATH}`")

        if "info_flash" in st.session_state:
            kind, msg = st.session_state.pop("info_flash")
            getattr(st, kind)(msg)

        counts = self._counts()
        cols = st.columns(len(TABLES))
        for col, table in zip(cols, TABLES):
            col.metric(table, counts.get(table, 0))

        tabs = st.tabs([t.replace("_", " ").title() for t in TABLES])
        for tab, table in zip(tabs, TABLES):
            with tab:
                self._render_table_tab(table)

        with st.expander("Schema"):
            st.code(self._schema(), language="sql")

    def _render_table_tab(self, table: str) -> None:
        rows = self._select_all(table)
        if not rows:
            st.info(f"No rows in `{table}` yet. Run `python -m data.seed`.")
            return

        event = st.dataframe(
            rows,
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key=f"df_{table}",
        )
        selected = event.selection.rows
        if not selected:
            st.caption("Click a row to enable delete.")
            return

        pk_col = PK_COLS[table]
        pk_value = rows[selected[0]][pk_col]
        left, right = st.columns([3, 1])
        with left:
            st.write(f"Selected **{pk_col}** = `{pk_value}`")
        with right:
            if st.button(
                "Delete row",
                key=f"del_{table}",
                type="primary",
                width="stretch",
            ):
                self._delete(table, pk_col, pk_value)

    def _delete(self, table: str, pk_col: str, pk_value) -> None:
        try:
            with get_connection() as conn:
                conn.execute(f"DELETE FROM {table} WHERE {pk_col} = ?", (pk_value,))
        except sqlite3.IntegrityError as e:
            st.session_state["info_flash"] = (
                "error",
                f"Cannot delete from `{table}` — referenced by another table. "
                f"Delete dependents first. ({e})",
            )
        else:
            st.session_state["info_flash"] = (
                "success",
                f"Deleted from `{table}` where {pk_col} = {pk_value}.",
            )
        st.rerun()

    @staticmethod
    def _counts() -> dict[str, int]:
        with get_connection() as conn:
            return {
                t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                for t in TABLES
            }

    @staticmethod
    def _select_all(table: str) -> list[dict]:
        with get_connection() as conn:
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _schema() -> str:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL"
            ).fetchall()
        return "\n\n".join(row["sql"] for row in rows)
