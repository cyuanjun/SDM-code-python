"""Delegation tests for ViewFundraisingActivityViewCountController (US-28)."""
from __future__ import annotations

import pytest

from controller.view_fundraising_activity_view_count_controller import (
    ViewFundraisingActivityViewCountController,
)
from entity.fundraising_activity import FundraisingActivity


def test_controller_returns_int_when_entity_returns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_fundraising_activity_view_count",
        classmethod(lambda cls, fra_id: 42),
    )
    assert (
        ViewFundraisingActivityViewCountController()
        .view_fundraising_activity_view_count("fra_001")
        == 42
    )


def test_controller_returns_zero_when_entity_returns_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: 0 forwarded unchanged."""
    monkeypatch.setattr(
        FundraisingActivity,
        "view_fundraising_activity_view_count",
        classmethod(lambda cls, fra_id: 0),
    )
    assert (
        ViewFundraisingActivityViewCountController()
        .view_fundraising_activity_view_count("fra_999")
        == 0
    )
