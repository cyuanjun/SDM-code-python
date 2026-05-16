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
    def suspend_my_fundraising_activity(
        cls, owner_account_id: str, fra_id: str
    ) -> bool:
        """US-16 — fundraiser suspends one of their own activities.
        Ownership scoped: UPDATE … WHERE fra_id AND owner_account_id."""
        owner_rowid = parse_id(owner_account_id)
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity SET suspended = 1 "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (rowid, owner_rowid),
            )
        return cursor.rowcount > 0

    @classmethod
    def unsuspend_my_fundraising_activity(
        cls, owner_account_id: str, fra_id: str
    ) -> bool:
        """Exception A — mirror of suspend so the UI can toggle.
        Logged in docs/diagram_typos.md."""
        owner_rowid = parse_id(owner_account_id)
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity SET suspended = 0 "
                "WHERE fra_id = ? AND owner_account_id = ?",
                (rowid, owner_rowid),
            )
        return cursor.rowcount > 0

    @classmethod
    def search_my_fundraising_activity(
        cls, owner_account_id: str, search_criteria: str
    ) -> list["FundraisingActivity"]:
        """US-17 — fundraiser searches their own activities. Case-insensitive
        substring match against title / description / category, scoped to
        owner_account_id."""
        owner_rowid = parse_id(owner_account_id)
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "WHERE owner_account_id = ? AND ("
                "  LOWER(title) LIKE ? OR LOWER(description) LIKE ? "
                "  OR LOWER(category) LIKE ?"
                ") ORDER BY fra_id",
                (owner_rowid, like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def search_my_completed_fra(
        cls, owner_account_id: str, search_criteria: str
    ) -> list["FundraisingActivity"]:
        """US-30 — fundraiser searches their completed activities. Scoped
        to owner + completed = 1."""
        owner_rowid = parse_id(owner_account_id)
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "WHERE owner_account_id = ? AND completed = 1 AND ("
                "  LOWER(title) LIKE ? OR LOWER(description) LIKE ? "
                "  OR LOWER(category) LIKE ?"
                ") ORDER BY fra_id",
                (owner_rowid, like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def view_my_completed_activity(
        cls, owner_account_id: str, fra_id: str
    ) -> Optional["FundraisingActivity"]:
        """US-31 — fundraiser views one of their completed activities.
        Returns None if the row is missing, owned by someone else, OR
        not yet completed."""
        owner_rowid = parse_id(owner_account_id)
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            row = conn.execute(
                "SELECT fra_id, title, description, target_amount, category, "
                "start_date, end_date, completed, suspended, owner_account_id, "
                "view_count, save_count FROM fundraising_activity "
                "WHERE fra_id = ? AND owner_account_id = ? AND completed = 1",
                (rowid, owner_rowid),
            ).fetchone()
        return None if row is None else cls._from_row(row)

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
                    updated_my_fra.title,
                    updated_my_fra.description,
                    str(updated_my_fra.target_amount),
                    updated_my_fra.category,
                    updated_my_fra.start_date.isoformat(),
                    updated_my_fra.end_date.isoformat(),
                    1 if updated_my_fra.completed else 0,
                    1 if updated_my_fra.suspended else 0,
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
    def view_fundraising_activity_view_count(cls, fra_id: str) -> int:
        """US-28 — fundraiser reads the view count of an activity. Returns
        0 when the row is missing (rather than raising) so callers can
        always display a number."""
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            row = conn.execute(
                "SELECT view_count FROM fundraising_activity WHERE fra_id = ?",
                (rowid,),
            ).fetchone()
        return int(row["view_count"]) if row is not None else 0

    @classmethod
    def view_fundraising_activity_save_count(cls, fra_id: str) -> int:
        """US-29 — fundraiser reads the save count of an activity. Returns
        0 when the row is missing."""
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            row = conn.execute(
                "SELECT save_count FROM fundraising_activity WHERE fra_id = ?",
                (rowid,),
            ).fetchone()
        return int(row["save_count"]) if row is not None else 0

    @classmethod
    def increment_view_count(cls, fra_id: str) -> bool:
        """Exception A: bump view_count by 1. Fired when a donee opens the
        activity detail in US-21. Returns True iff a row was updated."""
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity "
                "SET view_count = view_count + 1 WHERE fra_id = ?",
                (rowid,),
            )
        return cursor.rowcount > 0

    @classmethod
    def increment_save_count(cls, fra_id: str, delta: int = 1) -> bool:
        """Exception A: bump save_count by delta (+1 on favourite,
        -1 on remove favourite). Floors at 0 so a missing favourite-record
        can't drive the count negative."""
        rowid = parse_id(fra_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity "
                "SET save_count = MAX(save_count + ?, 0) WHERE fra_id = ?",
                (delta, rowid),
            )
        return cursor.rowcount > 0

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
