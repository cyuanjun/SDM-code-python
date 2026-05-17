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


@dataclass
class Favourite:
    account_id: str
    fra_id: str

    @classmethod
    def save_fundraising_activity(cls, account_id: str, fra_id: str) -> bool:
        from entity.fundraising_activity import FundraisingActivity

        # Pre-check for duplicates so the FK violations on account_id /
        # fra_id still raise IntegrityError while genuine duplicates
        # return False.
        with get_connection() as conn:
            existing = conn.execute(
                "SELECT 1 FROM favourite WHERE account_id = ? AND fra_id = ?",
                (account_id, fra_id),
            ).fetchone()
        if existing is not None:
            return False
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO favourite (account_id, fra_id) VALUES (?, ?)",
                (account_id, fra_id),
            )
        if cursor.rowcount > 0:
            # Exception A: bump save_count so US-29 has something to show.
            FundraisingActivity.increment_save_count(fra_id, +1)
            return True
        return False

    @classmethod
    def remove_favourite(cls, fra_id: str, account_id: str) -> bool:
        """US-23 — donee removes one favourite. Returns True on rowcount > 0
        (the pair existed), False otherwise. Scoped to the caller's
        account_id, so a different donee can't remove someone else's row.

        Parameter order matches the US-23 diagram (FRAId then accountId).
        """
        from entity.fundraising_activity import FundraisingActivity

        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM favourite "
                "WHERE fra_id = ? AND account_id = ?",
                (fra_id, account_id),
            )
        if cursor.rowcount > 0:
            # Exception A: bump save_count down.
            FundraisingActivity.increment_save_count(fra_id, -1)
            return True
        return False

    @classmethod
    def search_favourite(
        cls, account_id: str, search_criteria: str
    ) -> list["Favourite"]:
        """US-25 — donee searches their favourites. Joins to
        fundraising_activity and matches title / description / category
        against the criteria, scoped to the caller's account_id. Favourites
        pointing at suspended activities are hidden — once the owner
        suspends, the activity stops being donee-visible everywhere.
        """
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT f.account_id, f.fra_id "
                "FROM favourite f "
                "JOIN fundraising_activity a ON a.fra_id = f.fra_id "
                "JOIN fundraising_activity_category c ON c.fra_cat_id = a.fra_cat_id "
                "WHERE f.account_id = ? AND a.suspended = 0 AND ("
                "  LOWER(a.title) LIKE ? OR LOWER(a.description) LIKE ? "
                "  OR LOWER(c.category_name) LIKE ?"
                ") ORDER BY f.fra_id",
                (account_id, like, like, like),
            ).fetchall()
        return [
            cls(
                account_id=row["account_id"],
                fra_id=row["fra_id"],
            )
            for row in rows
        ]

    @classmethod
    def view_favourite_list(cls, account_id: str) -> list["Favourite"]:
        """US-24 — donee views their favourites. Favourites pointing at
        suspended activities are hidden via JOIN; the row stays in the
        favourite table so it reappears if the owner unsuspends."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT f.account_id, f.fra_id "
                "FROM favourite f "
                "JOIN fundraising_activity a ON a.fra_id = f.fra_id "
                "WHERE f.account_id = ? AND a.suspended = 0 "
                "ORDER BY f.fra_id",
                (account_id,),
            ).fetchall()
        return [
            cls(
                account_id=row["account_id"],
                fra_id=row["fra_id"],
            )
            for row in rows
        ]
