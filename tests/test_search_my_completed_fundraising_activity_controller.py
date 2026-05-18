"""Delegation tests for SearchMyCompletedFundraisingActivityController (US-30)."""
from __future__ import annotations

import pytest

from controller.search_my_completed_fundraising_activity_controller import (
    SearchMyCompletedFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity


def test_controller_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "search_my_completed_fundraising_activity",
        classmethod(lambda cls, owner_account_id, search_criteria: ["sentinel"]),
    )
    assert (
        SearchMyCompletedFundraisingActivityController().search_my_completed_fundraising_activity(
            owner_account_id="acc_001", search_criteria="x"
        )
        == ["sentinel"]
    )


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "search_my_completed_fundraising_activity",
        classmethod(lambda cls, owner_account_id, search_criteria: []),
    )
    assert (
        SearchMyCompletedFundraisingActivityController().search_my_completed_fundraising_activity(
            owner_account_id="x", search_criteria="y"
        )
        == []
    )
