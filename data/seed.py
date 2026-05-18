"""Seed data — idempotent bootstrap for the demo.

Solves the chicken-and-egg admin problem: the US-1 / US-6 diagrams imply
the actor is "User admin", but no admin can exist until someone creates
one. Also seeds one default account per role (admin / fundraiser / donee
/ platform_manager) so the demo is reachable without any pre-work, plus
three sample donations so US-32 / US-33 have data to display.

The four `seed_default_*` + `seed_demo_donations` functions are the
minimum-viable seed. On top of that, four `seed_bulk_*` helpers fill
each scalable table up to 100 rows — useful so admin/PM search and
browse-list pages have realistic data to scroll through at demo time.
The split-by-role count for the 100-account target is 1 admin / 25
fundraisers / 70 donees / 4 PMs (profiles are schema-locked at 1 per
role by the role UNIQUE constraint).

Idempotent — every helper checks before creating, and the bulk
helpers top-up rather than re-create.

Default credentials (short role prefix + 001 = the first seeded account
for that role; the bulk seed adds fr002..fr025, d002..d070, pm002..pm004):
    a001@a.com    / 123   (admin)
    fr001@a.com   / 123   (fundraiser)
    d001@a.com    / 123   (donee)
    pm001@a.com   / 123   (platform manager)
"""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from entity.donation import Donation
from entity.fundraising_activity import FundraisingActivity
from entity.fundraising_activity_category import FundraisingActivityCategory
from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from persistence.db import get_connection

DEFAULT_PASSWORD = "123"

DEFAULT_ADMIN_EMAIL = "a001@a.com"
DEFAULT_ADMIN_PASSWORD = DEFAULT_PASSWORD
DEFAULT_FUNDRAISER_EMAIL = "fr001@a.com"
DEFAULT_FUNDRAISER_PASSWORD = DEFAULT_PASSWORD
DEFAULT_DONEE_EMAIL = "d001@a.com"
DEFAULT_DONEE_PASSWORD = DEFAULT_PASSWORD
DEFAULT_PM_EMAIL = "pm001@a.com"
DEFAULT_PM_PASSWORD = DEFAULT_PASSWORD

# Bulk seed targets (post-bulk-seed totals).
BULK_FUNDRAISER_COUNT = 25      # fr001..fr025
BULK_DONEE_COUNT = 70           # d001..d070
BULK_PM_COUNT = 4               # pm001..pm004
BULK_CATEGORY_COUNT = 100       # cat_001..cat_100
BULK_ACTIVITY_COUNT = 100       # fra_001..fra_100
BULK_DONATION_COUNT = 100       # don_001..don_100

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
        return row["profile_id"]
    return UserProfile.create_profile(
        role=role, description=description
    ).profile_id


def _any_donation_exists() -> bool:
    with get_connection() as conn:
        row = conn.execute("SELECT 1 FROM donation LIMIT 1").fetchone()
    return row is not None


def _ensure_demo_category() -> str:
    """Idempotent: return the fra_cat_id of a 'Health' category, creating
    it if missing. Activity creation now requires an existing category id
    (per the 2026-05-18 US-13 attribute change)."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT fra_cat_id FROM fundraising_activity_category "
            "WHERE category_name = 'Health' LIMIT 1"
        ).fetchone()
    if row is not None:
        return row["fra_cat_id"]
    category = FundraisingActivityCategory.create_category(
        category_name="Health",
        description="Medical / healthcare campaigns (demo seed)",
    )
    assert category is not None
    return category.fra_cat_id


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
        activity = FundraisingActivity.view_fundraising_activity(row["fra_id"])
        assert activity is not None
        return activity

    fundraiser = UserAccount.login(
        DEFAULT_FUNDRAISER_EMAIL, DEFAULT_FUNDRAISER_PASSWORD
    )
    assert fundraiser is not None, (
        "default fundraiser must exist before seeding demo activity"
    )
    fra_cat_id = _ensure_demo_category()
    return FundraisingActivity.create_fundraising_activity(
        title="Demo hospital fund",
        description="Demo donations seeded for US-32/US-33",
        target_amount=Decimal("1000.00"),
        fra_cat_id=fra_cat_id,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 12, 31),
        owner_account_id=fundraiser.account_id,
    )


# ----------------------------------------------------------------------------
# bulk seed (100-row top-up per scalable table)
# ----------------------------------------------------------------------------


def seed_bulk_accounts() -> None:
    """Top up the user_account table to 100 rows: 1 admin / 25 fundraisers /
    70 donees / 4 PMs. The 4 default seeded accounts (a001/fr001/d001/pm001)
    are kept as-is; this helper only adds the missing accounts to reach the
    target counts. Idempotent — re-runs do nothing once the targets are met.

    Email pattern: `{prefix}{NNN}@a.com` (fr002@a.com, d042@a.com, …).
    Names: `Fundraiser 002`, `Donee 042`, etc.
    """
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()

    fr_profile = _profile_id_for_role("fundraiser")
    donee_profile = _profile_id_for_role("donee")
    pm_profile = _profile_id_for_role("platform_manager")

    _fill_role_accounts(
        prefix="fr",
        target=BULK_FUNDRAISER_COUNT,
        role_label="Fundraiser",
        profile_id=fr_profile,
    )
    _fill_role_accounts(
        prefix="d",
        target=BULK_DONEE_COUNT,
        role_label="Donee",
        profile_id=donee_profile,
    )
    _fill_role_accounts(
        prefix="pm",
        target=BULK_PM_COUNT,
        role_label="PM",
        profile_id=pm_profile,
    )


def seed_bulk_categories() -> None:
    """Top up the fundraising_activity_category table to 100 rows. The
    existing demo `Health` category is kept (cat_001); this helper adds
    `Category 002`..`Category 100` until the total reaches 100. Idempotent."""
    _ensure_demo_category()
    n = _count("fundraising_activity_category")
    for i in range(n + 1, BULK_CATEGORY_COUNT + 1):
        name = f"Category {i:03d}"
        if FundraisingActivityCategory.create_category(
            category_name=name,
            description=f"Demo category #{i} (seeded for browse/search demos)",
        ) is None:
            # Duplicate name shouldn't happen on a fresh top-up, but
            # silently skip if it does.
            continue


def seed_bulk_activities() -> None:
    """Top up the fundraising_activity table to 100 rows. Activities are
    spread round-robin across the 25 seeded fundraisers, each pointing at a
    different category (round-robin against the 100-category list). Dates
    mix past + future so US-30/31 (completed view) and the browse list both
    have realistic data:

    - every 3rd activity ends in 2025 (past) → derived `completed=True`
    - the rest end in 2099 (future) → ongoing

    Idempotent.
    """
    seed_bulk_accounts()
    seed_bulk_categories()

    fundraiser_ids = _account_ids_for_role("fundraiser")
    category_ids = _all_category_ids()
    if not fundraiser_ids or not category_ids:
        return

    n = _count("fundraising_activity")
    for i in range(n + 1, BULK_ACTIVITY_COUNT + 1):
        title = f"Activity {i:03d}"
        owner = fundraiser_ids[(i - 1) % len(fundraiser_ids)]
        category = category_ids[(i - 1) % len(category_ids)]
        # 1-in-3 cadence for past end-dates so US-30/31 has a meaningful pool.
        if i % 3 == 0:
            start_date = date(2025, 1, 1) + timedelta(days=(i % 30))
            end_date = date(2025, 6, 1) + timedelta(days=(i % 30))
        else:
            start_date = date(2099, 1, 1) + timedelta(days=(i % 30))
            end_date = date(2099, 12, 1) + timedelta(days=(i % 30))
        FundraisingActivity.create_fundraising_activity(
            title=title,
            description=f"Demo fundraising activity #{i}.",
            target_amount=Decimal("1000.00") + Decimal(i * 10),
            fra_cat_id=category,
            start_date=start_date,
            end_date=end_date,
            owner_account_id=owner,
        )


def seed_bulk_donations() -> None:
    """Top up the donation table to 100 rows. Each donation is round-robin
    across the 70 donees × 100 activities, with deterministic amounts and
    dates so the seed is reproducible. Idempotent."""
    seed_bulk_activities()

    donee_ids = _account_ids_for_role("donee")
    activity_ids = _all_activity_ids()
    if not donee_ids or not activity_ids:
        return

    n = _count("donation")
    for i in range(n + 1, BULK_DONATION_COUNT + 1):
        donee = donee_ids[(i - 1) % len(donee_ids)]
        activity = activity_ids[(i - 1) % len(activity_ids)]
        amount = Decimal("5.00") + Decimal((i * 7) % 500)
        donation_date = date(2026, 1, 1) + timedelta(days=(i % 120))
        Donation.create_donation(
            account_id=donee,
            fra_id=activity,
            amount=amount,
            donation_date=donation_date,
        )


def seed_bulk_all() -> None:
    """Run every bulk helper in the right order. Idempotent.

    Order matters: `seed_demo_donations` creates the "Demo hospital fund"
    activity + its 3 donations *before* `seed_bulk_activities` tops up to
    100 — so the demo activity becomes fra_001 and bulk fills fra_002..
    fra_100. Without this ordering, bulk would create 100 activities, then
    seed_demo_donations would create a 101st (overshooting the target).
    """
    seed_bulk_accounts()
    seed_bulk_categories()
    seed_demo_donations()      # 1 activity + 3 donations
    seed_bulk_activities()     # tops up to 100 activities (creates 99 more)
    seed_bulk_donations()      # tops up to 100 donations (creates 97 more)


# ----------------------------------------------------------------------------
# bulk helpers
# ----------------------------------------------------------------------------


def _count(table: str) -> int:
    with get_connection() as conn:
        return conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]


def _profile_id_for_role(role: str) -> str:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT profile_id FROM user_profile WHERE role = ? LIMIT 1",
            (role,),
        ).fetchone()
    assert row is not None, f"profile for role {role!r} must already exist"
    return row["profile_id"]


def _account_ids_for_role(role: str) -> list[str]:
    profile_id = _profile_id_for_role(role)
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT account_id FROM user_account WHERE profile_id = ? "
            "ORDER BY account_id",
            (profile_id,),
        ).fetchall()
    return [row["account_id"] for row in rows]


def _all_category_ids() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT fra_cat_id FROM fundraising_activity_category "
            "ORDER BY fra_cat_id"
        ).fetchall()
    return [row["fra_cat_id"] for row in rows]


def _all_activity_ids() -> list[str]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT fra_id FROM fundraising_activity ORDER BY fra_id"
        ).fetchall()
    return [row["fra_id"] for row in rows]


def _fill_role_accounts(
    *, prefix: str, target: int, role_label: str, profile_id: str
) -> None:
    """Create the missing accounts for one role to reach `target` total
    accounts of that role. Emails follow `{prefix}{NNN}@a.com`, names
    follow `{role_label} NNN`. Phone numbers are sourced from the
    next-globally-unique pool (`phone_num` is UNIQUE on the schema, so
    every account across all roles must have a distinct number).
    Idempotent — skips rows that already exist."""
    existing = _account_ids_for_role(_role_from_prefix(prefix))
    n = len(existing)
    for i in range(n + 1, target + 1):
        email = f"{prefix}{i:03d}@a.com"
        if _account_with_email_exists(email):
            continue
        UserAccount.create_account(
            email=email,
            password=DEFAULT_PASSWORD,
            name=f"{role_label} {i:03d}",
            dob=_DEFAULT_DOB,
            phone_num=_next_unique_phone(),
            profile_id=profile_id,
        )


def _next_unique_phone() -> str:
    """Return the next 10-digit phone number not yet used on any account.
    Walks from 0000000000 upward — cheap because the total account count
    is bounded (100). The four default-seeded accounts already occupy
    0000000000..0000000003, so this typically returns 0000000004 on the
    first bulk fill and increases from there."""
    with get_connection() as conn:
        used = {
            row["phone_num"]
            for row in conn.execute(
                "SELECT phone_num FROM user_account"
            ).fetchall()
        }
    i = 0
    while True:
        candidate = f"{i:010d}"
        if candidate not in used:
            return candidate
        i += 1


def _role_from_prefix(prefix: str) -> str:
    return {"fr": "fundraiser", "d": "donee", "pm": "platform_manager"}[prefix]


if __name__ == "__main__":
    # `python -m data.seed` — initialise the schema then run every seed
    # function. Safe to run repeatedly (idempotent). Pair with `rm app.db`
    # if you want a fully fresh DB.
    from persistence.db import init_db

    init_db()
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()
    seed_demo_donations()
    seed_bulk_all()
    print("Seed complete.")
    print(f"  admin   : {DEFAULT_ADMIN_EMAIL} / {DEFAULT_ADMIN_PASSWORD}")
    print(f"  funder  : {DEFAULT_FUNDRAISER_EMAIL} / {DEFAULT_FUNDRAISER_PASSWORD}")
    print(f"  donee   : {DEFAULT_DONEE_EMAIL} / {DEFAULT_DONEE_PASSWORD}")
    print(f"  PM      : {DEFAULT_PM_EMAIL} / {DEFAULT_PM_PASSWORD}")
    print(
        f"  bulk    : {_count('user_account')} accounts, "
        f"{_count('fundraising_activity_category')} categories, "
        f"{_count('fundraising_activity')} activities, "
        f"{_count('donation')} donations"
    )
