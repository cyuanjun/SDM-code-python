"""Delegation tests for ViewMyDonationHistoryController (US-33 + Exception A)."""
from __future__ import annotations

import pytest

from controller.view_my_donation_history_controller import (
    ViewMyDonationHistoryController,
)
from entity.donation import Donation


def test_view_my_donation_history_returns_entity_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "view_my_donation_history",
        classmethod(lambda cls, account_id, donation_id: "sentinel"),
    )
    assert (
        ViewMyDonationHistoryController().view_my_donation_history(
            account_id="acc_001", donation_id="don_001"
        )
        == "sentinel"
    )


def test_view_my_donation_history_forwards_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "view_my_donation_history",
        classmethod(lambda cls, account_id, donation_id: None),
    )
    assert (
        ViewMyDonationHistoryController().view_my_donation_history(
            account_id="x", donation_id="y"
        )
        is None
    )


def test_view_my_donations_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "view_my_donations",
        classmethod(lambda cls, account_id: ["sentinel"]),
    )
    assert (
        ViewMyDonationHistoryController().view_my_donations("acc_001")
        == ["sentinel"]
    )


def test_view_my_donations_forwards_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Donation,
        "view_my_donations",
        classmethod(lambda cls, account_id: []),
    )
    assert ViewMyDonationHistoryController().view_my_donations("x") == []
