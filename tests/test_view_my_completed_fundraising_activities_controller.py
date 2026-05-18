"""Delegation tests for ViewMyCompletedFundraisingActivitiesController (US-31)."""
from __future__ import annotations

import pytest

from controller.view_my_completed_fundraising_activities_controller import (
    ViewMyCompletedFundraisingActivitiesController,
)
from entity.fundraising_activity import FundraisingActivity


def test_controller_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_my_completed_fundraising_activities",
        classmethod(lambda cls, owner_account_id: ["sentinel"]),
    )
    assert (
        ViewMyCompletedFundraisingActivitiesController()
        .view_my_completed_fundraising_activities(owner_account_id="acc_001")
        == ["sentinel"]
    )


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "view_my_completed_fundraising_activities",
        classmethod(lambda cls, owner_account_id: []),
    )
    assert (
        ViewMyCompletedFundraisingActivitiesController()
        .view_my_completed_fundraising_activities(owner_account_id="x")
        == []
    )
