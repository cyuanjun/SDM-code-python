"""UserAccount <<Entity>>."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date
from typing import Optional


from persistence.db import get_connection
from persistence.ids import next_id


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
    ) -> Optional["UserAccount"]:
        try:
            with get_connection() as conn:
                new_id = next_id(conn, "user_account", "account_id", "acc")
                conn.execute(
                    "INSERT INTO user_account "
                    "(account_id, email, password, name, dob, phone_num, profile_id, suspended) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
                    (new_id, email, password, name, dob.isoformat(), phone_num, profile_id),
                )
        except sqlite3.IntegrityError:
            return None
        return cls(
            account_id=new_id,
            email=email,
            password=password,
            name=name,
            dob=dob,
            phone_num=phone_num,
            profile_id=profile_id,
            suspended=False,
        )

    @classmethod
    def view_user_account(cls, account_id: str) -> Optional["UserAccount"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, "
                "profile_id, suspended FROM user_account WHERE account_id = ?",
                (account_id,),
            ).fetchone()
        return None if row is None else cls._from_row(row)

    @classmethod
    def view_all_user_accounts(cls) -> list["UserAccount"]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, "
                "profile_id, suspended FROM user_account ORDER BY account_id"
            ).fetchall()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def update_user_account(
        cls, account_id: str, updated_account: "UserAccount"
    ) -> bool:
        try:
            with get_connection() as conn:
                cursor = conn.execute(
                    "UPDATE user_account SET email = ?, password = ?, name = ?, "
                    "dob = ?, phone_num = ?, profile_id = ?, suspended = ? "
                    "WHERE account_id = ?",
                    (
                        updated_account.email,
                        updated_account.password,
                        updated_account.name,
                        updated_account.dob.isoformat(),
                        updated_account.phone_num,
                        updated_account.profile_id,
                        1 if updated_account.suspended else 0,
                        account_id,
                    ),
                )
                affected = cursor.rowcount
        except sqlite3.IntegrityError:
            return False
        return affected > 0

    @classmethod
    def _from_row(cls, row) -> "UserAccount":
        return cls(
            account_id=row["account_id"],
            email=row["email"],
            password=row["password"],
            name=row["name"],
            dob=date.fromisoformat(row["dob"]),
            phone_num=row["phone_num"],
            profile_id=row["profile_id"],
            suspended=bool(row["suspended"]),
        )

    @classmethod
    def login(cls, email: str, password: str) -> Optional["UserAccount"]:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, "
                "profile_id, suspended FROM user_account "
                "WHERE email = ? AND password = ? AND suspended = 0 "
                "ORDER BY account_id LIMIT 1",
                (email, password),
            ).fetchone()
        return None if row is None else cls._from_row(row)

    @classmethod
    def suspend_user_account(cls, account_id: str) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_account SET suspended = 1 WHERE account_id = ?",
                (account_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def unsuspend_user_account(cls, account_id: str) -> bool:
        with get_connection() as conn:
            cursor = conn.execute(
                "UPDATE user_account SET suspended = 0 WHERE account_id = ?",
                (account_id,),
            )
        return cursor.rowcount > 0

    @classmethod
    def search_user_account(cls, search_criteria: str) -> list["UserAccount"]:
        like = f"%{search_criteria.lower()}%"
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT account_id, email, password, name, dob, phone_num, "
                "profile_id, suspended FROM user_account "
                "WHERE LOWER(email) LIKE ? OR LOWER(name) LIKE ? "
                "ORDER BY account_id",
                (like, like),
            ).fetchall()
        return [cls._from_row(row) for row in rows]
