"""FundraisingActivity <<Entity>> — see Sprint 1 class diagrams (US-13, US-21)."""
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
    owner_email: Optional[str] = None

    def save_fundraising_activity(self) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO fundraising_activity "
                "(title, description, target_amount, category, start_date, end_date, status, owner_email) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.title,
                    self.description,
                    self.target_amount,
                    self.category,
                    self.start_date,
                    self.end_date,
                    self.status,
                    self.owner_email,
                ),
            )
            self.activity_id = cursor.lastrowid
        return self.activity_id is not None

    @classmethod
    def view_all_fundraising_activities(cls) -> list["FundraisingActivity"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT activity_id, title, description, target_amount, category, "
                "start_date, end_date, status, owner_email "
                "FROM fundraising_activity ORDER BY activity_id"
            ).fetchall()
        return [
            cls(
                activity_id=row["activity_id"],
                title=row["title"],
                description=row["description"],
                target_amount=row["target_amount"],
                category=row["category"],
                start_date=row["start_date"],
                end_date=row["end_date"],
                status=row["status"],
                owner_email=row["owner_email"],
            )
            for row in rows
        ]

    @classmethod
    def view_fundraising_activity_details(
        cls, activity_id: str
    ) -> Optional["FundraisingActivity"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT activity_id, title, description, target_amount, category, "
                "start_date, end_date, status, owner_email "
                "FROM fundraising_activity WHERE activity_id = ?",
                (activity_id,),
            ).fetchone()
        if row is None:
            return None
        return cls(
            activity_id=row["activity_id"],
            title=row["title"],
            description=row["description"],
            target_amount=row["target_amount"],
            category=row["category"],
            start_date=row["start_date"],
            end_date=row["end_date"],
            status=row["status"],
            owner_email=row["owner_email"],
        )
