"""UserProfile <<Entity>> — Sprint 1 US-1.

Diagram contract (US-01.jpg):
    + createProfile(role: String, description: String): UserProfile

Attributes from the class diagram: profileId, role, description, suspended.
`suspended` is treated as Boolean (logged typo in docs/todo.md — the diagram
shows String).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection
from persistence.ids import format_id, parse_id


@dataclass
class UserProfile:
    role: str
    description: str
    suspended: bool = False
    profile_id: Optional[str] = None

    @classmethod
    def create_profile(cls, role: str, description: str) -> "UserProfile":
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO user_profile (role, description, suspended) "
                "VALUES (?, ?, 0)",
                (role, description),
            )
            rowid = cursor.lastrowid
        return cls(
            profile_id=format_id("prof", rowid),
            role=role,
            description=description,
            suspended=False,
        )

    @classmethod
    def view_user_profile(cls, profile_id: str) -> Optional["UserProfile"]:
        """US-2 — admin views a single profile by id. Returns None for a
        missing row (negative branch implicit in the diagram)."""
        rowid = parse_id(profile_id)
        with get_connection() as conn:
            row = conn.execute(
                "SELECT profile_id, role, description, suspended "
                "FROM user_profile WHERE profile_id = ?",
                (rowid,),
            ).fetchone()
        if row is None:
            return None
        return cls(
            profile_id=format_id("prof", row["profile_id"]),
            role=row["role"],
            description=row["description"] or "",
            suspended=bool(row["suspended"]),
        )

    @classmethod
    def view_all_profiles(cls) -> list["UserProfile"]:
        """Exception A (CLAUDE.md): not on the US-1 diagram but needed to
        power the profile dropdown on CreateAccountPage. Logged in
        docs/todo.md as a diagram update owed before final marking."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT profile_id, role, description, suspended "
                "FROM user_profile ORDER BY profile_id"
            ).fetchall()
        return [
            cls(
                profile_id=format_id("prof", row["profile_id"]),
                role=row["role"],
                description=row["description"] or "",
                suspended=bool(row["suspended"]),
            )
            for row in rows
        ]
