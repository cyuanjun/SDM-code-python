"""Delegation tests for SuspendUserProfileController (US-4)."""
from __future__ import annotations

import pytest

from controller.suspend_user_profile_controller import (
    SuspendUserProfileController,
)
from entity.user_profile import UserProfile


def test_controller_returns_true_when_entity_suspends() -> None:
    created = UserProfile.create_profile(role="admin", description="a")
    assert (
        SuspendUserProfileController().suspend_user_profile(created.profile_id)
        is True
    )


def test_controller_returns_false_when_entity_returns_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserProfile,
        "suspend_user_profile",
        classmethod(lambda cls, profile_id: False),
    )
    assert SuspendUserProfileController().suspend_user_profile("x") is False
