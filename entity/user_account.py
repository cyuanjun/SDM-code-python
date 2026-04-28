"""UserAccount <<Entity>> — Sprint 1 (US-6, login) + Sprint 2 (US-7 view, US-8 update)."""
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
    account_id: Optional[int] = None
    suspended: bool = False

    @classmethod
    def login(cls, email: str, password: str) -> Optional["UserAccount"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, profile_id, suspended "
                "FROM user_account WHERE email = ? AND password = ? AND suspended = 0",
                (email, password),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

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
            cursor = conn.execute(
                "INSERT INTO user_account (email, password, name, dob, phone_num, profile_id) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (email, password, name, dob, phone_num, profile_id),
            )
            account_id = cursor.lastrowid
        return cls(
            email=email,
            password=password,
            name=name,
            dob=dob,
            phone_num=phone_num,
            profile_id=profile_id,
            account_id=account_id,
        )

    @classmethod
    def view_user_account(cls, account_id: str) -> Optional["UserAccount"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, profile_id, suspended "
                "FROM user_account WHERE account_id = ?",
                (account_id,),
            ).fetchone()
        if row is None:
            return None
        return cls._from_row(row)

    @classmethod
    def view_all_user_accounts(cls) -> list["UserAccount"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, profile_id, suspended "
                "FROM user_account ORDER BY account_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def update_user_account(
        cls, account_id: str, updated_account: "UserAccount"
    ) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_account SET email = ?, password = ?, name = ?, dob = ?, "
                "phone_num = ?, profile_id = ?, suspended = ? WHERE account_id = ?",
                (
                    updated_account.email,
                    updated_account.password,
                    updated_account.name,
                    updated_account.dob,
                    updated_account.phone_num,
                    updated_account.profile_id,
                    int(updated_account.suspended),
                    account_id,
                ),
            )
        return cursor.rowcount > 0

    @classmethod
    def _from_row(cls, row) -> "UserAccount":
        return cls(
            account_id=row["account_id"],
            email=row["email"],
            password=row["password"],
            name=row["name"],
            dob=row["dob"],
            phone_num=row["phone_num"],
            profile_id=row["profile_id"],
            suspended=bool(row["suspended"]),
        )
