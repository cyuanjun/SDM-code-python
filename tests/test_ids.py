"""Tests for persistence.ids helpers."""
from __future__ import annotations

from persistence.db import get_connection
from persistence.ids import format_id, next_id


def test_format_id_zero_pads_to_three_digits() -> None:
    assert format_id("prof", 1) == "prof_001"
    assert format_id("acc", 42) == "acc_042"


def test_format_id_overflows_padding_gracefully_for_large_numbers() -> None:
    assert format_id("fra", 1234) == "fra_1234"


def test_next_id_returns_001_when_table_is_empty() -> None:
    with get_connection() as conn:
        assert next_id(conn, "user_profile", "profile_id", "prof") == "prof_001"


def test_next_id_increments_after_existing_rows() -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO user_profile (profile_id, role, description) "
            "VALUES (?, ?, ?)",
            ("prof_001", "admin", ""),
        )
        conn.execute(
            "INSERT INTO user_profile (profile_id, role, description) "
            "VALUES (?, ?, ?)",
            ("prof_002", "fundraiser", ""),
        )
        assert next_id(conn, "user_profile", "profile_id", "prof") == "prof_003"


def test_next_id_uses_lexicographic_max_so_zero_padding_matters() -> None:
    """With 3-digit zero-padding, lexicographic ORDER BY ... DESC LIMIT 1
    matches numeric ORDER BY ... DESC LIMIT 1 up to 999 rows.

    Inserts 4 rows with distinct roles (UNIQUE constraint) but explicit
    profile_id values so the ordering — not the next_id minted by the
    helper — is what's exercised."""
    with get_connection() as conn:
        for n, role in zip((1, 2, 9, 10), ("a", "b", "c", "d")):
            conn.execute(
                "INSERT INTO user_profile (profile_id, role, description) "
                "VALUES (?, ?, ?)",
                (format_id("prof", n), role, ""),
            )
        assert next_id(conn, "user_profile", "profile_id", "prof") == "prof_011"
