"""UserAccount <<Entity>> — Sprint 1 US-6.

Diagram contract (US-06.jpg):
    + createAccount(
        email: String, password: String, name: String, DOB: Date,
        phoneNum: String, profileId: String,
      ): UserAccount

Attributes from the class diagram: accountId, email, password, name, DOB,
phoneNum, profileId, suspended (Boolean).

The diagram does not declare email as unique; duplicates are permitted at
the entity layer. Login (US-11) will need to handle this, logged in
docs/todo.md as an architectural concern.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from persistence.db import get_connection
from persistence.ids import format_id, parse_id


@dataclass
class UserAccount:
    email: str
    password: str
    name: str
    dob: date
    phone_num: str
    profile_id: str
    suspended: bool = False
    account_id: Optional[str] = None

    @classmethod
    def create_account(
        cls,
        email: str,
        password: str,
        name: str,
        dob: date,
        phone_num: str,
        profile_id: str,
    ) -> "UserAccount":
        profile_rowid = parse_id(profile_id)
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO user_account "
                "(email, password, name, dob, phone_num, profile_id, suspended) "
                "VALUES (?, ?, ?, ?, ?, ?, 0)",
                (email, password, name, dob.isoformat(), phone_num, profile_rowid),
            )
            rowid = cursor.lastrowid
        return cls(
            account_id=format_id("acc", rowid),
            email=email,
            password=password,
            name=name,
            dob=dob,
            phone_num=phone_num,
            profile_id=profile_id,
            suspended=False,
        )
