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
from persistence.ids import next_id


@dataclass
class UserProfile:
    role: str
    description: str
    suspended: bool = False
    profile_id: Optional[str] = None

    @classmethod
    def create_profile(cls, role: str, description: str) -> "UserProfile":
        with get_connection() as conn:
            new_id = next_id(conn, "user_profile", "profile_id", "prof")
            conn.execute(
                "INSERT INTO user_profile (profile_id, role, description, suspended) "
                "VALUES (?, ?, ?, 0)",
                (new_id, role, description),
            )
        return cls(
            profile_id=new_id,
            role=role,
            description=description,
            suspended=False,
        )

    @classmethod
    def view_user_profile(cls, profile_id: str) -> Optional["UserProfile"]:
        """US-2 — admin views a single profile by id. Returns None for a
        missing row (negative branch implicit in the diagram)."""
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
        """US-3 — admin updates a profile. Returns True on success, False
        when no row matches profile_id."""
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
        return cursor.rowcount > 0

    @classmethod
    def suspend_user_profile(cls, profile_id: str) -> bool:
        """US-4 — admin suspends a profile. Returns True on rowcount > 0,
        False when no row matches."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_profile SET suspended = 1 WHERE profile_id = ?",
                (profile_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def unsuspend_user_profile(cls, profile_id: str) -> bool:
        """Exception A — mirror of suspend so the UI can toggle.
        Logged in docs/diagram_typos.md."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_profile SET suspended = 0 WHERE profile_id = ?",
                (profile_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def search_user_profile(cls, search_criteria: str) -> list["UserProfile"]:
        """US-5 — admin searches profiles by criteria. Case-insensitive
        substring match against role and description."""
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
                profile_id=row["profile_id"],
                role=row["role"],
                description=row["description"] or "",
                suspended=bool(row["suspended"]),
            )
            for row in rows
        ]
