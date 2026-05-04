"""FundraisingActivity <<Entity>> — Sprint 1 (US-13, US-21) + Sprint 2 (US-14, US-15, US-20)
+ Sprint 3 (US-16 suspend, US-17 fundraiser search, US-30 search completed, US-31 view completed).

Note on owner field: Sprint 2 migrated owner_email -> owner_account_id to track
account_id as the primary key. Sprint 1 callers passing owner_email should
update to owner_account_id.

Sprint 3 update: submit_search_criteria gained owner_account_id and status
filter parameters to disambiguate the four use cases (US-17, US-20, US-30,
deferred US-32) sharing the diagram method name. Diagrams to be updated
before final marking — see docs/todo.md.
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
        cls,
        search_criteria: str,
        owner_account_id: Optional[int] = None,
        status: Optional[str] = None,
    ) -> list["FundraisingActivity"]:
        """Shared search for US-17, US-20, US-30. Matches title, description,
        or category (case-insensitive substring). Optional filters narrow to
        a specific owner (US-17, US-30) and/or a specific status (US-30).
        """
        like = f"%{search_criteria}%"
        sql = (
            "SELECT activity_id, title, description, target_amount, category, "
            "start_date, end_date, status, owner_account_id "
            "FROM fundraising_activity "
            "WHERE (title LIKE ? OR description LIKE ? OR category LIKE ?)"
        )
        params: list = [like, like, like]
        if owner_account_id is not None:
            sql += " AND owner_account_id = ?"
            params.append(owner_account_id)
        if status is not None:
            sql += " AND status = ?"
            params.append(status)
        sql += " ORDER BY activity_id"
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def suspend_fundraising_activity(cls, activity_id: str) -> bool:
        """US-16 — fundraiser suspends donations on their activity."""
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE fundraising_activity SET status = 'suspended' "
                "WHERE activity_id = ?",
                (activity_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def view_completed_activity(
        cls, activity_id: str
    ) -> Optional["FundraisingActivity"]:
        """US-31 — fundraiser views one of their completed activities. Returns
        None when the row is missing or its status is not 'completed'."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT activity_id, title, description, target_amount, category, "
                "start_date, end_date, status, owner_account_id "
                "FROM fundraising_activity "
                "WHERE activity_id = ? AND status = 'completed'",
                (activity_id,),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

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
