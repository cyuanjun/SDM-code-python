"""Favourite <<Entity>>."""
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
            FundraisingActivity.increment_save_count(fra_id, +1)
            return True
        return False

    @classmethod
    def remove_favourite(cls, fra_id: str, account_id: str) -> bool:
        from entity.fundraising_activity import FundraisingActivity

        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM favourite "
                "WHERE fra_id = ? AND account_id = ?",
                (fra_id, account_id),
            )
        if cursor.rowcount > 0:
            FundraisingActivity.increment_save_count(fra_id, -1)
            return True
        return False

    @classmethod
    def search_favourite(
        cls, account_id: str, search_criteria: str
    ) -> list["Favourite"]:
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
