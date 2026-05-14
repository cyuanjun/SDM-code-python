"""UserAccount <<Entity>> — Sprint 1 US-6 + US-11/18/26/39.

Diagram contracts:
    US-06.jpg: + createAccount(
        email: String, password: String, name: String, DOB: Date,
        phoneNum: String, profileId: String,
      ): UserAccount
    US-11/18/26/39.jpg: + login(email: String, password: String): UserAccount

The diagrams do not show a failure branch for login. Implementation
returns None on no match so the Boundary can call displayError. Logged
in docs/todo.md as a missing diagram branch.

The diagram does not declare email as unique; duplicates are permitted at
the entity layer. When duplicates exist with the same password, login
returns the first row (lowest account_id). Logged in docs/todo.md.
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

    @classmethod
    def login(cls, email: str, password: str) -> Optional["UserAccount"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, "
                "profile_id, suspended FROM user_account "
                "WHERE email = ? AND password = ? "
                "ORDER BY account_id LIMIT 1",
                (email, password),
            ).fetchone()
        if row is None:
            return None
        return cls(
            account_id=format_id("acc", row["account_id"]),
            email=row["email"],
            password=row["password"],
            name=row["name"],
            dob=date.fromisoformat(row["dob"]),
            phone_num=row["phone_num"],
            profile_id=format_id("prof", row["profile_id"]),
            suspended=bool(row["suspended"]),
        )
