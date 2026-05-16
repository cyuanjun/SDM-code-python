"""FundraisingActivityCategory <<Entity>> — Sprint 4 US-34..US-38.

Diagram contracts:
    US-34: + createCategory(categoryName: String, description: String): FundraisingActivityCategory
    US-35: + viewFundraisingActivityCategory(FRACatId: String): FundraisingActivityCategory
    US-36: + updateFundraisingActivityCategory(FRACatId: String,
              updatedFRACategory: FundraisingActivityCategory): Boolean
    US-37: + searchFundraisingActivityCategory(searchCriteria: String):
              List<FundraisingActivityCategory>
    US-38: + suspendFundraisingActivityCategory(FRACatId: String): Boolean

Attributes: FRACatId, categoryName, description, suspended (Boolean).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection
from persistence.ids import next_id


@dataclass
class FundraisingActivityCategory:
    category_name: str
    description: str
    suspended: bool = False
    fra_cat_id: Optional[str] = None

    @classmethod
    def create_category(
        cls, category_name: str, description: str
    ) -> "FundraisingActivityCategory":
        with get_connection() as conn:
            new_id = next_id(conn, "fundraising_activity_category", "fra_cat_id", "cat")
            conn.execute(
                "INSERT INTO fundraising_activity_category "
                "(fra_cat_id, category_name, description, suspended) "
                "VALUES (?, ?, ?, 0)",
                (new_id, category_name, description),
            )
        return cls(
            fra_cat_id=new_id,
            category_name=category_name,
            description=description,
            suspended=False,
        )

    @classmethod
    def view_fundraising_activity_category(
        cls, fra_cat_id: str
    ) -> Optional["FundraisingActivityCategory"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT fra_cat_id, category_name, description, suspended "
                "FROM fundraising_activity_category WHERE fra_cat_id = ?",
                (fra_cat_id,),
            ).fetchone()
        return None if row is None else cls._from_row(row)

    @classmethod
    def update_fundraising_activity_category(
        cls,
        fra_cat_id: str,
        updated_category: "FundraisingActivityCategory",
    ) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity_category "
                "SET category_name = ?, description = ?, suspended = ? "
                "WHERE fra_cat_id = ?",
                (
                    updated_category.category_name,
                    updated_category.description,
                    1 if updated_category.suspended else 0,
                    fra_cat_id,
                ),
            )
        return cursor.rowcount > 0

    @classmethod
    def search_fundraising_activity_category(
        cls, search_criteria: str
    ) -> list["FundraisingActivityCategory"]:
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT fra_cat_id, category_name, description, suspended "
                "FROM fundraising_activity_category "
                "WHERE LOWER(category_name) LIKE ? "
                "   OR LOWER(COALESCE(description, '')) LIKE ? "
                "ORDER BY fra_cat_id",
                (like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def suspend_fundraising_activity_category(cls, fra_cat_id: str) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity_category "
                "SET suspended = 1 WHERE fra_cat_id = ?",
                (fra_cat_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def unsuspend_fundraising_activity_category(cls, fra_cat_id: str) -> bool:
        """Exception A — mirror of suspend so the UI can toggle.
        Logged in docs/diagram_typos.md."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity_category "
                "SET suspended = 0 WHERE fra_cat_id = ?",
                (fra_cat_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def view_all_categories(cls) -> list["FundraisingActivityCategory"]:
        """Exception A: list-all for the boundary picker on US-35 / US-36 /
        US-38. Logged in docs/todo.md."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT fra_cat_id, category_name, description, suspended "
                "FROM fundraising_activity_category ORDER BY fra_cat_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row) -> "FundraisingActivityCategory":
        return cls(
            fra_cat_id=row["fra_cat_id"],
            category_name=row["category_name"],
            description=row["description"] or "",
            suspended=bool(row["suspended"]),
        )
