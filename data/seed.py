"""Seed data — idempotent bootstrap for the demo.

Default credentials:
    a001@a.com    / 123   (admin)
    fr001@a.com   / 123   (fundraiser)
    d001@a.com    / 123   (donee)
    pm001@a.com   / 123   (platform manager)
"""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from calendar import monthrange

from entity.donation import Donation
from entity.favourite import Favourite
from entity.fundraising_activity import FundraisingActivity
from entity.fundraising_activity_category import FundraisingActivityCategory
from entity.report import Report
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

TC_ADMIN_EMAIL = "tc-admin@a.com"
TC_FUNDRAISER_EMAIL = "tc-fr@a.com"
TC_DONEE_EMAIL = "tc-d@a.com"
TC_PM_EMAIL = "tc-pm@a.com"
TC_ADMIN_PHONE = "0099999900"
TC_FUNDRAISER_PHONE = "0099999901"
TC_DONEE_PHONE = "0099999902"
TC_PM_PHONE = "0099999903"

BULK_ADMIN_COUNT = 2
BULK_FUNDRAISER_COUNT = 25
BULK_DONEE_COUNT = 69
BULK_PM_COUNT = 4
BULK_CATEGORY_COUNT = 100
BULK_ACTIVITY_COUNT = 100
BULK_DONATION_COUNT = 100
BULK_FAVOURITE_COUNT = 100
BULK_REPORT_COUNT = 100

TC_ADMIN_COUNT = 1
TC_FUNDRAISER_COUNT = 1
TC_DONEE_COUNT = 1
TC_PM_COUNT = 1
TC_CATEGORY_COUNT = 3
TC_ACTIVITY_COUNT = 3
TC_DONATION_COUNT = 2
TC_FAVOURITE_COUNT = 1
TC_REPORT_COUNT = 1

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
    if _any_donation_exists():
        return
    seed_default_fundraiser()
    seed_default_donee()
    donee = UserAccount.login(DEFAULT_DONEE_EMAIL, DEFAULT_DONEE_PASSWORD)
    assert donee is not None

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


def seed_tc_scenario() -> None:
    if _tc_scenario_already_seeded():
        return
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()

    _ensure_tc_account(
        email=TC_ADMIN_EMAIL,
        name="TC - Admin",
        phone_num=TC_ADMIN_PHONE,
        role="admin",
    )
    _ensure_tc_account(
        email=TC_FUNDRAISER_EMAIL,
        name="TC - Fundraiser",
        phone_num=TC_FUNDRAISER_PHONE,
        role="fundraiser",
    )
    _ensure_tc_account(
        email=TC_DONEE_EMAIL,
        name="TC - Donee",
        phone_num=TC_DONEE_PHONE,
        role="donee",
    )
    _ensure_tc_account(
        email=TC_PM_EMAIL,
        name="TC - Platform Manager",
        phone_num=TC_PM_PHONE,
        role="platform_manager",
    )

    fundraiser = UserAccount.login(TC_FUNDRAISER_EMAIL, DEFAULT_PASSWORD)
    donee = UserAccount.login(TC_DONEE_EMAIL, DEFAULT_PASSWORD)
    pm = UserAccount.login(TC_PM_EMAIL, DEFAULT_PASSWORD)
    assert fundraiser and donee and pm

    cat_health = FundraisingActivityCategory.create_category(
        category_name="TC - Health",
        description="TC scenario active category",
    )
    cat_edu = FundraisingActivityCategory.create_category(
        category_name="TC - Education",
        description="TC scenario active category",
    )
    cat_sports = FundraisingActivityCategory.create_category(
        category_name="TC - Sports",
        description="TC scenario suspended category",
    )
    assert cat_health and cat_edu and cat_sports
    FundraisingActivityCategory.suspend_fundraising_activity_category(
        cat_sports.fra_cat_id
    )

    active = FundraisingActivity.create_fundraising_activity(
        title="TC - Active hospital fund",
        description="TC scenario active activity",
        target_amount=Decimal("5000.00"),
        fra_cat_id=cat_health.fra_cat_id,
        start_date=date(2026, 1, 1),
        end_date=date(2027, 12, 31),
        owner_account_id=fundraiser.account_id,
    )
    completed = FundraisingActivity.create_fundraising_activity(
        title="TC - Completed school fund",
        description="TC scenario completed activity",
        target_amount=Decimal("3000.00"),
        fra_cat_id=cat_edu.fra_cat_id,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 12, 31),
        owner_account_id=fundraiser.account_id,
    )
    suspended_act = FundraisingActivity.create_fundraising_activity(
        title="TC - Suspended sports fund",
        description="TC scenario suspended activity",
        target_amount=Decimal("2000.00"),
        fra_cat_id=cat_edu.fra_cat_id,
        start_date=date(2026, 6, 1),
        end_date=date(2027, 6, 1),
        owner_account_id=fundraiser.account_id,
    )
    assert active and completed and suspended_act
    FundraisingActivity.suspend_my_fundraising_activity(
        owner_account_id=fundraiser.account_id, fra_id=suspended_act.fra_id,
    )

    Donation.create_donation(
        account_id=donee.account_id, fra_id=active.fra_id,
        amount=Decimal("100.00"), donation_date=date(2026, 4, 15),
    )
    Donation.create_donation(
        account_id=donee.account_id, fra_id=completed.fra_id,
        amount=Decimal("200.00"), donation_date=date(2025, 9, 10),
    )

    Favourite.save_fundraising_activity(
        account_id=donee.account_id, fra_id=active.fra_id,
    )

    Report.generate_monthly_report(
        start_date=date(2026, 4, 1),
        end_date=date(2026, 4, 30),
        platform_manager_id=pm.account_id,
    )


def _tc_scenario_already_seeded() -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM fundraising_activity "
            "WHERE title = 'TC - Active hospital fund' LIMIT 1"
        ).fetchone()
    return row is not None


def _ensure_tc_account(
    *, email: str, name: str, phone_num: str, role: str
) -> None:
    if _account_with_email_exists(email):
        return
    profile_id = _profile_id_for_role(role)
    UserAccount.create_account(
        email=email,
        password=DEFAULT_PASSWORD,
        name=name,
        dob=_DEFAULT_DOB,
        phone_num=phone_num,
        profile_id=profile_id,
    )


def _ensure_role_account(
    *,
    role: str,
    profile_description: str,
    email: str,
    password: str,
    name: str,
    phone_num: str,
) -> None:
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
    assert fundraiser is not None
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


def seed_bulk_accounts() -> None:
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()

    fr_profile = _profile_id_for_role("fundraiser")
    donee_profile = _profile_id_for_role("donee")
    pm_profile = _profile_id_for_role("platform_manager")

    _fill_role_accounts(
        prefix="fr",
        target=BULK_FUNDRAISER_COUNT - TC_FUNDRAISER_COUNT,
        role_label="Fundraiser",
        profile_id=fr_profile,
    )
    _fill_role_accounts(
        prefix="d",
        target=BULK_DONEE_COUNT - TC_DONEE_COUNT,
        role_label="Donee",
        profile_id=donee_profile,
    )
    _fill_role_accounts(
        prefix="pm",
        target=BULK_PM_COUNT - TC_PM_COUNT,
        role_label="PM",
        profile_id=pm_profile,
    )


def seed_bulk_categories() -> None:
    _ensure_demo_category()
    n = _count("fundraising_activity_category")
    target = BULK_CATEGORY_COUNT - TC_CATEGORY_COUNT
    for i in range(n + 1, target + 1):
        name = f"Category {i:03d}"
        if FundraisingActivityCategory.create_category(
            category_name=name,
            description=f"Demo category #{i}",
        ) is None:
            continue


def seed_bulk_activities() -> None:
    seed_bulk_accounts()
    seed_bulk_categories()

    fundraiser_ids = _account_ids_for_role("fundraiser")
    category_ids = _all_category_ids()
    if not fundraiser_ids or not category_ids:
        return

    n = _count("fundraising_activity")
    target = BULK_ACTIVITY_COUNT - TC_ACTIVITY_COUNT
    for i in range(n + 1, target + 1):
        title = f"Activity {i:03d}"
        owner = fundraiser_ids[(i - 1) % len(fundraiser_ids)]
        category = category_ids[(i - 1) % len(category_ids)]
        if i % 3 == 0:
            start_date = date(2025, 1, 1) + timedelta(days=(i % 30))
            end_date = date(2025, 6, 1) + timedelta(days=(i % 30))
        else:
            start_date = date(2026, 7, 1) + timedelta(days=(i % 60))
            end_date = date(2027, 6, 30) + timedelta(days=(i % 60))
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
    seed_bulk_activities()

    donee_ids = _account_ids_for_role("donee")
    activity_ids = _all_activity_ids()
    if not donee_ids or not activity_ids:
        return

    n = _count("donation")
    target = BULK_DONATION_COUNT - TC_DONATION_COUNT
    for i in range(n + 1, target + 1):
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


def seed_bulk_favourites() -> None:
    seed_bulk_activities()

    donee_ids = _account_ids_for_role("donee")
    activity_ids = _all_activity_ids()
    if not donee_ids or not activity_ids:
        return

    target = BULK_FAVOURITE_COUNT - TC_FAVOURITE_COUNT
    i = 0
    safety = BULK_FAVOURITE_COUNT * 3
    while _count("favourite") < target and safety > 0:
        donee = donee_ids[i % len(donee_ids)]
        activity = activity_ids[i % len(activity_ids)]
        Favourite.save_fundraising_activity(
            account_id=donee, fra_id=activity,
        )
        i += 1
        safety -= 1


def seed_bulk_reports() -> None:
    seed_bulk_donations()

    pm_ids = _account_ids_for_role("platform_manager")
    if not pm_ids:
        return

    n = _count("report")
    target = BULK_REPORT_COUNT - TC_REPORT_COUNT
    for i in range(n + 1, target + 1):
        pm = pm_ids[(i - 1) % len(pm_ids)]
        kind = (i - 1) % 3
        if kind == 0:
            day = date(2026, 1, 1) + timedelta(days=(i % 60))
            Report.generate_daily_report(
                start_date=day, end_date=day, platform_manager_id=pm,
            )
        elif kind == 1:
            monday = date(2026, 1, 5) + timedelta(weeks=(i % 20))
            Report.generate_weekly_report(
                start_date=monday,
                end_date=monday + timedelta(days=6),
                platform_manager_id=pm,
            )
        else:
            month = ((i - 1) // 3) % 12 + 1
            last_day = monthrange(2026, month)[1]
            Report.generate_monthly_report(
                start_date=date(2026, month, 1),
                end_date=date(2026, month, last_day),
                platform_manager_id=pm,
            )


def seed_bulk_all() -> None:
    seed_demo_donations()
    seed_bulk_accounts()
    seed_bulk_categories()
    seed_bulk_activities()
    seed_bulk_donations()
    seed_bulk_favourites()
    seed_bulk_reports()
    seed_tc_scenario()


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
    from persistence.db import init_db

    init_db()
    seed_default_admin()
    seed_default_fundraiser()
    seed_default_donee()
    seed_default_platform_manager()
    seed_demo_donations()
    seed_bulk_all()
    FundraisingActivity.refresh_completed_flags()
    print("Seed complete.")
    print(f"  admin   : {DEFAULT_ADMIN_EMAIL} / {DEFAULT_ADMIN_PASSWORD}")
    print(f"  funder  : {DEFAULT_FUNDRAISER_EMAIL} / {DEFAULT_FUNDRAISER_PASSWORD}")
    print(f"  donee   : {DEFAULT_DONEE_EMAIL} / {DEFAULT_DONEE_PASSWORD}")
    print(f"  PM      : {DEFAULT_PM_EMAIL} / {DEFAULT_PM_PASSWORD}")
    print(
        f"  bulk    : {_count('user_account')} accounts, "
        f"{_count('fundraising_activity_category')} categories, "
        f"{_count('fundraising_activity')} activities, "
        f"{_count('donation')} donations, "
        f"{_count('favourite')} favourites, "
        f"{_count('report')} reports"
    )
