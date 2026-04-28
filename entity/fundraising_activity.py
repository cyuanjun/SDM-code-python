"""FundraisingActivity <<Entity>> — Sprint 1 (US-13, US-21) + Sprint 2 (US-14, US-15, US-20).

Note on owner field: Sprint 2 migrated owner_email -> owner_account_id to track
account_id as the primary key. Sprint 1 callers passing owner_email should
update to owner_account_id.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection


@dataclass
class FundraisingActivity:
    title: str
    description: str
    target_amount: float
    category: str
    start_date: str
    end_date: str
    status: str
    activity_id: Optional[int] = None
    owner_account_id: Optional[int] = None

    def save_fundraising_activity(self) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO fundraising_activity "
                "(title, description, target_amount, category, start_date, end_date, "
                "status, owner_account_id) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.title,
                    self.description,
                    self.target_amount,
                    self.category,
                    self.start_date,
                    self.end_date,
                    self.status,
                    self.owner_account_id,
                ),
            )
            self.activity_id = cursor.lastrowid
        return self.activity_id is not None

    @classmethod
    def view_fundraising_activity_details(
        cls, activity_id: str
    ) -> Optional["FundraisingActivity"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT activity_id, title, description, target_amount, category, "
                "start_date, end_date, status, owner_account_id "
                "FROM fundraising_activity WHERE activity_id = ?",
                (activity_id,),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

    @classmethod
    def view_all_fundraising_activities(cls) -> list["FundraisingActivity"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT activity_id, title, description, target_amount, category, "
                "start_date, end_date, status, owner_account_id "
                "FROM fundraising_activity ORDER BY activity_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def view_fundraiser_activity(
        cls, activity_id: str
    ) -> Optional["FundraisingActivity"]:
        """US-14 — view a fundraiser's specific activity. Same lookup as
        view_fundraising_activity_details; ownership filtering is done at the
        Boundary list view."""
        return cls.view_fundraising_activity_details(activity_id)

    @classmethod
    def view_activities_by_owner(
        cls, owner_account_id: int
    ) -> list["FundraisingActivity"]:
        """Helper for the fundraiser list view (US-14/US-15). Not on diagram —
        Boundary uses this to scope the list to the current fundraiser."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT activity_id, title, description, target_amount, category, "
                "start_date, end_date, status, owner_account_id "
                "FROM fundraising_activity WHERE owner_account_id = ? "
                "ORDER BY activity_id",
                (owner_account_id,),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def update_fundraiser_activity(
        cls, activity_id: str, updated_fundraiser: "FundraisingActivity"
    ) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity SET title = ?, description = ?, "
                "target_amount = ?, category = ?, start_date = ?, end_date = ?, "
                "status = ? WHERE activity_id = ?",
                (
                    updated_fundraiser.title,
                    updated_fundraiser.description,
                    updated_fundraiser.target_amount,
                    updated_fundraiser.category,
                    updated_fundraiser.start_date,
                    updated_fundraiser.end_date,
                    updated_fundraiser.status,
                    activity_id,
                ),
            )
        return cursor.rowcount > 0

    @classmethod
    def submit_search_criteria(
        cls, search_criteria: str
    ) -> list["FundraisingActivity"]:
        """US-20 — donee searches activities. Matches title, description, or
        category (case-insensitive substring)."""
        like = f"%{search_criteria}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT activity_id, title, description, target_amount, category, "
                "start_date, end_date, status, owner_account_id "
                "FROM fundraising_activity "
                "WHERE title LIKE ? OR description LIKE ? OR category LIKE ? "
                "ORDER BY activity_id",
                (like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row) -> "FundraisingActivity":
        return cls(
            activity_id=row["activity_id"],
            title=row["title"],
            description=row["description"],
            target_amount=row["target_amount"],
            category=row["category"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            status=row["status"],
            owner_account_id=row["owner_account_id"],
        )
