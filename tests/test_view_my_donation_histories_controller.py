"""Delegation tests for ViewMyDonationHistoriesController (US-33)."""
from __future__ import annotations

import pytest

from controller.view_my_donation_histories_controller import (
    ViewMyDonationHistoriesController,
)
from entity.donation import Donation


def test_controller_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "view_my_donation_histories",
        classmethod(lambda cls, account_id: ["sentinel"]),
    )
    assert (
        ViewMyDonationHistoriesController().view_my_donation_histories(
            account_id="acc_001"
        )
        == ["sentinel"]
    )


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "view_my_donation_histories",
        classmethod(lambda cls, account_id: []),
    )
    assert (
        ViewMyDonationHistoriesController().view_my_donation_histories(
            account_id="x"
        )
        == []
    )
