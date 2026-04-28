"""SQLite connection helper. Single source of truth for DB access."""
from __future__ import annotations

import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "app.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    schema = SCHEMA_PATH.read_text()
    with get_connection() as conn:
        conn.executescript(schema)


if __name__ == "__main__":
    init_db()
    print(f"Initialised database at {DB_PATH}")
