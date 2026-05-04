"""FavouriteList <<Entity>> — Sprint 2 (US-22 save, US-24 view) + Sprint 3
(US-23 delete, US-25 search).

A row pairs an account with an activity it has favourited. Composite PK.
The class diagram for US-22 mistakenly labels the entity 'FundraisingActivity';
the sequence diagram and field list (accountId + activityId) make clear it is
FavouriteList.

Sprint 3 update: submit_search_criteria takes an optional account_id to scope
the donee's search to their own favourites — the US-25 diagram only shows the
search criteria, but without account scoping the method would leak other
donees' favourites. Diagram update logged in docs/todo.md.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection


@dataclass
class FavouriteList:
    account_id: int
    activity_id: int

    @classmethod
    def save_fundraising_activity(cls, account_id, activity_id) -> bool:
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO favourite_list (account_id, activity_id) VALUES (?, ?)",
                    (account_id, activity_id),
                )
        except sqlite3.IntegrityError:
            # already favourited or FK violation — idempotent failure
            return False
        return True

    @classmethod
    def view_favourite_list(cls, account_id: str) -> list["FavouriteList"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT account_id, activity_id FROM favourite_list "
                "WHERE account_id = ? ORDER BY activity_id",
                (account_id,),
            ).fetchall()
        return [
            cls(account_id=row["account_id"], activity_id=row["activity_id"])
            for row in rows
        ]

    @classmethod
    def delete_favourite(cls, activity_id, account_id) -> bool:
        """US-23. Param order matches the diagram: (activityId, accountId)."""
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM favourite_list WHERE activity_id = ? AND account_id = ?",
                (activity_id, account_id),
            )
        return cursor.rowcount > 0

    @classmethod
    def submit_search_criteria(
        cls, search_criteria: str, account_id: Optional[int] = None
    ) -> list["FavouriteList"]:
        """US-25. Returns favourites whose linked activity matches the
        criteria (case-insensitive substring on title, description, or
        category). Scoped to one account when account_id is provided."""
        like = f"%{search_criteria}%"
        sql = (
            "SELECT f.account_id, f.activity_id "
            "FROM favourite_list f "
            "JOIN fundraising_activity a ON a.activity_id = f.activity_id "
            "WHERE (a.title LIKE ? OR a.description LIKE ? OR a.category LIKE ?)"
        )
        params: list = [like, like, like]
        if account_id is not None:
            sql += " AND f.account_id = ?"
            params.append(account_id)
        sql += " ORDER BY f.activity_id"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [
            cls(account_id=row["account_id"], activity_id=row["activity_id"])
            for row in rows
        ]
