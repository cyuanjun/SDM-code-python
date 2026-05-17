-- Revamp schema. Each table mirrors one Entity class.
--
-- PKs are TEXT in the form "{prefix}_{NNN}" (e.g. "prof_001"); see
-- persistence/ids.py for the next_id helper that mints them on INSERT.
-- FKs are TEXT too, holding the same prefixed string the parent stores.
--
-- Type proxies for diagram types SQLite can't represent natively:
--   diagram Decimal  -> SQLite TEXT     (preserves precision; entity
--                                        wraps with Decimal() on read,
--                                        str() on write)
--   diagram Date     -> SQLite TEXT     (ISO-8601; entity wraps with
--                                        date.fromisoformat() on read,
--                                        .isoformat() on write)
--   diagram Boolean  -> SQLite INTEGER  (0/1; entity wraps with bool()
--                                        on read, 1 if x else 0 on write)
-- Entity public APIs still expose the diagram types (Decimal / date /
-- bool); the proxies are storage detail.

CREATE TABLE IF NOT EXISTS user_profile (
    profile_id  TEXT PRIMARY KEY,
    role        TEXT NOT NULL,
    description TEXT,
    suspended   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_account (
    account_id TEXT PRIMARY KEY,
    email      TEXT NOT NULL UNIQUE,
    password   TEXT NOT NULL,
    name       TEXT NOT NULL,
    dob        TEXT NOT NULL,
    phone_num  TEXT NOT NULL,
    profile_id TEXT NOT NULL REFERENCES user_profile(profile_id),
    suspended  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fundraising_activity (
    fra_id           TEXT PRIMARY KEY,
    title            TEXT NOT NULL,
    description      TEXT NOT NULL,
    target_amount    TEXT NOT NULL,
    category         TEXT NOT NULL,
    start_date       TEXT NOT NULL,
    end_date         TEXT NOT NULL,
    completed        INTEGER NOT NULL DEFAULT 0,
    suspended        INTEGER NOT NULL DEFAULT 0,
    owner_account_id TEXT NOT NULL REFERENCES user_account(account_id),
    view_count       INTEGER NOT NULL DEFAULT 0,
    save_count       INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS favourite (
    account_id TEXT NOT NULL REFERENCES user_account(account_id) ON DELETE CASCADE,
    fra_id     TEXT NOT NULL REFERENCES fundraising_activity(fra_id) ON DELETE CASCADE,
    PRIMARY KEY (account_id, fra_id)
);

CREATE TABLE IF NOT EXISTS donation (
    donation_id   TEXT PRIMARY KEY,
    account_id    TEXT NOT NULL REFERENCES user_account(account_id),
    fra_id        TEXT NOT NULL REFERENCES fundraising_activity(fra_id),
    amount        TEXT NOT NULL,
    donation_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fundraising_activity_category (
    fra_cat_id    TEXT PRIMARY KEY,
    category_name TEXT NOT NULL,
    description   TEXT,
    suspended     INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS report (
    report_id              TEXT PRIMARY KEY,
    report_type            TEXT NOT NULL,
    start_date             TEXT NOT NULL,
    end_date               TEXT NOT NULL,
    generated_at           TEXT NOT NULL,
    platform_manager_id    TEXT NOT NULL REFERENCES user_account(account_id),
    total_donation_amount  TEXT NOT NULL DEFAULT '0',
    total_donation_count   INTEGER NOT NULL DEFAULT 0,
    total_activity_count   INTEGER NOT NULL DEFAULT 0,
    total_fundraiser_count INTEGER NOT NULL DEFAULT 0,
    total_donee_count      INTEGER NOT NULL DEFAULT 0
);
