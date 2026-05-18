"""Donation <<Entity>>."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from persistence.db import get_connection
from persistence.ids import next_id


@dataclass
class Donation:
    account_id: str
    fra_id: str
    amount: Decimal
    donation_date: date
    donation_id: Optional[str] = None

    @classmethod
    def create_donation(
        cls,
        account_id: str,
        fra_id: str,
        amount: Decimal,
        donation_date: date,
    ) -> "Donation":
        with get_connection() as conn:
            new_id = next_id(conn, "donation", "donation_id", "don")
            conn.execute(
                "INSERT INTO donation "
                "(donation_id, account_id, fra_id, amount, donation_date) "
                "VALUES (?, ?, ?, ?, ?)",
                (new_id, account_id, fra_id, str(amount), donation_date.isoformat()),
            )
        return cls(
            donation_id=new_id,
            account_id=account_id,
            fra_id=fra_id,
            amount=amount,
            donation_date=donation_date,
        )

    @classmethod
    def search_my_donation_history(
        cls, account_id: str, search_criteria: str
    ) -> list["Donation"]:
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT d.donation_id, d.account_id, d.fra_id, d.amount, "
                "d.donation_date "
                "FROM donation d "
                "JOIN fundraising_activity a ON a.fra_id = d.fra_id "
                "JOIN fundraising_activity_category c ON c.fra_cat_id = a.fra_cat_id "
                "WHERE d.account_id = ? AND ("
                "  LOWER(a.title) LIKE ? OR LOWER(a.description) LIKE ? "
                "  OR LOWER(c.category_name) LIKE ?"
                ") ORDER BY d.donation_id",
                (account_id, like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def view_my_donation_histories(cls, account_id: str) -> list["Donation"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT donation_id, account_id, fra_id, amount, donation_date "
                "FROM donation WHERE account_id = ? ORDER BY donation_id",
                (account_id,),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row) -> "Donation":
        return cls(
            donation_id=row["donation_id"],
            account_id=row["account_id"],
            fra_id=row["fra_id"],
            amount=Decimal(row["amount"]),
            donation_date=date.fromisoformat(row["donation_date"]),
        )
