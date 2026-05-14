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
from persistence.ids import format_id


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
