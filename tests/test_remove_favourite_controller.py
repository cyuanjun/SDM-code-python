"""Delegation tests for RemoveFavouriteController (US-23)."""
from __future__ import annotations

import pytest

from controller.remove_favourite_controller import RemoveFavouriteController
from entity.favourite import Favourite


def test_controller_returns_true_when_entity_removes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Favourite,
        "remove_favourite",
        classmethod(lambda cls, fra_id, account_id: True),
    )
    assert (
        RemoveFavouriteController().remove_favourite(
            fra_id="fra_001", account_id="acc_001"
        )
        is True
    )


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Favourite,
        "remove_favourite",
        classmethod(lambda cls, fra_id, account_id: False),
    )
    assert (
        RemoveFavouriteController().remove_favourite(
            fra_id="x", account_id="y"
        )
        is False
    )
