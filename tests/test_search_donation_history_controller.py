"""Delegation tests for SearchDonationHistoryController (US-32)."""
from __future__ import annotations

import pytest

from controller.search_donation_history_controller import (
    SearchDonationHistoryController,
)
from entity.donation import Donation


def test_controller_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "search_donation_history",
        classmethod(lambda cls, account_id, search_criteria: ["sentinel"]),
    )
    assert (
        SearchDonationHistoryController().search_donation_history(
            account_id="acc_001", search_criteria="x"
        )
        == ["sentinel"]
    )


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "search_donation_history",
        classmethod(lambda cls, account_id, search_criteria: []),
    )
    assert (
        SearchDonationHistoryController().search_donation_history(
            account_id="y", search_criteria="x"
        )
        == []
    )
