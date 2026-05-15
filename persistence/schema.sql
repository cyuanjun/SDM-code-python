-- Revamp schema. Tables land here as their entities are rebuilt from the
-- reworked diagrams. Each table mirrors one Entity class.
-- SQLite column types follow type-affinity rules; INTEGER PKs are surfaced
-- as prefixed strings via persistence/ids.py.

CREATE TABLE IF NOT EXISTS user_profile (
    profile_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    role        TEXT NOT NULL,
    description TEXT,
    suspended   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_account (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email      TEXT NOT NULL UNIQUE,
    password   TEXT NOT NULL,
    name       TEXT NOT NULL,
    dob        TEXT NOT NULL,
    phone_num  TEXT NOT NULL,
    profile_id INTEGER NOT NULL REFERENCES user_profile(profile_id),
    suspended  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fundraising_activity (
    fra_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT NOT NULL,
    description      TEXT NOT NULL,
    target_amount    TEXT NOT NULL,
    category         TEXT NOT NULL,
    start_date       TEXT NOT NULL,
    end_date         TEXT NOT NULL,
    completed        INTEGER NOT NULL DEFAULT 0,
    suspended        INTEGER NOT NULL DEFAULT 0,
    owner_account_id INTEGER NOT NULL REFERENCES user_account(account_id),
    view_count       INTEGER NOT NULL DEFAULT 0,
    save_count       INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS favourite (
    account_id INTEGER NOT NULL REFERENCES user_account(account_id) ON DELETE CASCADE,
    fra_id     INTEGER NOT NULL REFERENCES fundraising_activity(fra_id) ON DELETE CASCADE,
    PRIMARY KEY (account_id, fra_id)
);

CREATE TABLE IF NOT EXISTS donation (
    donation_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id    INTEGER NOT NULL REFERENCES user_account(account_id),
    fra_id        INTEGER NOT NULL REFERENCES fundraising_activity(fra_id),
    amount        TEXT NOT NULL,
    donation_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fundraising_activity_category (
    fra_cat_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL,
    description   TEXT,
    suspended     INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS report (
    report_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    report_type            TEXT NOT NULL,
    start_date             TEXT NOT NULL,
    end_date               TEXT NOT NULL,
    generated_at           TEXT NOT NULL,
    platform_manager_id    INTEGER NOT NULL REFERENCES user_account(account_id),
    total_donation_amount  TEXT NOT NULL DEFAULT '0',
    total_donation_count   INTEGER NOT NULL DEFAULT 0,
    total_activity_count   INTEGER NOT NULL DEFAULT 0,
    total_fundraiser_count INTEGER NOT NULL DEFAULT 0,
    total_donee_count      INTEGER NOT NULL DEFAULT 0
);
