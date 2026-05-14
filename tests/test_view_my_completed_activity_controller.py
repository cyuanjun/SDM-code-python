"""Delegation tests for ViewMyCompletedActivityController (US-31)."""
from __future__ import annotations

import pytest

from controller.view_my_completed_activity_controller import (
    ViewMyCompletedActivityController,
)
from entity.fundraising_activity import FundraisingActivity


def test_controller_returns_activity_when_entity_returns_one(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_my_completed_activity",
        classmethod(lambda cls, owner_account_id, fra_id: "sentinel"),
    )
    assert (
        ViewMyCompletedActivityController().view_my_completed_activity(
            owner_account_id="acc_001", fra_id="fra_001"
        )
        == "sentinel"
    )


def test_controller_returns_none_when_entity_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_my_completed_activity",
        classmethod(lambda cls, owner_account_id, fra_id: None),
    )
    assert (
        ViewMyCompletedActivityController().view_my_completed_activity(
            owner_account_id="x", fra_id="y"
        )
        is None
    )
