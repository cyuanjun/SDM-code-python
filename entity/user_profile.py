"""UserProfile <<Entity>>."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection
from persistence.ids import next_id


@dataclass
class UserProfile:
    role: str
    description: str
    suspended: bool = False
    profile_id: Optional[str] = None

    @classmethod
    def create_profile(
        cls, role: str, description: str
    ) -> Optional["UserProfile"]:
        try:
            with get_connection() as conn:
                new_id = next_id(conn, "user_profile", "profile_id", "prof")
                conn.execute(
                    "INSERT INTO user_profile (profile_id, role, description, suspended) "
                    "VALUES (?, ?, ?, 0)",
                    (new_id, role, description),
                )
        except sqlite3.IntegrityError:
            return None
        return cls(
            profile_id=new_id,
            role=role,
            description=description,
            suspended=False,
        )

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
        return cls(
            profile_id=row["profile_id"],
            role=row["role"],
            description=row["description"] or "",
            suspended=bool(row["suspended"]),
        )

    @classmethod
    def update_user_profile(
        cls, profile_id: str, updated_profile: "UserProfile"
    ) -> bool:
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE user_profile SET role = ?, description = ?, suspended = ? "
                    "WHERE profile_id = ?",
                    (
                        updated_profile.role,
                        updated_profile.description,
                        1 if updated_profile.suspended else 0,
                        profile_id,
                    ),
                )
        except sqlite3.IntegrityError:
            return False
        return cursor.rowcount > 0

    @classmethod
    def suspend_user_profile(cls, profile_id: str) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_profile SET suspended = 1 WHERE profile_id = ?",
                (profile_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def unsuspend_user_profile(cls, profile_id: str) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_profile SET suspended = 0 WHERE profile_id = ?",
                (profile_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def search_user_profile(cls, search_criteria: str) -> list["UserProfile"]:
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT profile_id, role, description, suspended "
                "FROM user_profile "
                "WHERE LOWER(role) LIKE ? OR LOWER(COALESCE(description, '')) LIKE ? "
                "ORDER BY profile_id",
                (like, like),
            ).fetchall()
        return [
            cls(
                profile_id=row["profile_id"],
                role=row["role"],
                description=row["description"] or "",
                suspended=bool(row["suspended"]),
            )
            for row in rows
        ]

    @classmethod
    def view_all_profiles(cls) -> list["UserProfile"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT profile_id, role, description, suspended "
                "FROM user_profile ORDER BY profile_id"
            ).fetchall()
        return [
            cls(
                profile_id=row["profile_id"],
                role=row["role"],
                description=row["description"] or "",
                suspended=bool(row["suspended"]),
            )
            for row in rows
        ]
