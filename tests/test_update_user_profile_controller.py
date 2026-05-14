"""Delegation tests for UpdateUserProfileController (US-3)."""
from __future__ import annotations

import pytest

from controller.update_user_profile_controller import (
    UpdateUserProfileController,
)
from entity.user_profile import UserProfile


def test_controller_returns_true_when_entity_updates_a_row() -> None:
    created = UserProfile.create_profile(role="admin", description="a")
    updated = UserProfile(role="superadmin", description="z", suspended=False)

    assert (
        UpdateUserProfileController().update_user_profile(
            created.profile_id, updated
        )
        is True
    )


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: when the entity returns False (no row matched),
    the controller must forward False unchanged."""
    monkeypatch.setattr(
        UserProfile,
        "update_user_profile",
        classmethod(lambda cls, profile_id, updated_profile: False),
    )

    result = UpdateUserProfileController().update_user_profile(
        "anything", UserProfile(role="x", description="y")
    )
    assert result is False
