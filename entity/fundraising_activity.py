"""FundraisingActivity <<Entity>> — Sprint 1 US-13, US-21.

Diagram contracts:
    US-13.jpg: + createFundraisingActivity(
        title: String, description: String, targetAmount: Decimal,
        category: String, startDate: Date, endDate: Date,
      ): FundraisingActivity
    US-21.jpg: + viewFundraisingActivity(activityId: String): FundraisingActivity

Implementation adds `owner_account_id` to create_fundraising_activity even
though the diagram method signature omits it; the entity attribute
`ownerAccountId` would otherwise have nowhere to come from. Logged in
docs/todo.md as a Sprint 1 diagram typo.

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
from persistence.ids import format_id, parse_id


@dataclass
class FundraisingActivity:
    title: str
    description: str
    target_amount: Decimal
    category: str
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
        category: str,
        start_date: date,
        end_date: date,
        owner_account_id: str,
    ) -> "FundraisingActivity":
        owner_rowid = parse_id(owner_account_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO fundraising_activity "
                "(title, description, target_amount, category, start_date, "
                " end_date, completed, suspended, owner_account_id, view_count, save_count) "
                "VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?, 0, 0)",
                (
                    title,
                    description,
                    str(target_amount),
                    category,
                    start_date.isoformat(),
                    end_date.isoformat(),
                    owner_rowid,
                ),
            )
            rowid = cursor.lastrowid
        return cls(
            fra_id=format_id("fra", rowid),
            title=title,
            description=description,
            target_amount=target_amount,
            category=category,
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
        owner_rowid = parse_id(owner_account_id)
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            row = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (rowid, owner_rowid),
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
        owner_rowid = parse_id(owner_account_id)
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "WHERE owner_account_id = ? ORDER BY fra_id",
                (owner_rowid,),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def search_fundraising_activity(
        cls, search_criteria: str
    ) -> list["FundraisingActivity"]:
        """US-20 — donee searches activities by criteria. Case-insensitive
        substring match against title, description, or category."""
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "WHERE LOWER(title) LIKE ? "
                "   OR LOWER(description) LIKE ? "
                "   OR LOWER(category) LIKE ? "
                "ORDER BY fra_id",
                (like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def update_fundraiser_activity(
        cls,
        owner_account_id: str,
        fra_id: str,
        updated_activity: "FundraisingActivity",
    ) -> bool:
        """US-15 — fundraiser updates one of their own activities.
        Returns True iff a row matched both fra_id AND owner_account_id;
        cross-owner writes are refused (rowcount stays 0).
        The diagram's class-level method signature omits owner_account_id
        but the sequence diagram includes it — logged as a Sprint 2 typo.
        """
        owner_rowid = parse_id(owner_account_id)
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity "
                "SET title = ?, description = ?, target_amount = ?, "
                "category = ?, start_date = ?, end_date = ?, "
                "completed = ?, suspended = ? "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (
                    updated_activity.title,
                    updated_activity.description,
                    str(updated_activity.target_amount),
                    updated_activity.category,
                    updated_activity.start_date.isoformat(),
                    updated_activity.end_date.isoformat(),
                    1 if updated_activity.completed else 0,
                    1 if updated_activity.suspended else 0,
                    rowid,
                    owner_rowid,
                ),
            )
        return cursor.rowcount > 0

    @classmethod
    def view_fundraising_activity(
        cls, activity_id: str
    ) -> Optional["FundraisingActivity"]:
        rowid = parse_id(activity_id)
        with get_connection() as conn:
            row = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "WHERE fra_id = ?",
                (rowid,),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

    @classmethod
    def view_all_fundraising_activities(cls) -> list["FundraisingActivity"]:
        """Exception A (CLAUDE.md): not on the US-21 diagram but needed so
        ViewFundraisingActivityPage can list activities for the donee to
        click. Logged in docs/todo.md."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "ORDER BY fra_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row) -> "FundraisingActivity":
        return cls(
            fra_id=format_id("fra", row["fra_id"]),
            title=row["title"],
            description=row["description"],
            target_amount=Decimal(row["target_amount"]),
            category=row["category"],
            start_date=date.fromisoformat(row["start_date"]),
            end_date=date.fromisoformat(row["end_date"]),
            completed=bool(row["completed"]),
            suspended=bool(row["suspended"]),
            owner_account_id=format_id("acc", row["owner_account_id"]),
            view_count=int(row["view_count"]),
            save_count=int(row["save_count"]),
        )
