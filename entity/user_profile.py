"""UserProfile <<Entity>> — Sprint 1 (US-1) + Sprint 2 (US-2 view, US-3 update)
+ Sprint 3 (US-4 delete, US-5 search)."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection


@dataclass
class UserProfile:
    role: str
    description: str
    profile_id: Optional[int] = None
    suspended: bool = False

    @classmethod
    def create_profile(cls, role: str, description: str) -> Optional["UserProfile"]:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO user_profile (role, description) VALUES (?, ?)",
                (role, description),
            )
            profile_id = cursor.lastrowid
        return cls(role=role, description=description, profile_id=profile_id)

    @classmethod
    def view_all_profiles(cls) -> list["UserProfile"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT profile_id, role, description, suspended "
                "FROM user_profile WHERE suspended = 0 ORDER BY profile_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def view_user_profile(cls, profile_id: str) -> Optional["UserProfile"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT profile_id, role, description, suspended "
                "FROM user_profile WHERE profile_id = ?",
                (profile_id,),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

    @classmethod
    def update_user_profile(
        cls, profile_id: str, updated_profile: "UserProfile"
    ) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_profile SET role = ?, description = ?, suspended = ? "
                "WHERE profile_id = ?",
                (
                    updated_profile.role,
                    updated_profile.description,
                    int(updated_profile.suspended),
                    profile_id,
                ),
            )
        return cursor.rowcount > 0

    @classmethod
    def delete_user_profile(cls, profile_id: str) -> bool:
        """US-4. Returns False on FK violation (profile referenced by an
        account) — see docs/todo.md Sprint 3 entry."""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "DELETE FROM user_profile WHERE profile_id = ?", (profile_id,)
                )
        except sqlite3.IntegrityError:
            return False
        return cursor.rowcount > 0

    @classmethod
    def submit_search_criteria(cls, search_criteria: str) -> list["UserProfile"]:
        """US-5. Case-insensitive substring match on role or description."""
        like = f"%{search_criteria}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT profile_id, role, description, suspended "
                "FROM user_profile WHERE role LIKE ? OR description LIKE ? "
                "ORDER BY profile_id",
                (like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row) -> "UserProfile":
        return cls(
            role=row["role"],
            description=row["description"],
            profile_id=row["profile_id"],
            suspended=bool(row["suspended"]),
        )
