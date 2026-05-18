"""Delegation tests for ViewFundraisingActivitySaveCountController (US-29)."""
from __future__ import annotations

import pytest

from controller.view_fundraising_activity_save_count_controller import (
    ViewFundraisingActivitySaveCountController,
)
from entity.fundraising_activity import FundraisingActivity


def test_controller_returns_int_when_entity_returns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_fundraising_activity_save_count",
        classmethod(lambda cls, fra_id: 7),
    )
    assert (
        ViewFundraisingActivitySaveCountController()
        .view_fundraising_activity_save_count("fra_001")
        == 7
    )


def test_controller_returns_zero_when_entity_returns_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_fundraising_activity_save_count",
        classmethod(lambda cls, fra_id: 0),
    )
    assert (
        ViewFundraisingActivitySaveCountController()
        .view_fundraising_activity_save_count("fra_999")
        == 0
    )
