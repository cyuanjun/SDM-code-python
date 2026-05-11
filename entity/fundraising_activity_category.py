"""FundraisingActivityCategory <<Entity>> — Sprint 4 (US-34..US-38).

Naming deviation from the diagrams: the Sprint 4 class diagrams use
`createCategory` / `ViewFRACategory` / `updateFRACategory` /
`suspendFRACategory` and the typo `submitSeachCriteria`. To stay consistent
with the rest of the codebase (`suspend_fundraising_activity`,
`submit_search_criteria` on `FundraisingActivity` and `UserProfile`), the
implementation uses the full-word forms documented under
docs/todo.md "Sprint 4 naming deviations".
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection


@dataclass
class FundraisingActivityCategory:
    category_name: str
    description: str
    status: str = "active"
    category_id: Optional[int] = None

    @classmethod
    def create_category(cls, category_name: str, description: str) -> bool:
        """US-34. Returns False on uniqueness conflict (category_name UNIQUE)."""
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO fundraising_activity_category "
                    "(category_name, description) VALUES (?, ?)",
                    (category_name, description),
                )
        except sqlite3.IntegrityError:
            return False
        return True

    @classmethod
    def view_fundraising_activity_category(
        cls, category_id: int
    ) -> Optional["FundraisingActivityCategory"]:
        """US-35. Lookup by category_id. Returns None when not found."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT category_id, category_name, description, status "
                "FROM fundraising_activity_category WHERE category_id = ?",
                (category_id,),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

    @classmethod
    def view_all_categories(cls) -> list["FundraisingActivityCategory"]:
        """Helper for the Create-FRA page dropdown (Exception A in CLAUDE.md).
        Not on any Sprint 4 diagram — logged in docs/todo.md."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT category_id, category_name, description, status "
                "FROM fundraising_activity_category ORDER BY category_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def update_fundraising_activity_category(
        cls,
        category_id: int,
        updated_category: "FundraisingActivityCategory",
    ) -> bool:
        """US-36. Returns False when no row matches the id."""
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE fundraising_activity_category "
                    "SET category_name = ?, description = ?, status = ? "
                    "WHERE category_id = ?",
                    (
                        updated_category.category_name,
                        updated_category.description,
                        updated_category.status,
                        category_id,
                    ),
                )
        except sqlite3.IntegrityError:
            return False
        return cursor.rowcount > 0

    @classmethod
    def submit_search_criteria(
        cls, search_criteria: str
    ) -> list["FundraisingActivityCategory"]:
        """US-37. Case-insensitive substring match on name or description."""
        like = f"%{search_criteria}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT category_id, category_name, description, status "
                "FROM fundraising_activity_category "
                "WHERE category_name LIKE ? OR description LIKE ? "
                "ORDER BY category_id",
                (like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def suspend_fundraising_activity_category(cls, category_id: int) -> bool:
        """US-38. Returns False when no row matches the id."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity_category SET status = 'suspended' "
                "WHERE category_id = ?",
                (category_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def _from_row(cls, row) -> "FundraisingActivityCategory":
        return cls(
            category_id=row["category_id"],
            category_name=row["category_name"],
            description=row["description"],
            status=row["status"],
        )
