"""Tests for data/seed.py — every seeded role account must be idempotent
and reachable via the login flow."""
from __future__ import annotations

from datetime import date

from data.seed import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_DONEE_EMAIL,
    DEFAULT_DONEE_PASSWORD,
    DEFAULT_FUNDRAISER_EMAIL,
    DEFAULT_FUNDRAISER_PASSWORD,
    DEFAULT_PM_EMAIL,
    DEFAULT_PM_PASSWORD,
    seed_default_admin,
    seed_default_donee,
    seed_default_fundraiser,
    seed_default_platform_manager,
    seed_demo_donations,
)
from entity.donation import Donation
from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from persistence.db import get_connection


def _account_count() -> int:
    with get_connection() as conn:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM user_account"
        ).fetchone()["n"]


def test_seed_admin_creates_account_on_empty_db() -> None:
    seed_default_admin()
    admin = UserAccount.login(DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD)
    assert admin is not None
    assert admin.email == DEFAULT_ADMIN_EMAIL


def test_seed_admin_is_idempotent() -> None:
    seed_default_admin()
    seed_default_admin()
    seed_default_admin()
    assert _account_count() == 1


def test_seed_admin_reuses_existing_admin_profile() -> None:
    """Negative path: an admin profile already exists — the seed must use
    it instead of creating a second."""
    existing = UserProfile.create_profile(
        role="admin", description="manually created"
    )
    seed_default_admin()
    profiles = UserProfile.view_all_profiles()
    assert len(profiles) == 1
    assert profiles[0].profile_id == existing.profile_id


def test_seed_fundraiser_creates_account_on_empty_db() -> None:
    seed_default_fundraiser()
    fr = UserAccount.login(
        DEFAULT_FUNDRAISER_EMAIL, DEFAULT_FUNDRAISER_PASSWORD
    )
    assert fr is not None
    assert fr.email == DEFAULT_FUNDRAISER_EMAIL


def test_seed_fundraiser_is_idempotent() -> None:
    seed_default_fundraiser()
    seed_default_fundraiser()
    seed_default_fundraiser()
    assert _account_count() == 1


def test_seed_donee_creates_account_on_empty_db() -> None:
    seed_default_donee()
    donee = UserAccount.login(DEFAULT_DONEE_EMAIL, DEFAULT_DONEE_PASSWORD)
    assert donee is not None
    assert donee.email == DEFAULT_DONEE_EMAIL


def test_seed_donee_is_idempotent() -> None:
    seed_default_donee()
    seed_default_donee()
    assert _account_count() == 1


def test_seed_pm_creates_account_on_empty_db() -> None:
    seed_default_platform_manager()
    pm = UserAccount.login(DEFAULT_PM_EMAIL, DEFAULT_PM_PASSWORD)
    assert pm is not None
    assert pm.email == DEFAULT_PM_EMAIL


def test_seed_pm_is_idempotent() -> None:
    seed_default_platform_manager()
    seed_default_platform_manager()
    assert _account_count() == 1


def test_seed_all_four_roles_creates_four_accounts() -> None:
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()
    assert _account_count() == 4


def test_seed_does_not_overwrite_existing_account_with_same_role() -> None:
    """Negative path: someone already has a real fundraiser account
    under a different email. The seed must still insert its own role
    account (matched by email, not role) without clobbering the existing
    one."""
    profile = UserProfile.create_profile(
        role="fundraiser", description="real"
    )
    UserAccount.create_account(
        email="real-fundraiser@x.com", password="real-pwd", name="Real",
        dob=date(1990, 1, 1), phone_num="1",
        profile_id=profile.profile_id,
    )

    seed_default_fundraiser()

    assert _account_count() == 2
    assert UserAccount.login("real-fundraiser@x.com", "real-pwd") is not None
    assert UserAccount.login(
        DEFAULT_FUNDRAISER_EMAIL, DEFAULT_FUNDRAISER_PASSWORD
    ) is not None


def test_seed_demo_donations_creates_three_rows_on_empty_db() -> None:
    seed_demo_donations()
    with get_connection() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM donation").fetchone()["n"]
    assert n == 3


def test_seed_demo_donations_is_idempotent() -> None:
    seed_demo_donations()
    seed_demo_donations()
    seed_demo_donations()
    with get_connection() as conn:
        n = conn.execute("SELECT COUNT(*) AS n FROM donation").fetchone()["n"]
    assert n == 3


def test_seed_demo_donations_visible_via_search_for_default_donee() -> None:
    seed_demo_donations()
    donee = UserAccount.login(DEFAULT_DONEE_EMAIL, DEFAULT_DONEE_PASSWORD)
    assert donee is not None
    results = Donation.search_my_donation_history(
        account_id=donee.account_id, search_criteria="hospital"
    )
    assert len(results) == 3
