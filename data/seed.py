"""Generate ~100 records per table for live demo. Idempotent: drops & recreates."""
from __future__ import annotations

import random
from datetime import date, timedelta

from faker import Faker

from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile
from persistence.db import DB_PATH, init_db

fake = Faker()
ROLES = ("admin", "fundraiser", "donee", "platform_manager")
CATEGORIES = ("medical", "education", "disaster_relief", "community", "other")
STATUSES = ("active", "completed", "suspended")


def seed() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()

    profile_ids: list[int] = []
    for _ in range(100):
        role = random.choice(ROLES)
        profile = UserProfile.create_profile(role, fake.sentence(nb_words=6))
        if profile and profile.profile_id is not None:
            profile_ids.append(profile.profile_id)

    emails: list[str] = []
    for _ in range(100):
        email = fake.unique.email()
        account = UserAccount.create_account(
            email=email,
            password="password123",
            name=fake.name(),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
            phone_num=fake.msisdn(),
            profile_id=random.choice(profile_ids),
        )
        if account is not None:
            emails.append(email)

    for _ in range(100):
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
            owner_email=random.choice(emails) if emails else None,
        )
        activity.save_fundraising_activity()

    print(
        f"Seeded {len(profile_ids)} profiles, {len(emails)} accounts, "
        f"and 100 fundraising activities into {DB_PATH}"
    )


if __name__ == "__main__":
    seed()
