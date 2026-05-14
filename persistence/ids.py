"""Shared ID format helpers.

Every primary key on the SQLite side is INTEGER PRIMARY KEY AUTOINCREMENT,
but Sprint 1 diagrams type every ID as String. Bridge: format on read,
parse on write.

    format_id("prof", 7)  -> "prof_007"
    parse_id("prof_007")  -> 7
"""
from __future__ import annotations


def format_id(prefix: str, rowid: int) -> str:
    return f"{prefix}_{rowid:03d}"


def parse_id(id_str: str) -> int:
    return int(id_str.split("_")[-1])
