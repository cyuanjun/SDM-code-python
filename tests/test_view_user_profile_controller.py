"""Delegation tests for ViewUserProfileController (US-2)."""
from __future__ import annotations

import pytest

from controller.view_user_profile_controller import ViewUserProfileController
from entity.user_profile import UserProfile


def test_controller_returns_profile_when_entity_returns_one() -> None:
    created = UserProfile.create_profile(role="admin", description="a")

    result = ViewUserProfileController().view_user_profile(created.profile_id)

    assert result is not None
    assert result.profile_id == created.profile_id


def test_controller_returns_none_when_entity_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: when UserProfile.view_user_profile returns
    None, the controller must forward None unchanged."""
    monkeypatch.setattr(
        UserProfile,
        "view_user_profile",
        classmethod(lambda cls, profile_id: None),
    )

    assert ViewUserProfileController().view_user_profile("anything") is None
