-- SDM project schema. Each table corresponds to one Entity class.
-- Field names mirror the UML class diagrams (snake_case in code, original case here).

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
    dob        TEXT,
    phone_num  TEXT,
    profile_id INTEGER NOT NULL REFERENCES user_profile(profile_id),
    suspended  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS fundraising_activity (
    activity_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    title         TEXT NOT NULL,
    description   TEXT,
    target_amount REAL NOT NULL,
    category      TEXT NOT NULL,
    start_date    TEXT NOT NULL,
    end_date      TEXT NOT NULL,
    status        TEXT NOT NULL,
    owner_account_id INTEGER REFERENCES user_account(account_id),
    view_count    INTEGER NOT NULL DEFAULT 0,
    save_count    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS favourite_list (
    account_id  INTEGER NOT NULL REFERENCES user_account(account_id) ON DELETE CASCADE,
    activity_id INTEGER NOT NULL REFERENCES fundraising_activity(activity_id) ON DELETE CASCADE,
    PRIMARY KEY (account_id, activity_id)
);

CREATE TABLE IF NOT EXISTS fundraising_activity_category (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE,
    description   TEXT,
    status        TEXT NOT NULL DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS report (
    report_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    report_type            TEXT NOT NULL,
    start_date             TEXT NOT NULL,
    end_date               TEXT NOT NULL,
    generated_at           TEXT NOT NULL,
    platform_manager_id    INTEGER REFERENCES user_account(account_id),
    total_donation_amount  REAL NOT NULL DEFAULT 0,
    total_donation_count   INTEGER NOT NULL DEFAULT 0,
    total_activity_count   INTEGER NOT NULL DEFAULT 0,
    total_fundraiser_count INTEGER NOT NULL DEFAULT 0,
    total_donee_count      INTEGER NOT NULL DEFAULT 0
);

