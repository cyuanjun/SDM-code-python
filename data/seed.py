"""Generate seed records for development. Idempotent: drops & recreates app.db.

NOTE: the project spec asks for ~100 records per table for the live demo.
RECORD_COUNT is currently 10 for fast local iteration — bump it back to 100
before recording the marking demo.
"""
from __future__ import annotations

import random
from datetime import date, timedelta

from faker import Faker

from entity.fundraising_activity import FundraisingActivity
from entity.fundraising_activity_category import FundraisingActivityCategory
from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from persistence.db import DB_PATH, init_db

RECORD_COUNT = 10
FAVOURITE_ATTEMPTS = RECORD_COUNT * 2

fake = Faker()
ROLES = ("admin", "fundraiser", "donee", "platform_manager")
CATEGORIES = ("medical", "education", "disaster_relief", "community", "other")
STATUSES = ("active", "completed", "suspended")
CATEGORY_DESCRIPTIONS = {
    "medical": "Medical emergencies, treatment, and ongoing care.",
    "education": "Tuition, supplies, and school-related needs.",
    "disaster_relief": "Response and recovery after natural disasters.",
    "community": "Local projects supporting neighbourhoods and groups.",
    "other": "Causes not covered by the listed categories.",
}


def seed() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()

    # First len(ROLES) profiles pin one per role so the demo always has at
    # least one of each (including platform_manager, who needs an account
    # to log in via the shared LoginPage — see Sprint 1 US-39 diagram).
    profile_ids: list[int] = []
    for i in range(RECORD_COUNT):
        role = ROLES[i] if i < len(ROLES) else random.choice(ROLES)
        profile = UserProfile.create_profile(role, fake.sentence(nb_words=6))
        if profile and profile.profile_id is not None:
            profile_ids.append(profile.profile_id)

    account_ids: list[int] = []
    for i in range(RECORD_COUNT):
        # Same pinning for accounts: first len(ROLES) accounts each take a
        # different role's profile, so every role has a logged-in-able account.
        if i < len(ROLES) and i < len(profile_ids):
            profile_id = profile_ids[i]
        else:
            profile_id = random.choice(profile_ids)
        account = UserAccount.create_account(
            email=fake.unique.email(),
            password="password123",
            name=fake.name(),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
            phone_num=fake.msisdn(),
            profile_id=profile_id,
        )
        if account is not None and account.account_id is not None:
            account_ids.append(account.account_id)

    activity_ids: list[int] = []
    for _ in range(RECORD_COUNT):
        start = fake.date_between(start_date="-1y", end_date="+30d")
        end = start + timedelta(days=random.randint(7, 90))
        activity = FundraisingActivity(
            title=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=3),
            target_amount=round(random.uniform(500, 50000), 2),
            category=random.choice(CATEGORIES),
            start_date=start.isoformat(),
            end_date=end.isoformat(),
            status=random.choice(STATUSES),
            owner_account_id=random.choice(account_ids) if account_ids else None,
        )
        if activity.save_fundraising_activity() and activity.activity_id is not None:
            activity_ids.append(activity.activity_id)

    favourites_added = 0
    if account_ids and activity_ids:
        from entity.favourite_list import FavouriteList

        for _ in range(FAVOURITE_ATTEMPTS):
            account_id = random.choice(account_ids)
            activity_id = random.choice(activity_ids)
            if FavouriteList.save_fundraising_activity(account_id, activity_id):
                favourites_added += 1

    category_ids: list[int] = []
    for name in CATEGORIES:
        if FundraisingActivityCategory.create_category(
            name, CATEGORY_DESCRIPTIONS[name]
        ):
            category_ids.append(name)

    print(
        f"Seeded {len(profile_ids)} profiles, {len(account_ids)} accounts, "
        f"{len(activity_ids)} fundraising activities, "
        f"{favourites_added} favourites, "
        f"and {len(category_ids)} categories into {DB_PATH}"
    )


if __name__ == "__main__":
    seed()
