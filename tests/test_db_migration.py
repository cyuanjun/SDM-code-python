"""Tests for the auto-migration pass in `persistence.db.init_db()`.

When `schema.sql` gains a column on a table that already exists in
`app.db`, plain `CREATE TABLE IF NOT EXISTS` won't add it — the table is
already there. The reconcile pass after the executescript catches this
by ALTER TABLE ADD COLUMN'ing the missing columns. These tests exercise
that path against a hand-built stale DB to keep the auto-heal honest
across every table the project defines.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from persistence import db as db_module
from persistence.db import init_db


def _columns(table: str) -> set[str]:
    with sqlite3.connect(db_module.DB_PATH) as conn:
        return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def _build_stale_db(missing_column: str, table: str = "fundraising_activity") -> None:
    """Create app.db with schema.sql, but immediately drop one column from
    a chosen table so it looks like a pre-migration database."""
    init_db()
    # Use the SQLite "rebuild without the column" recipe.
    with sqlite3.connect(db_module.DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = OFF")
        info = conn.execute(f"PRAGMA table_info({table})").fetchall()
        kept = [row for row in info if row[1] != missing_column]
        if len(kept) == len(info):
            raise RuntimeError(f"{missing_column!r} was not in {table}")
        # Re-create the table without `missing_column` using a temp name,
        # copy rows, then swap. Crude but enough for the test.
        col_defs = []
        for cid, name, type_, notnull, dflt, pk in kept:
            piece = f"{name} {type_}"
            if notnull:
                piece += " NOT NULL"
            if dflt is not None:
                piece += f" DEFAULT {dflt}"
            if pk:
                piece += " PRIMARY KEY"
            col_defs.append(piece)
        col_list = ", ".join(row[1] for row in kept)
        conn.executescript(
            f"DROP TABLE IF EXISTS _migration_tmp;\n"
            f"CREATE TABLE _migration_tmp ({', '.join(col_defs)});\n"
            f"INSERT INTO _migration_tmp SELECT {col_list} FROM {table};\n"
            f"DROP TABLE {table};\n"
            f"ALTER TABLE _migration_tmp RENAME TO {table};\n"
        )


def test_init_db_heals_missing_completed_on_fundraising_activity() -> None:
    """Happy path of the 2026-05-18 auto-migration: a pre-migration DB
    is missing `fundraising_activity.completed`; calling init_db a second
    time picks up the gap and ALTERs the column in."""
    _build_stale_db("completed")
    assert "completed" not in _columns("fundraising_activity")

    init_db()

    assert "completed" in _columns("fundraising_activity")


@pytest.mark.parametrize(
    "table,column",
    [
        ("favourite", "fra_id"),
        ("report", "report_type"),
    ],
)
def test_init_db_heals_missing_column_on_any_table(
    table: str, column: str,
) -> None:
    """The migration walks every CREATE TABLE in schema.sql — proves the
    reconcile is generic, not hard-coded to fundraising_activity."""
    _build_stale_db(column, table=table)
    assert column not in _columns(table)

    init_db()

    assert column in _columns(table)


def test_init_db_is_a_no_op_when_schema_matches_db() -> None:
    """Negative path: running init_db twice against a fresh DB makes no
    schema changes the second time (the reconcile pass finds nothing
    missing and emits zero ALTER statements)."""
    init_db()
    before = _columns("fundraising_activity")

    init_db()

    assert _columns("fundraising_activity") == before
