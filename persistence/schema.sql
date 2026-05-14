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
