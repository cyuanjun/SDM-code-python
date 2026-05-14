"""Favourite <<Entity>> — Sprint 2 US-22, US-24.

Diagram contracts:
    US-22.jpg: + saveFundraisingActivity(accountId: String, FRAId: String): Boolean
    US-24.jpg: + viewFavourites(accountId: String): List<Favourite>
               (the diagram literally says `viewFavourite(...): Favourite`
               returning a single Favourite, but the user story is "view
               ALL my favourites". Sprint 2 typo logged in docs/todo.md.
               Implementation uses the list version.)

One row per (account_id, fra_id) pair. Composite primary key; duplicates
return False from save (caught via INSERT OR IGNORE rowcount).
"""
from __future__ import annotations

from dataclasses import dataclass

from persistence.db import get_connection
from persistence.ids import format_id, parse_id


@dataclass
class Favourite:
    account_id: str
    fra_id: str

    @classmethod
    def save_fundraising_activity(cls, account_id: str, fra_id: str) -> bool:
        account_rowid = parse_id(account_id)
        fra_rowid = parse_id(fra_id)
        # Pre-check for duplicates so the FK violations on account_id /
        # fra_id still raise IntegrityError while genuine duplicates
        # return False.
        with get_connection() as conn:
            existing = conn.execute(
                "SELECT 1 FROM favourite WHERE account_id = ? AND fra_id = ?",
                (account_rowid, fra_rowid),
            ).fetchone()
        if existing is not None:
            return False
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO favourite (account_id, fra_id) VALUES (?, ?)",
                (account_rowid, fra_rowid),
            )
        return cursor.rowcount > 0

    @classmethod
    def view_favourites(cls, account_id: str) -> list["Favourite"]:
        account_rowid = parse_id(account_id)
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT account_id, fra_id FROM favourite "
                "WHERE account_id = ? ORDER BY fra_id",
                (account_rowid,),
            ).fetchall()
        return [
            cls(
                account_id=format_id("acc", row["account_id"]),
                fra_id=format_id("fra", row["fra_id"]),
            )
            for row in rows
        ]
