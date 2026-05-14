"""Tests for data/seed.py — bootstrap admin must be idempotent and reachable
via the login flow."""
from __future__ import annotations

from data.seed import (
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_PM_EMAIL,
    DEFAULT_PM_PASSWORD,
    seed_default_admin,
    seed_default_platform_manager,
    seed_demo_donations,
)
from entity.donation import Donation
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_seed_creates_default_admin_on_empty_db() -> None:
    seed_default_admin()

    admin = UserAccount.login(DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD)

    assert admin is not None
    assert admin.email == DEFAULT_ADMIN_EMAIL
    assert admin.profile_id == "prof_001"


def test_seed_creates_admin_profile_too() -> None:
    seed_default_admin()

    profiles = UserProfile.view_all_profiles()

    assert len(profiles) == 1
    assert profiles[0].role == "admin"


def test_seed_is_idempotent() -> None:
    """Negative path: running the seed twice must not create duplicate
    admin profiles or accounts."""
    seed_default_admin()
    seed_default_admin()
    seed_default_admin()

    profiles = UserProfile.view_all_profiles()
    assert len(profiles) == 1

    with __import__("persistence.db", fromlist=["get_connection"]).get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS n FROM user_account").fetchone()["n"]
    assert count == 1


def test_seed_reuses_existing_admin_profile_when_present() -> None:
    """Negative path: if an admin profile already exists (e.g. created
    manually by a previous user) the seed must not create a second one."""
    existing = UserProfile.create_profile(
        role="admin", description="manually created"
    )

    seed_default_admin()

    profiles = UserProfile.view_all_profiles()
    assert len(profiles) == 1
    assert profiles[0].profile_id == existing.profile_id


def test_seed_does_not_run_when_admin_account_already_exists() -> None:
    """Negative path: an admin account already exists (created by a real
    person, not the seed); seed must not create a duplicate."""
    profile = UserProfile.create_profile(role="admin", description="real admin")
    UserAccount.create_account(
        email="real@example.com", password="real-password", name="Real",
        dob=__import__("datetime").date(1990, 1, 1), phone_num="1",
        profile_id=profile.profile_id,
    )

    seed_default_admin()

    with __import__("persistence.db", fromlist=["get_connection"]).get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS n FROM user_account").fetchone()["n"]
    assert count == 1
    # The default admin's email was never inserted.
    assert UserAccount.login(DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD) is None


def test_seed_demo_donations_creates_donations_on_empty_db() -> None:
    seed_demo_donations()

    with __import__("persistence.db", fromlist=["get_connection"]).get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS n FROM donation").fetchone()["n"]
    assert count > 0


def test_seed_demo_donations_is_idempotent() -> None:
    """Negative path: running the donations seed twice doesn't add more rows."""
    seed_demo_donations()
    seed_demo_donations()
    seed_demo_donations()

    with __import__("persistence.db", fromlist=["get_connection"]).get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) AS n FROM donation").fetchone()["n"]
    # Same count as a single seed run.
    assert count == 3


def test_seed_demo_donations_visible_via_search_for_seeded_donee() -> None:
    """Seeded donations should be reachable through the US-32 search path
    for the demo donee."""
    seed_demo_donations()

    # The seeded demo donee should now exist; fetch it via login.
    donee = UserAccount.login("demo-donee@example.com", "demo")
    assert donee is not None

    results = Donation.search_donation_history(
        search_criteria="hospital", account_id=donee.account_id
    )
    assert len(results) == 3


def test_seed_default_pm_creates_pm_on_empty_db() -> None:
    seed_default_platform_manager()
    pm = UserAccount.login(DEFAULT_PM_EMAIL, DEFAULT_PM_PASSWORD)
    assert pm is not None
    assert pm.email == DEFAULT_PM_EMAIL


def test_seed_default_pm_is_idempotent() -> None:
    """Negative path: running the PM seed twice doesn't create duplicates."""
    seed_default_platform_manager()
    seed_default_platform_manager()
    seed_default_platform_manager()

    pms = [p for p in UserProfile.view_all_profiles() if p.role == "platform_manager"]
    assert len(pms) == 1
