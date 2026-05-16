"""Shared ID helpers.

Every primary key is TEXT in the schema (e.g. "prof_001", "acc_042") so
the storage form matches the diagrams. Since TEXT primary keys don't
auto-increment, this module owns the "what's the next ID" logic.

    format_id("prof", 7)              -> "prof_007"
    next_id(conn, "user_profile",
            "profile_id", "prof")     -> "prof_004" (if max existing was prof_003)
"""
from __future__ import annotations

import sqlite3


def format_id(prefix: str, n: int) -> str:
    """Zero-pad to 3 digits so lexicographic ordering matches numeric
    ordering up to 999 rows per table."""
    return f"{prefix}_{n:03d}"


def next_id(
    conn: sqlite3.Connection, table: str, id_column: str, prefix: str
) -> str:
    """Compute the next available prefixed id for `table`.

    Reads the highest existing id, parses its numeric suffix, increments,
    and re-formats. Returns "{prefix}_001" when the table is empty.
    """
    row = conn.execute(
        f"SELECT {id_column} FROM {table} ORDER BY {id_column} DESC LIMIT 1"
    ).fetchone()
    if row is None:
        return format_id(prefix, 1)
    last = row[id_column]
    n = int(last.split("_")[-1]) + 1
    return format_id(prefix, n)
