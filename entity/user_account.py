"""UserAccount <<Entity>> — see Sprint 1 class diagrams (US-6, US-11/18/26/39 login)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from persistence.db import get_connection


@dataclass
class UserAccount:
    email: str
    password: str
    name: str
    dob: str
    phone_num: str
    profile_id: int
    suspended: bool = False

    @classmethod
    def login(cls, email: str, password: str) -> Optional["UserAccount"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT email, password, name, dob, phone_num, profile_id, suspended "
                "FROM user_account WHERE email = ? AND password = ? AND suspended = 0",
                (email, password),
            ).fetchone()
        if row is None:
            return None
        return cls(
            email=row["email"],
            password=row["password"],
            name=row["name"],
            dob=row["dob"],
            phone_num=row["phone_num"],
            profile_id=row["profile_id"],
            suspended=bool(row["suspended"]),
        )

    @classmethod
    def create_account(
        cls,
        email: str,
        password: str,
        name: str,
        dob: str,
        phone_num: str,
        profile_id: int,
    ) -> Optional["UserAccount"]:
        with get_connection() as conn:
            existing = conn.execute(
                "SELECT 1 FROM user_account WHERE email = ?", (email,)
            ).fetchone()
            if existing is not None:
                return None
            conn.execute(
                "INSERT INTO user_account (email, password, name, dob, phone_num, profile_id) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (email, password, name, dob, phone_num, profile_id),
            )
        return cls(
            email=email,
            password=password,
            name=name,
            dob=dob,
            phone_num=phone_num,
            profile_id=profile_id,
        )
