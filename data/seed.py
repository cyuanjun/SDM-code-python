"""Seed data — idempotent bootstrap for the demo.

Solves the chicken-and-egg admin problem: the US-1 / US-6 diagrams imply
the actor is "User admin", but no admin can exist until someone creates
one. Without this seed, the first user to walk up has to create their
own admin profile + account before logging in.

Also seeds a handful of demo donations so US-32 / US-33 (donation
history) have data to display — no Sprint 1-3 diagram defines a "make
donation" use case, so without seeding the donation table would be
empty. Logged in docs/todo.md.

Idempotent — safe to call on every app start. Re-running does nothing if
an admin account already exists.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from entity.donation import Donation
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from persistence.db import get_connection
from persistence.ids import format_id

DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_ADMIN_PASSWORD = "admin"
DEFAULT_PM_EMAIL = "pm@example.com"
DEFAULT_PM_PASSWORD = "pm"


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


def seed_default_platform_manager() -> None:
    """Sprint 4 bootstrap: PM-only stories need a logged-in PM. Adds a
    default PM account if one doesn't already exist."""
    if _platform_manager_account_exists():
        return
    profile_id = _ensure_profile_for_role("platform_manager", "Default PM")
    UserAccount.create_account(
        email=DEFAULT_PM_EMAIL,
        password=DEFAULT_PM_PASSWORD,
        name="Default PM",
        dob=date(1985, 1, 1),
        phone_num="0000000003",
        profile_id=profile_id,
    )


def seed_demo_donations() -> None:
    """Idempotent: skips if any donation row already exists. Creates a
    fundraiser + donee + sample activity if needed, then a few donations.
    """
    if _any_donation_exists():
        return
    donee = _ensure_demo_donee()
    activity = _ensure_demo_activity()
    Donation.create_donation(
        account_id=donee.account_id, fra_id=activity.fra_id,
        amount=Decimal("50.00"), donation_date=date(2026, 1, 15),
    )
    Donation.create_donation(
        account_id=donee.account_id, fra_id=activity.fra_id,
        amount=Decimal("100.00"), donation_date=date(2026, 2, 20),
    )
    Donation.create_donation(
        account_id=donee.account_id, fra_id=activity.fra_id,
        amount=Decimal("25.50"), donation_date=date(2026, 3, 5),
    )


def _admin_account_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT a.account_id FROM user_account a "
            "JOIN user_profile p ON p.profile_id = a.profile_id "
            "WHERE p.role = 'admin' LIMIT 1"
        ).fetchone()
    return row is not None


def _platform_manager_account_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT a.account_id FROM user_account a "
            "JOIN user_profile p ON p.profile_id = a.profile_id "
            "WHERE p.role = 'platform_manager' LIMIT 1"
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


def _any_donation_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute("SELECT 1 FROM donation LIMIT 1").fetchone()
    return row is not None


def _ensure_demo_donee() -> UserAccount:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT a.account_id FROM user_account a "
            "JOIN user_profile p ON p.profile_id = a.profile_id "
            "WHERE p.role = 'donee' AND a.email = 'demo-donee@example.com' "
            "LIMIT 1"
        ).fetchone()
    if row is not None:
        account = UserAccount.view_user_account(
            format_id("acc", row["account_id"])
        )
        assert account is not None
        return account
    profile = _ensure_profile_for_role("donee", "Demo donee")
    return UserAccount.create_account(
        email="demo-donee@example.com",
        password="demo",
        name="Demo Donee",
        dob=date(2000, 1, 1),
        phone_num="0000000001",
        profile_id=profile,
    )


def _ensure_demo_activity() -> FundraisingActivity:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT fra_id FROM fundraising_activity "
            "WHERE title = 'Demo hospital fund' LIMIT 1"
        ).fetchone()
    if row is not None:
        activity = FundraisingActivity.view_fundraising_activity(
            format_id("fra", row["fra_id"])
        )
        assert activity is not None
        return activity
    fr_profile = _ensure_profile_for_role("fundraiser", "Demo fundraiser")
    fr = UserAccount.create_account(
        email="demo-fundraiser@example.com",
        password="demo",
        name="Demo Fundraiser",
        dob=date(1990, 1, 1),
        phone_num="0000000002",
        profile_id=fr_profile,
    )
    return FundraisingActivity.create_fundraising_activity(
        title="Demo hospital fund",
        description="Demo donations seeded for US-32/US-33",
        target_amount=Decimal("1000.00"),
        category="health",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31),
        owner_account_id=fr.account_id,
    )


def _ensure_profile_for_role(role: str, description: str) -> str:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT profile_id FROM user_profile WHERE role = ? LIMIT 1",
            (role,),
        ).fetchone()
    if row is not None:
        return format_id("prof", row["profile_id"])
    return UserProfile.create_profile(
        role=role, description=description
    ).profile_id
