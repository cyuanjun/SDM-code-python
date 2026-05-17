"""FundraisingActivity <<Entity>> — Sprint 1 US-13, US-21.

Diagram contracts (2026-05-18 set):
    US-13.jpg: + createFundraisingActivity(
        title: String, description: String, targetAmount: Decimal,
        FRACatId: String, startDate: Date, endDate: Date,
        ownerAccountId: String,
      ): FundraisingActivity
    US-21.jpg: + viewFundraisingActivity(activityId: String): FundraisingActivity

Per the 2026-05-18 US-13 diagram the entity attribute `category: String`
was replaced with `FRACatId: String` — an FK to `FundraisingActivityCategory`
rather than a free-text string. Search methods (US-17, US-20, US-30) now
JOIN to `fundraising_activity_category` and match the criteria against
the category name (in addition to title + description).

`target_amount` is Decimal per the diagram (not Float). Stored as TEXT
to preserve precision; converted back to Decimal on read.

`view_count` and `save_count` are declared on the entity from Sprint 1
even though the read/increment methods are not introduced until later
sprints. They default to 0 here.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from persistence.db import get_connection
from persistence.ids import next_id


_SELECT_COLUMNS = (
    "fra_id, title, description, target_amount, fra_cat_id, "
    "start_date, end_date, completed, suspended, owner_account_id, "
    "view_count, save_count"
)


@dataclass
class FundraisingActivity:
    title: str
    description: str
    target_amount: Decimal
    fra_cat_id: str
    start_date: date
    end_date: date
    owner_account_id: str
    completed: bool = False
    suspended: bool = False
    view_count: int = 0
    save_count: int = 0
    fra_id: Optional[str] = None

    @classmethod
    def create_fundraising_activity(
        cls,
        title: str,
        description: str,
        target_amount: Decimal,
        fra_cat_id: str,
        start_date: date,
        end_date: date,
        owner_account_id: str,
    ) -> "FundraisingActivity":
        with get_connection() as conn:
            new_id = next_id(conn, "fundraising_activity", "fra_id", "fra")
            conn.execute(
                "INSERT INTO fundraising_activity "
                "(fra_id, title, description, target_amount, fra_cat_id, start_date, "
                " end_date, completed, suspended, owner_account_id, view_count, save_count) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, ?, 0, 0)",
                (
                    new_id,
                    title,
                    description,
                    str(target_amount),
                    fra_cat_id,
                    start_date.isoformat(),
                    end_date.isoformat(),
                    owner_account_id,
                ),
            )
        return cls(
            fra_id=new_id,
            title=title,
            description=description,
            target_amount=target_amount,
            fra_cat_id=fra_cat_id,
            start_date=start_date,
            end_date=end_date,
            owner_account_id=owner_account_id,
            completed=False,
            suspended=False,
            view_count=0,
            save_count=0,
        )

    @classmethod
    def view_my_fundraising_activity(
        cls, owner_account_id: str, fra_id: str
    ) -> Optional["FundraisingActivity"]:
        """US-14 — fundraiser views one of their own activities.
        Ownership scoped at the entity layer per the diagram signature."""
        with get_connection() as conn:
            row = conn.execute(
                f"SELECT {_SELECT_COLUMNS} FROM fundraising_activity "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (fra_id, owner_account_id),
            ).fetchone()
        return None if row is None else cls._from_row(row)

    @classmethod
    def view_my_fundraising_activities(
        cls, owner_account_id: str
    ) -> list["FundraisingActivity"]:
        """Exception A: list-by-owner scoping for US-14 / US-15. Without
        this the fundraiser would have to know their own activity ids
        verbatim before triggering viewMyFundraisingActivity. Logged in
        docs/todo.md."""
        with get_connection() as conn:
            rows = conn.execute(
                f"SELECT {_SELECT_COLUMNS} FROM fundraising_activity "
                "WHERE owner_account_id = ? ORDER BY fra_id",
                (owner_account_id,),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def suspend_my_fundraising_activity(
        cls, owner_account_id: str, fra_id: str
    ) -> bool:
        """US-16 — fundraiser suspends one of their own activities.
        Ownership scoped: UPDATE … WHERE fra_id AND owner_account_id."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity SET suspended = 1 "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (fra_id, owner_account_id),
            )
        return cursor.rowcount > 0

    @classmethod
    def unsuspend_my_fundraising_activity(
        cls, owner_account_id: str, fra_id: str
    ) -> bool:
        """Exception A — mirror of suspend so the UI can toggle.
        Logged in docs/diagram_typos.md."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity SET suspended = 0 "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (fra_id, owner_account_id),
            )
        return cursor.rowcount > 0

    @classmethod
    def search_my_fundraising_activity(
        cls, owner_account_id: str, search_criteria: str
    ) -> list["FundraisingActivity"]:
        """US-17 — fundraiser searches their own activities. Case-insensitive
        substring match against title / description / category_name
        (JOIN'd from FundraisingActivityCategory), scoped to owner_account_id."""
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                f"SELECT {_alias_columns('a')} FROM fundraising_activity a "
                "JOIN fundraising_activity_category c ON c.fra_cat_id = a.fra_cat_id "
                "WHERE a.owner_account_id = ? AND ("
                "  LOWER(a.title) LIKE ? OR LOWER(a.description) LIKE ? "
                "  OR LOWER(c.category_name) LIKE ?"
                ") ORDER BY a.fra_id",
                (owner_account_id, like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def search_my_completed_fundraising_activity(
        cls, owner_account_id: str, search_criteria: str
    ) -> list["FundraisingActivity"]:
        """US-30 — fundraiser searches their completed activities. Scoped
        to owner + completed = 1; matches title / description / category_name."""
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                f"SELECT {_alias_columns('a')} FROM fundraising_activity a "
                "JOIN fundraising_activity_category c ON c.fra_cat_id = a.fra_cat_id "
                "WHERE a.owner_account_id = ? AND a.completed = 1 AND ("
                "  LOWER(a.title) LIKE ? OR LOWER(a.description) LIKE ? "
                "  OR LOWER(c.category_name) LIKE ?"
                ") ORDER BY a.fra_id",
                (owner_account_id, like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def view_my_completed_fundraising_activities(
        cls, owner_account_id: str
    ) -> list["FundraisingActivity"]:
        """US-31 — fundraiser views the list of their completed activities."""
        with get_connection() as conn:
            rows = conn.execute(
                f"SELECT {_SELECT_COLUMNS} FROM fundraising_activity "
                "WHERE owner_account_id = ? AND completed = 1 "
                "ORDER BY fra_id",
                (owner_account_id,),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def search_fundraising_activity(
        cls, search_criteria: str
    ) -> list["FundraisingActivity"]:
        """US-20 — donee searches activities by criteria. Case-insensitive
        substring match against title / description / category_name.
        Suspended activities are hidden from donees: they only show up in
        owner-scoped searches."""
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                f"SELECT {_alias_columns('a')} FROM fundraising_activity a "
                "JOIN fundraising_activity_category c ON c.fra_cat_id = a.fra_cat_id "
                "WHERE a.suspended = 0 AND ("
                "  LOWER(a.title) LIKE ? "
                "   OR LOWER(a.description) LIKE ? "
                "   OR LOWER(c.category_name) LIKE ? "
                ") ORDER BY a.fra_id",
                (like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def update_my_fundraising_activity(
        cls,
        owner_account_id: str,
        fra_id: str,
        updated_my_fra: "FundraisingActivity",
    ) -> bool:
        """US-15 — fundraiser updates one of their own activities.
        Returns True iff a row matched both fra_id AND owner_account_id;
        cross-owner writes are refused (rowcount stays 0).
        """
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity "
                "SET title = ?, description = ?, target_amount = ?, "
                "fra_cat_id = ?, start_date = ?, end_date = ?, "
                "completed = ?, suspended = ? "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (
                    updated_my_fra.title,
                    updated_my_fra.description,
                    str(updated_my_fra.target_amount),
                    updated_my_fra.fra_cat_id,
                    updated_my_fra.start_date.isoformat(),
                    updated_my_fra.end_date.isoformat(),
                    1 if updated_my_fra.completed else 0,
                    1 if updated_my_fra.suspended else 0,
                    fra_id,
                    owner_account_id,
                ),
            )
        return cursor.rowcount > 0

    @classmethod
    def view_fundraising_activity(
        cls, activity_id: str
    ) -> Optional["FundraisingActivity"]:
        with get_connection() as conn:
            row = conn.execute(
                f"SELECT {_SELECT_COLUMNS} FROM fundraising_activity "
                "WHERE fra_id = ?",
                (activity_id,),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

    @classmethod
    def view_all_fundraising_activities(cls) -> list["FundraisingActivity"]:
        """Exception A (CLAUDE.md): not on the US-21 diagram but needed so
        ViewFundraisingActivityPage can list activities for the donee to
        click. Logged in docs/todo.md. Suspended activities are hidden —
        only the owner sees them via view_my_fundraising_activities."""
        with get_connection() as conn:
            rows = conn.execute(
                f"SELECT {_SELECT_COLUMNS} FROM fundraising_activity "
                "WHERE suspended = 0 "
                "ORDER BY fra_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def view_fundraising_activity_view_count(cls, fra_id: str) -> int:
        """US-28 — fundraiser reads the view count of an activity. Returns
        0 when the row is missing (rather than raising) so callers can
        always display a number."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT view_count FROM fundraising_activity WHERE fra_id = ?",
                (fra_id,),
            ).fetchone()
        return int(row["view_count"]) if row is not None else 0

    @classmethod
    def view_fundraising_activity_save_count(cls, fra_id: str) -> int:
        """US-29 — fundraiser reads the save count of an activity. Returns
        0 when the row is missing."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT save_count FROM fundraising_activity WHERE fra_id = ?",
                (fra_id,),
            ).fetchone()
        return int(row["save_count"]) if row is not None else 0

    @classmethod
    def increment_view_count(cls, fra_id: str) -> bool:
        """Exception A: bump view_count by 1. Fired when a donee opens the
        activity detail in US-21. Returns True iff a row was updated."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity "
                "SET view_count = view_count + 1 WHERE fra_id = ?",
                (fra_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def increment_save_count(cls, fra_id: str, delta: int = 1) -> bool:
        """Exception A: bump save_count by delta (+1 on favourite,
        -1 on remove favourite). Floors at 0 so a missing favourite-record
        can't drive the count negative."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity "
                "SET save_count = MAX(save_count + ?, 0) WHERE fra_id = ?",
                (delta, fra_id),
            )
        return cursor.rowcount > 0

    @classmethod
    def _from_row(cls, row) -> "FundraisingActivity":
        return cls(
            fra_id=row["fra_id"],
            title=row["title"],
            description=row["description"],
            target_amount=Decimal(row["target_amount"]),
            fra_cat_id=row["fra_cat_id"],
            start_date=date.fromisoformat(row["start_date"]),
            end_date=date.fromisoformat(row["end_date"]),
            completed=bool(row["completed"]),
            suspended=bool(row["suspended"]),
            owner_account_id=row["owner_account_id"],
            view_count=int(row["view_count"]),
            save_count=int(row["save_count"]),
        )


def _alias_columns(alias: str) -> str:
    """Prefix the SELECT columns with a table alias for JOIN queries."""
    return ", ".join(f"{alias}.{col.strip()}" for col in _SELECT_COLUMNS.split(","))
