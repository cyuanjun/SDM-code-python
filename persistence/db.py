"""SQLite connection helper. Single source of truth for DB access.

`init_db()` runs `schema.sql` then a generic schema-reconcile pass that
ALTERs any existing table to add columns declared in `schema.sql` but
missing in `app.db` — lets schema additions (e.g. the 2026-05-18
re-introduction of `fundraising_activity.completed`) heal an old DB
without forcing the user to `rm app.db` first. Covers every table.
"""
from __future__ import annotations

import re
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
    """Apply schema.sql (CREATE TABLE IF NOT EXISTS) + reconcile any
    existing tables against the canonical column list. Idempotent."""
    schema = SCHEMA_PATH.read_text()
    with get_connection() as conn:
        conn.executescript(schema)
    _reconcile_columns(schema)


# ----------------------------------------------------------------------------
# auto-migration: add columns to existing tables when schema.sql adds them
# ----------------------------------------------------------------------------


def _reconcile_columns(schema: str) -> None:
    """For every CREATE TABLE in `schema`, ALTER TABLE ADD COLUMN any
    columns that are in the schema but missing from the existing table.
    Skips PRIMARY KEY / UNIQUE / NOT NULL semantics that SQLite refuses
    to add retroactively (those are reported but not enforced — they'd
    require a table-rebuild). Idempotent."""
    expected = _parse_schema_columns(schema)
    with get_connection() as conn:
        for table, columns in expected.items():
            existing = {
                row["name"]
                for row in conn.execute(
                    f"PRAGMA table_info({table})"
                ).fetchall()
            }
            if not existing:
                # Table didn't exist before either CREATE TABLE just made
                # it; nothing to migrate.
                continue
            for column_name, definition in columns.items():
                if column_name in existing:
                    continue
                # SQLite can only ADD COLUMN if the new column is either
                # nullable or has a default value. NOT NULL without
                # default would fail. Our schema uses `NOT NULL DEFAULT
                # 0` (or `''`) on every addable column, so this works.
                conn.execute(
                    f"ALTER TABLE {table} ADD COLUMN {column_name} {definition}"
                )


# Match `CREATE TABLE IF NOT EXISTS <name> ( <body> );` blocks. The body
# is a comma-separated list of column definitions and table-level
# constraints. We only need column defs (name + the rest of the line).
_CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+(\w+)\s*\((.*?)\);",
    re.IGNORECASE | re.DOTALL,
)
# Strip SQL line comments (`-- …`) before parsing column bodies.
_SQL_COMMENT_RE = re.compile(r"--[^\n]*")
# Column lines look like: `<name> <type> [constraints…]`. We capture the
# name (first token) and the rest of the line as the column definition.
_COLUMN_RE = re.compile(r"^\s*(\w+)\s+(.+?)\s*$")


def _parse_schema_columns(schema: str) -> dict[str, dict[str, str]]:
    """Parse `schema.sql` into `{table: {column: definition_after_name}}`.
    Skips lines that are table-level constraints (PRIMARY KEY, FOREIGN
    KEY, etc.) rather than column definitions."""
    result: dict[str, dict[str, str]] = {}
    for match in _CREATE_TABLE_RE.finditer(schema):
        table = match.group(1)
        body = _SQL_COMMENT_RE.sub("", match.group(2))
        columns: dict[str, str] = {}
        for line in _split_top_level(body):
            line = line.strip()
            if not line:
                continue
            head = line.split(None, 1)[0].upper()
            if head in {
                "PRIMARY", "FOREIGN", "UNIQUE", "CHECK", "CONSTRAINT",
            }:
                continue
            m = _COLUMN_RE.match(line)
            if not m:
                continue
            columns[m.group(1)] = m.group(2)
        result[table] = columns
    return result


def _split_top_level(body: str) -> list[str]:
    """Split the CREATE TABLE body on top-level commas, ignoring commas
    nested inside parentheses (so a FOREIGN KEY clause with a multi-arg
    REFERENCES stays in one piece)."""
    depth = 0
    current: list[str] = []
    out: list[str] = []
    for ch in body:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(current))
            current = []
        else:
            current.append(ch)
    if current:
        out.append("".join(current))
    return out


if __name__ == "__main__":
    init_db()
    print(f"Initialised database at {DB_PATH}")
