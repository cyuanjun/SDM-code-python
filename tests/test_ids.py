"""Tests for persistence/ids.py — happy and negative paths for both helpers."""
from __future__ import annotations

import pytest

from persistence.ids import format_id, parse_id


def test_format_id_zero_pads_to_three_digits() -> None:
    assert format_id("prof", 1) == "prof_001"
    assert format_id("acc", 42) == "acc_042"


def test_format_id_overflows_padding_gracefully_for_large_rowids() -> None:
    assert format_id("fra", 1234) == "fra_1234"


def test_parse_id_extracts_rowid() -> None:
    assert parse_id("prof_001") == 1
    assert parse_id("acc_042") == 42
    assert parse_id("fra_1234") == 1234


def test_parse_id_raises_on_missing_underscore() -> None:
    with pytest.raises(ValueError):
        parse_id("malformed")


def test_parse_id_raises_on_non_numeric_suffix() -> None:
    with pytest.raises(ValueError):
        parse_id("prof_abc")
