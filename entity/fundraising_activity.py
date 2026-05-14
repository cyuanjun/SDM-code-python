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
