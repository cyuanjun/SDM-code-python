"""Delegation tests for ViewFavouriteListController (US-24)."""
from __future__ import annotations

import pytest

from controller.view_favourite_list_controller import ViewFavouriteListController
from entity.favourite import Favourite


def test_controller_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sentinel = [Favourite(account_id="acc_001", fra_id="fra_001")]
    monkeypatch.setattr(
        Favourite,
        "view_favourite_list",
        classmethod(lambda cls, account_id: sentinel),
    )

    assert (
        ViewFavouriteListController().view_favourite_list("acc_001") is sentinel
    )


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: empty list forwarded unchanged."""
    monkeypatch.setattr(
        Favourite,
        "view_favourite_list",
        classmethod(lambda cls, account_id: []),
    )

    assert ViewFavouriteListController().view_favourite_list("acc_001") == []
