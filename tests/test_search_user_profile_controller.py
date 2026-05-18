"""Delegation tests for SearchUserProfileController (US-5)."""
from __future__ import annotations

import pytest

from controller.search_user_profile_controller import (
    SearchUserProfileController,
)
from entity.user_profile import UserProfile


def test_controller_returns_entity_list_unchanged() -> None:
    UserProfile.create_profile(role="admin", description="a")
    results = SearchUserProfileController().search_user_profile("admin")
    assert [p.role for p in results] == ["admin"]


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserProfile,
        "search_user_profile",
        classmethod(lambda cls, search_criteria: []),
    )
    assert SearchUserProfileController().search_user_profile("x") == []
