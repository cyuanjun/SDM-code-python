-- SDM project schema. Each table corresponds to one Entity class.
-- Field names mirror the UML class diagrams (snake_case in code, original case here).

CREATE TABLE IF NOT EXISTS user_profile (
    profile_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    role        TEXT NOT NULL,
    description TEXT,
    suspended   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS user_account (
    email      TEXT PRIMARY KEY,
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
    owner_email   TEXT REFERENCES user_account(email)
);
