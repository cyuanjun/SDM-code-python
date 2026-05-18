"""SQLite connection helper."""
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
    schema = SCHEMA_PATH.read_text()
    with get_connection() as conn:
        conn.executescript(schema)
    _reconcile_columns(schema)


def _reconcile_columns(schema: str) -> None:
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
                continue
            for column_name, definition in columns.items():
                if column_name in existing:
                    continue
                conn.execute(
                    f"ALTER TABLE {table} ADD COLUMN {column_name} {definition}"
                )


_CREATE_TABLE_RE = re.compile(
    r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+(\w+)\s*\((.*?)\);",
    re.IGNORECASE | re.DOTALL,
)
_SQL_COMMENT_RE = re.compile(r"--[^\n]*")
_COLUMN_RE = re.compile(r"^\s*(\w+)\s+(.+?)\s*$")


def _parse_schema_columns(schema: str) -> dict[str, dict[str, str]]:
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
