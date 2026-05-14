"""Delegation tests for SearchFavouriteController (US-25)."""
from __future__ import annotations

import pytest

from controller.search_favourite_controller import SearchFavouriteController
from entity.favourite import Favourite


def test_controller_returns_entity_list_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sentinel = [Favourite(account_id="acc_001", fra_id="fra_007")]
    monkeypatch.setattr(
        Favourite,
        "search_favourite",
        classmethod(lambda cls, search_criteria, account_id: sentinel),
    )
    result = SearchFavouriteController().search_favourite(
        search_criteria="x", account_id="acc_001"
    )
    assert result is sentinel


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        Favourite,
        "search_favourite",
        classmethod(lambda cls, search_criteria, account_id: []),
    )
    assert (
        SearchFavouriteController().search_favourite(
            search_criteria="x", account_id="y"
        )
        == []
    )
