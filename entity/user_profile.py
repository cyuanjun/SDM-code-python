"""UserProfile <<Entity>> — see Sprint 1 class diagram (US-1)."""
from __future__ import annotations

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
        return [
            cls(
                role=row["role"],
                description=row["description"],
                profile_id=row["profile_id"],
                suspended=bool(row["suspended"]),
            )
            for row in rows
        ]
