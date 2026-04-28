"""FavouriteList <<Entity>> — Sprint 2 (US-22 save, US-24 view).

A row pairs an account with an activity it has favourited. Composite PK.
The class diagram for US-22 mistakenly labels the entity 'FundraisingActivity';
the sequence diagram and field list (accountId + activityId) make clear it is
FavouriteList.
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
    def remove_favourite(cls, account_id, activity_id) -> bool:
        """Helper for the View Favourites page so a Donee can unfavourite.
        Not in diagram — covers US-23 functionality which the team will
        formalize in a later sprint."""
        with get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM favourite_list WHERE account_id = ? AND activity_id = ?",
                (account_id, activity_id),
            )
        return cursor.rowcount > 0
