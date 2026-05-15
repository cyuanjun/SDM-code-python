"""Seed data — idempotent bootstrap for the demo.

Solves the chicken-and-egg admin problem: the US-1 / US-6 diagrams imply
the actor is "User admin", but no admin can exist until someone creates
one. Also seeds one default account per role (admin / fundraiser / donee
/ platform_manager) so the demo is reachable without any pre-work, plus
three sample donations so US-32 / US-33 have data to display.

Idempotent — every helper checks for the existing row before creating.

Default credentials (short role prefix + 001 = the first seeded account
for that role; room to grow with a002 etc.):
    a001@a.com    / 123   (admin)
    fr001@a.com   / 123   (fundraiser)
    d001@a.com    / 123   (donee)
    pm001@a.com   / 123   (platform manager)
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

DEFAULT_PASSWORD = "123"

DEFAULT_ADMIN_EMAIL = "a001@a.com"
DEFAULT_ADMIN_PASSWORD = DEFAULT_PASSWORD
DEFAULT_FUNDRAISER_EMAIL = "fr001@a.com"
DEFAULT_FUNDRAISER_PASSWORD = DEFAULT_PASSWORD
DEFAULT_DONEE_EMAIL = "d001@a.com"
DEFAULT_DONEE_PASSWORD = DEFAULT_PASSWORD
DEFAULT_PM_EMAIL = "pm001@a.com"
DEFAULT_PM_PASSWORD = DEFAULT_PASSWORD

_DEFAULT_DOB = date(2000, 1, 1)


def seed_default_admin() -> None:
    _ensure_role_account(
        role="admin",
        profile_description="Default admin (bootstrap)",
        email=DEFAULT_ADMIN_EMAIL,
        password=DEFAULT_ADMIN_PASSWORD,
        name="Default Admin",
        phone_num="0000000000",
    )


def seed_default_fundraiser() -> None:
    _ensure_role_account(
        role="fundraiser",
        profile_description="Default fundraiser",
        email=DEFAULT_FUNDRAISER_EMAIL,
        password=DEFAULT_FUNDRAISER_PASSWORD,
        name="Default Fundraiser",
        phone_num="0000000001",
    )


def seed_default_donee() -> None:
    _ensure_role_account(
        role="donee",
        profile_description="Default donee",
        email=DEFAULT_DONEE_EMAIL,
        password=DEFAULT_DONEE_PASSWORD,
        name="Default Donee",
        phone_num="0000000002",
    )


def seed_default_platform_manager() -> None:
    _ensure_role_account(
        role="platform_manager",
        profile_description="Default PM",
        email=DEFAULT_PM_EMAIL,
        password=DEFAULT_PM_PASSWORD,
        name="Default PM",
        phone_num="0000000003",
    )


def seed_demo_donations() -> None:
    """Three sample donations from the default donee against a demo
    activity owned by the default fundraiser. Skips if any donation row
    already exists."""
    if _any_donation_exists():
        return
    seed_default_fundraiser()
    seed_default_donee()
    donee = UserAccount.login(DEFAULT_DONEE_EMAIL, DEFAULT_DONEE_PASSWORD)
    assert donee is not None, "donee seed did not create a logged-in-able row"

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


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------


def _ensure_role_account(
    *,
    role: str,
    profile_description: str,
    email: str,
    password: str,
    name: str,
    phone_num: str,
) -> None:
    """Idempotent: create the profile-for-role + account if either is
    missing. Matches by email so re-runs don't duplicate."""
    if _account_with_email_exists(email):
        return
    profile_id = _ensure_profile_for_role(role, profile_description)
    UserAccount.create_account(
        email=email,
        password=password,
        name=name,
        dob=_DEFAULT_DOB,
        phone_num=phone_num,
        profile_id=profile_id,
    )


def _account_with_email_exists(email: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM user_account WHERE email = ? LIMIT 1", (email,)
        ).fetchone()
    return row is not None


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


def _any_donation_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute("SELECT 1 FROM donation LIMIT 1").fetchone()
    return row is not None


def _ensure_demo_activity() -> FundraisingActivity:
    """Pick the default fundraiser's first activity, or create a demo one
    if they don't have any. The demo activity is what the seeded donations
    point at."""
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

    fundraiser = UserAccount.login(
        DEFAULT_FUNDRAISER_EMAIL, DEFAULT_FUNDRAISER_PASSWORD
    )
    assert fundraiser is not None, (
        "default fundraiser must exist before seeding demo activity"
    )
    return FundraisingActivity.create_fundraising_activity(
        title="Demo hospital fund",
        description="Demo donations seeded for US-32/US-33",
        target_amount=Decimal("1000.00"),
        category="health",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31),
        owner_account_id=fundraiser.account_id,
    )
