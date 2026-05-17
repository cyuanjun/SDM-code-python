"""Shared pytest fixtures. Each test gets a fresh in-memory-style DB by pointing
DB_PATH at a temp file and re-initialising the schema.

A default `FundraisingActivityCategory` ("Test", id `cat_001`) is also seeded
on every test so the FK on `fundraising_activity.fra_cat_id` resolves without
each test having to set up its own category. The category-entity test module
opts out (it asserts against a clean category table) — see the `request.node`
check below.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from entity.fundraising_activity_category import FundraisingActivityCategory
from persistence import db as db_module


DEFAULT_TEST_CATEGORY_ID = "cat_001"


@pytest.fixture(autouse=True)
def fresh_db(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> Path:
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", test_db)
    db_module.init_db()
    # Seed a default category so every test can create activities without
    # explicitly seeding a category first. Tests that need multiple distinct
    # categories should create additional ones in-test.
    # Skip for the category-entity tests, which expect a clean table.
    if "test_fundraising_activity_category" not in request.node.nodeid:
        FundraisingActivityCategory.create_category(
            category_name="Test", description="Default seeded test category",
        )
    return test_db
