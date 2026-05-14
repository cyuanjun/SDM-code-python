"""Delegation tests for ViewFavouriteController (US-24)."""
from __future__ import annotations

import pytest

from controller.view_favourite_controller import ViewFavouriteController
from entity.favourite import Favourite


def test_controller_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sentinel = [Favourite(account_id="acc_001", fra_id="fra_001")]
    monkeypatch.setattr(
        Favourite,
        "view_favourites",
        classmethod(lambda cls, account_id: sentinel),
    )

    assert (
        ViewFavouriteController().view_favourites("acc_001") is sentinel
    )


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: empty list forwarded unchanged."""
    monkeypatch.setattr(
        Favourite,
        "view_favourites",
        classmethod(lambda cls, account_id: []),
    )

    assert ViewFavouriteController().view_favourites("acc_001") == []
