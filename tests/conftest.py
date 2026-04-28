"""Shared pytest fixtures. Each test gets a fresh in-memory-style DB by pointing
DB_PATH at a temp file and re-initialising the schema.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from persistence import db as db_module


@pytest.fixture(autouse=True)
def fresh_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db_module, "DB_PATH", test_db)
    db_module.init_db()
    return test_db
