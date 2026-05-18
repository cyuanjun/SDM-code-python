"""Tests for data/seed.py — every seeded role account must be idempotent
and reachable via the login flow."""
from __future__ import annotations

from datetime import date

from data.seed import (
    BULK_ACTIVITY_COUNT,
    BULK_ADMIN_COUNT,
    BULK_CATEGORY_COUNT,
    BULK_DONATION_COUNT,
    BULK_DONEE_COUNT,
    BULK_FAVOURITE_COUNT,
    BULK_FUNDRAISER_COUNT,
    BULK_PM_COUNT,
    BULK_REPORT_COUNT,
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_DONEE_EMAIL,
    DEFAULT_DONEE_PASSWORD,
    DEFAULT_FUNDRAISER_EMAIL,
    DEFAULT_FUNDRAISER_PASSWORD,
    DEFAULT_PASSWORD,
    DEFAULT_PM_EMAIL,
    DEFAULT_PM_PASSWORD,
    TC_ACTIVITY_COUNT,
    TC_ADMIN_COUNT,
    TC_ADMIN_EMAIL,
    TC_CATEGORY_COUNT,
    TC_DONATION_COUNT,
    TC_DONEE_COUNT,
    TC_DONEE_EMAIL,
    TC_FAVOURITE_COUNT,
    TC_FUNDRAISER_COUNT,
    TC_FUNDRAISER_EMAIL,
    TC_PM_COUNT,
    TC_PM_EMAIL,
    TC_REPORT_COUNT,
    seed_bulk_accounts,
    seed_bulk_activities,
    seed_bulk_all,
    seed_bulk_categories,
    seed_bulk_donations,
    seed_bulk_favourites,
    seed_bulk_reports,
    seed_default_admin,
    seed_default_donee,
    seed_default_fundraiser,
    seed_default_platform_manager,
    seed_demo_donations,
    seed_tc_scenario,
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
        dob=date(1990, 1, 1), phone_num="0400000132",
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


# ----- bulk seed (100 / 100 / 100 / 100) ------------------------------------


def _count_role(role: str) -> int:
    with get_connection() as conn:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM user_account a "
            "JOIN user_profile p ON p.profile_id = a.profile_id "
            "WHERE p.role = ?",
            (role,),
        ).fetchone()["n"]


def _count_table(table: str) -> int:
    with get_connection() as conn:
        return conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]


def test_seed_bulk_accounts_fills_to_role_distribution() -> None:
    """seed_bulk_accounts reserves the trailing TC slots — fills to
    1 admin / 24 fundraisers / 68 donees / 3 PMs = 96 total. The
    remaining 4 slots (1 per role) are filled by seed_tc_scenario at
    the end of seed_bulk_all."""
    seed_bulk_accounts()
    assert _count_role("admin") == BULK_ADMIN_COUNT - TC_ADMIN_COUNT
    assert _count_role("fundraiser") == BULK_FUNDRAISER_COUNT - TC_FUNDRAISER_COUNT
    assert _count_role("donee") == BULK_DONEE_COUNT - TC_DONEE_COUNT
    assert _count_role("platform_manager") == BULK_PM_COUNT - TC_PM_COUNT
    assert _count_table("user_account") == 96


def test_seed_bulk_accounts_is_idempotent() -> None:
    """Negative path: a second run must not push counts past the bulk
    fill target (96 — the 4 TC slots are still unfilled)."""
    seed_bulk_accounts()
    seed_bulk_accounts()
    seed_bulk_accounts()
    assert _count_table("user_account") == 96


def test_seed_bulk_accounts_preserves_default_credentials() -> None:
    """Default a001/fr001/d001/pm001 stay reachable via login after bulk seed."""
    seed_bulk_accounts()
    assert UserAccount.login(DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD) is not None
    assert UserAccount.login(DEFAULT_FUNDRAISER_EMAIL, DEFAULT_FUNDRAISER_PASSWORD) is not None
    assert UserAccount.login(DEFAULT_DONEE_EMAIL, DEFAULT_DONEE_PASSWORD) is not None
    assert UserAccount.login(DEFAULT_PM_EMAIL, DEFAULT_PM_PASSWORD) is not None


def test_seed_bulk_accounts_produces_globally_unique_phones() -> None:
    """Negative path of the 2026-05-18 phone-UNIQUE constraint: bulk seed
    must produce distinct phone numbers (not just unique-per-role) across
    the 96 bulk-fill accounts."""
    seed_bulk_accounts()
    with get_connection() as conn:
        rows = conn.execute("SELECT phone_num FROM user_account").fetchall()
    phones = [r["phone_num"] for r in rows]
    assert len(phones) == 96
    assert len(set(phones)) == 96


def test_seed_bulk_categories_fills_to_reserved_target() -> None:
    """Reserves TC_CATEGORY_COUNT trailing slots — bulk fills to 97."""
    seed_bulk_categories()
    assert _count_table("fundraising_activity_category") == (
        BULK_CATEGORY_COUNT - TC_CATEGORY_COUNT
    )


def test_seed_bulk_categories_is_idempotent() -> None:
    seed_bulk_categories()
    seed_bulk_categories()
    assert _count_table("fundraising_activity_category") == (
        BULK_CATEGORY_COUNT - TC_CATEGORY_COUNT
    )


def test_seed_bulk_activities_fills_to_reserved_target() -> None:
    """Reserves TC_ACTIVITY_COUNT trailing slots — bulk fills to 97."""
    seed_bulk_activities()
    assert _count_table("fundraising_activity") == (
        BULK_ACTIVITY_COUNT - TC_ACTIVITY_COUNT
    )


def test_seed_bulk_activities_is_idempotent() -> None:
    seed_bulk_activities()
    seed_bulk_activities()
    assert _count_table("fundraising_activity") == (
        BULK_ACTIVITY_COUNT - TC_ACTIVITY_COUNT
    )


def test_seed_bulk_activities_spreads_across_fundraisers() -> None:
    """Round-robin assignment: every fundraiser owns ≥ 1 activity, no
    single fundraiser owns more than ceil(97/24) = 5 activities."""
    seed_bulk_activities()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT owner_account_id, COUNT(*) AS n FROM fundraising_activity "
            "GROUP BY owner_account_id"
        ).fetchall()
    counts = [r["n"] for r in rows]
    assert min(counts) >= 1
    assert max(counts) <= 5


def test_seed_bulk_donations_fills_to_reserved_target() -> None:
    """Reserves TC_DONATION_COUNT trailing slots — bulk fills to 98."""
    seed_bulk_donations()
    assert _count_table("donation") == (
        BULK_DONATION_COUNT - TC_DONATION_COUNT
    )


def test_seed_bulk_donations_is_idempotent() -> None:
    seed_bulk_donations()
    seed_bulk_donations()
    assert _count_table("donation") == (
        BULK_DONATION_COUNT - TC_DONATION_COUNT
    )


def test_seed_bulk_favourites_fills_to_reserved_target() -> None:
    """Reserves TC_FAVOURITE_COUNT trailing slot — bulk fills to 99."""
    seed_bulk_favourites()
    assert _count_table("favourite") == (
        BULK_FAVOURITE_COUNT - TC_FAVOURITE_COUNT
    )


def test_seed_bulk_favourites_is_idempotent() -> None:
    seed_bulk_favourites()
    seed_bulk_favourites()
    assert _count_table("favourite") == (
        BULK_FAVOURITE_COUNT - TC_FAVOURITE_COUNT
    )


def test_seed_bulk_favourites_pairs_are_unique() -> None:
    """Negative path of the composite PK (account_id, fra_id): every
    seeded favourite must be a distinct pair, even though donees cycle."""
    seed_bulk_favourites()
    expected = BULK_FAVOURITE_COUNT - TC_FAVOURITE_COUNT
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT account_id, fra_id FROM favourite"
        ).fetchall()
    pairs = [(r["account_id"], r["fra_id"]) for r in rows]
    assert len(pairs) == expected
    assert len(set(pairs)) == expected


def test_seed_bulk_reports_fills_to_reserved_target() -> None:
    """Reserves TC_REPORT_COUNT trailing slot — bulk fills to 99."""
    seed_bulk_reports()
    assert _count_table("report") == (BULK_REPORT_COUNT - TC_REPORT_COUNT)


def test_seed_bulk_reports_is_idempotent() -> None:
    seed_bulk_reports()
    seed_bulk_reports()
    assert _count_table("report") == (BULK_REPORT_COUNT - TC_REPORT_COUNT)


def test_seed_bulk_reports_covers_all_three_types() -> None:
    """The bulk reports cycle through daily/weekly/monthly — each
    report_type must appear at least once so US-41/42/43 demos have
    data to show."""
    seed_bulk_reports()
    expected = BULK_REPORT_COUNT - TC_REPORT_COUNT
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT report_type, COUNT(*) AS n FROM report "
            "GROUP BY report_type"
        ).fetchall()
    by_type = {r["report_type"]: r["n"] for r in rows}
    assert by_type.get("daily", 0) >= 1
    assert by_type.get("weekly", 0) >= 1
    assert by_type.get("monthly", 0) >= 1
    assert sum(by_type.values()) == expected


# ----- TC scenario (curated rows backing docs/test_cases.md) ----------------


def test_seed_tc_scenario_creates_named_rows() -> None:
    """Every TC row is prefixed `TC - ` so it's discoverable in the
    Manage / Browse pages. Verifies the canonical scenario shape:
    4 TC accounts, 3 categories, 3 activities, 2 donations, 1 favourite,
    1 report."""
    seed_tc_scenario()
    with get_connection() as conn:
        accs = [r["name"] for r in conn.execute(
            "SELECT name FROM user_account WHERE name LIKE 'TC - %' "
            "ORDER BY name"
        ).fetchall()]
        cats = [r["category_name"] for r in conn.execute(
            "SELECT category_name FROM fundraising_activity_category "
            "WHERE category_name LIKE 'TC - %' ORDER BY category_name"
        ).fetchall()]
        acts = [r["title"] for r in conn.execute(
            "SELECT title FROM fundraising_activity "
            "WHERE title LIKE 'TC - %' ORDER BY title"
        ).fetchall()]
    assert accs == [
        "TC - Admin",
        "TC - Donee",
        "TC - Fundraiser",
        "TC - Platform Manager",
    ]
    assert cats == ["TC - Education", "TC - Health", "TC - Sports"]
    assert acts == [
        "TC - Active hospital fund",
        "TC - Completed school fund",
        "TC - Suspended sports fund",
    ]
    assert _count_table("donation") == 2
    assert _count_table("favourite") == 1
    assert _count_table("report") == 1


def test_seed_tc_scenario_accounts_are_login_reachable() -> None:
    """The 4 TC accounts must be reachable via login with password '123'
    — they back actor-driven TCs like 'login as admin/fundraiser/...'."""
    seed_tc_scenario()
    assert UserAccount.login(TC_ADMIN_EMAIL, DEFAULT_PASSWORD) is not None
    assert UserAccount.login(TC_FUNDRAISER_EMAIL, DEFAULT_PASSWORD) is not None
    assert UserAccount.login(TC_DONEE_EMAIL, DEFAULT_PASSWORD) is not None
    assert UserAccount.login(TC_PM_EMAIL, DEFAULT_PASSWORD) is not None


def test_seed_tc_scenario_links_ownership_to_tc_accounts() -> None:
    """TC activities are owned by TC - Fundraiser; TC donations + the
    favourite are made by TC - Donee; the report is owned by TC - PM.
    Guards against an accidental re-wire back to fr001/d001/pm001."""
    seed_tc_scenario()
    tc_fr = UserAccount.login(TC_FUNDRAISER_EMAIL, DEFAULT_PASSWORD)
    tc_d = UserAccount.login(TC_DONEE_EMAIL, DEFAULT_PASSWORD)
    tc_pm = UserAccount.login(TC_PM_EMAIL, DEFAULT_PASSWORD)
    assert tc_fr and tc_d and tc_pm
    with get_connection() as conn:
        act_owners = {r["owner_account_id"] for r in conn.execute(
            "SELECT owner_account_id FROM fundraising_activity "
            "WHERE title LIKE 'TC - %'"
        ).fetchall()}
        don_owners = {r["account_id"] for r in conn.execute(
            "SELECT account_id FROM donation"
        ).fetchall()}
        fav_owners = {r["account_id"] for r in conn.execute(
            "SELECT account_id FROM favourite"
        ).fetchall()}
        rep_owners = {r["platform_manager_id"] for r in conn.execute(
            "SELECT platform_manager_id FROM report"
        ).fetchall()}
    assert act_owners == {tc_fr.account_id}
    assert don_owners == {tc_d.account_id}
    assert fav_owners == {tc_d.account_id}
    assert rep_owners == {tc_pm.account_id}


def test_seed_tc_scenario_is_idempotent() -> None:
    """Negative path: second run is a no-op (would otherwise collide on
    the UNIQUE category_name constraint and crash)."""
    seed_tc_scenario()
    seed_tc_scenario()
    seed_tc_scenario()
    with get_connection() as conn:
        n_cats = conn.execute(
            "SELECT COUNT(*) AS n FROM fundraising_activity_category "
            "WHERE category_name LIKE 'TC - %'"
        ).fetchone()["n"]
        n_acts = conn.execute(
            "SELECT COUNT(*) AS n FROM fundraising_activity "
            "WHERE title LIKE 'TC - %'"
        ).fetchone()["n"]
    assert n_cats == 3
    assert n_acts == 3
    assert _count_table("donation") == 2
    assert _count_table("favourite") == 1
    assert _count_table("report") == 1


def test_seed_tc_scenario_marks_completed_activity() -> None:
    """`TC - Completed school fund` has end_date in 2025 → `completed` is
    stored as 1 at write-time (derive+store flow)."""
    seed_tc_scenario()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT completed FROM fundraising_activity "
            "WHERE title = 'TC - Completed school fund'"
        ).fetchone()
    assert row is not None
    assert row["completed"] == 1


def test_seed_tc_scenario_marks_suspended_rows() -> None:
    """`TC - Sports` category and `TC - Suspended sports fund` activity
    are both flagged suspended=1 so negative-path TCs have data."""
    seed_tc_scenario()
    with get_connection() as conn:
        cat = conn.execute(
            "SELECT suspended FROM fundraising_activity_category "
            "WHERE category_name = 'TC - Sports'"
        ).fetchone()
        act = conn.execute(
            "SELECT suspended FROM fundraising_activity "
            "WHERE title = 'TC - Suspended sports fund'"
        ).fetchone()
    assert cat is not None and cat["suspended"] == 1
    assert act is not None and act["suspended"] == 1


def test_seed_tc_scenario_links_donations_to_correct_activities() -> None:
    """The two TC donations target the active + completed activities by
    name — guards against an accidental swap in the seed."""
    seed_tc_scenario()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT a.title, d.amount FROM donation d "
            "JOIN fundraising_activity a ON a.fra_id = d.fra_id "
            "ORDER BY a.title"
        ).fetchall()
    by_title = {r["title"]: r["amount"] for r in rows}
    assert by_title == {
        "TC - Active hospital fund": "100.00",
        "TC - Completed school fund": "200.00",
    }


def test_seed_tc_scenario_runs_inside_seed_bulk_all_without_breaking_totals() -> None:
    """seed_bulk_all now calls seed_tc_scenario between demo + bulk fills.
    Final counts must still hit 100 per scalable table — bulk top-ups
    absorb the TC rows."""
    seed_bulk_all()
    assert _count_table("user_account") == 100
    assert _count_table("fundraising_activity_category") == BULK_CATEGORY_COUNT
    assert _count_table("fundraising_activity") == BULK_ACTIVITY_COUNT
    assert _count_table("donation") == BULK_DONATION_COUNT
    assert _count_table("favourite") == BULK_FAVOURITE_COUNT
    assert _count_table("report") == BULK_REPORT_COUNT
    # And the canonical TC row still exists alongside the bulk fill.
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM fundraising_activity "
            "WHERE title = 'TC - Active hospital fund'"
        ).fetchone()
    assert row is not None


def test_seed_bulk_all_brings_every_table_to_100() -> None:
    """Top-level bulk seed entry point — fresh DB → all six scalable
    tables at 100 rows."""
    seed_bulk_all()
    assert _count_table("user_account") == 100
    assert _count_table("fundraising_activity_category") == BULK_CATEGORY_COUNT
    assert _count_table("fundraising_activity") == BULK_ACTIVITY_COUNT
    assert _count_table("donation") == BULK_DONATION_COUNT
    assert _count_table("favourite") == BULK_FAVOURITE_COUNT
    assert _count_table("report") == BULK_REPORT_COUNT


def test_seed_bulk_all_is_idempotent() -> None:
    seed_bulk_all()
    seed_bulk_all()
    assert _count_table("user_account") == 100
    assert _count_table("fundraising_activity_category") == BULK_CATEGORY_COUNT
    assert _count_table("fundraising_activity") == BULK_ACTIVITY_COUNT
    assert _count_table("donation") == BULK_DONATION_COUNT
    assert _count_table("favourite") == BULK_FAVOURITE_COUNT
    assert _count_table("report") == BULK_REPORT_COUNT
