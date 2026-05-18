"""Shared ID helpers."""
from __future__ import annotations

import sqlite3


def format_id(prefix: str, n: int) -> str:
    return f"{prefix}_{n:03d}"


def next_id(
    conn: sqlite3.Connection, table: str, id_column: str, prefix: str
) -> str:
    row = conn.execute(
        f"SELECT {id_column} FROM {table} ORDER BY {id_column} DESC LIMIT 1"
    ).fetchone()
    if row is None:
        return format_id(prefix, 1)
    last = row[id_column]
    n = int(last.split("_")[-1]) + 1
    return format_id(prefix, n)
