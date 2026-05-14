"""Seed data — idempotent bootstrap for the demo.

Solves the chicken-and-egg admin problem: the US-1 / US-6 diagrams imply
the actor is "User admin", but no admin can exist until someone creates
one. Without this seed, the first user to walk up has to create their
own admin profile + account before logging in.

Idempotent — safe to call on every app start. Re-running does nothing if
an admin account already exists.

Logged in docs/todo.md as a bootstrap deviation from the diagrams.
"""
from __future__ import annotations

from datetime import date

from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from persistence.db import get_connection
from persistence.ids import format_id

DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_ADMIN_PASSWORD = "admin"


def seed_default_admin() -> None:
    if _admin_account_exists():
        return
    profile_id = _ensure_admin_profile()
    UserAccount.create_account(
        email=DEFAULT_ADMIN_EMAIL,
        password=DEFAULT_ADMIN_PASSWORD,
        name="Default Admin",
        dob=date(2000, 1, 1),
        phone_num="0000000000",
        profile_id=profile_id,
    )


def _admin_account_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT a.account_id FROM user_account a "
            "JOIN user_profile p ON p.profile_id = a.profile_id "
            "WHERE p.role = 'admin' LIMIT 1"
        ).fetchone()
    return row is not None


def _ensure_admin_profile() -> str:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT profile_id FROM user_profile WHERE role = 'admin' LIMIT 1"
        ).fetchone()
    if row is not None:
        return format_id("prof", row["profile_id"])
    profile = UserProfile.create_profile(
        role="admin",
        description="Default admin (bootstrap)",
    )
    return profile.profile_id
