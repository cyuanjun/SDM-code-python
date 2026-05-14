"""Donation <<Entity>> — Sprint 3 US-32, US-33.

Diagram contracts:
    US-32.jpg: + searchDonationHistory(searchCriteria: String, accountId: String): List<Donation>
               (class diagram types accountId as Integer — typo logged.)
    US-33.jpg: + viewMyDonationHistory(accountId: String, donationId: String): Donation

Attributes: donationId, accountId, FRAId, amount (Decimal), donationDate (Date).

No "make donation" use case exists on any Sprint 1-3 diagram. data/seed.py
creates a handful of demo donations so US-32/33 have data to display.
A `create_donation` classmethod is provided here so the seed can call it
through the entity rather than writing raw SQL.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from persistence.db import get_connection
from persistence.ids import format_id, parse_id


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
        account_rowid = parse_id(account_id)
        fra_rowid = parse_id(fra_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO donation "
                "(account_id, fra_id, amount, donation_date) "
                "VALUES (?, ?, ?, ?)",
                (account_rowid, fra_rowid, str(amount), donation_date.isoformat()),
            )
            rowid = cursor.lastrowid
        return cls(
            donation_id=format_id("don", rowid),
            account_id=account_id,
            fra_id=fra_id,
            amount=amount,
            donation_date=donation_date,
        )

    @classmethod
    def search_donation_history(
        cls, search_criteria: str, account_id: str
    ) -> list["Donation"]:
        """US-32 — donee searches donation history. Joins to
        fundraising_activity and matches title / description / category."""
        account_rowid = parse_id(account_id)
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT d.donation_id, d.account_id, d.fra_id, d.amount, "
                "d.donation_date "
                "FROM donation d "
                "JOIN fundraising_activity a ON a.fra_id = d.fra_id "
                "WHERE d.account_id = ? AND ("
                "  LOWER(a.title) LIKE ? OR LOWER(a.description) LIKE ? "
                "  OR LOWER(a.category) LIKE ?"
                ") ORDER BY d.donation_id",
                (account_rowid, like, like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def view_my_donation_history(
        cls, account_id: str, donation_id: str
    ) -> Optional["Donation"]:
        """US-33 — donee views one of their donations. Returns None when
        the row is missing or belongs to another donee."""
        account_rowid = parse_id(account_id)
        rowid = parse_id(donation_id)
        with get_connection() as conn:
            row = conn.execute(
                "SELECT donation_id, account_id, fra_id, amount, donation_date "
                "FROM donation WHERE donation_id = ? AND account_id = ?",
                (rowid, account_rowid),
            ).fetchone()
        return None if row is None else cls._from_row(row)

    @classmethod
    def view_my_donations(cls, account_id: str) -> list["Donation"]:
        """Exception A: list-by-owner so ViewMyDonationHistoryPage can show
        a picker. Logged in docs/todo.md."""
        account_rowid = parse_id(account_id)
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT donation_id, account_id, fra_id, amount, donation_date "
                "FROM donation WHERE account_id = ? ORDER BY donation_id",
                (account_rowid,),
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def _from_row(cls, row) -> "Donation":
        return cls(
            donation_id=format_id("don", row["donation_id"]),
            account_id=format_id("acc", row["account_id"]),
            fra_id=format_id("fra", row["fra_id"]),
            amount=Decimal(row["amount"]),
            donation_date=date.fromisoformat(row["donation_date"]),
        )
