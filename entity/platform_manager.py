"""PlatformManager <<Entity>> — Sprint 4 (US-41..US-43 reports).

Sprint 4 introduces the Platform Manager actor for category management
(US-34..US-38) and report generation (US-41..US-43). No login flow is
required by the supplied diagrams — the table exists to satisfy the
Report.platformManagerId field and to seed at least one PM for the
on-the-fly report generation flow. See docs/issues.md "Platform Manager
actor has no login flow" for the scoping decision.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection


@dataclass
class PlatformManager:
    username: str
    password: str
    email: str
    name: str
    platform_manager_id: Optional[int] = None

    @classmethod
    def create_platform_manager(
        cls, username: str, password: str, email: str, name: str
    ) -> Optional["PlatformManager"]:
        """Returns None on uniqueness conflict (username or email)."""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO platform_manager (username, password, email, name) "
                    "VALUES (?, ?, ?, ?)",
                    (username, password, email, name),
                )
                platform_manager_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        return cls(
            username=username,
            password=password,
            email=email,
            name=name,
            platform_manager_id=platform_manager_id,
        )

    @classmethod
    def view_all_platform_managers(cls) -> list["PlatformManager"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT platform_manager_id, username, password, email, name "
                "FROM platform_manager ORDER BY platform_manager_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row) -> "PlatformManager":
        return cls(
            platform_manager_id=row["platform_manager_id"],
            username=row["username"],
            password=row["password"],
            email=row["email"],
            name=row["name"],
        )
