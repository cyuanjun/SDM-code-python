"""Delegation tests for CreateProfileController (US-1).

Controllers are pure delegators per CLAUDE.md — they forward Boundary input
to one Entity method and return whatever the Entity returns, unchanged.

UserProfile.create_profile has no failure return path (it always returns a
UserProfile or raises). The negative-path mirror is therefore exercised by
monkey-patching the entity to verify the controller forwards an arbitrary
return value without inspection or transformation.
"""
from __future__ import annotations

import pytest

from controller.create_profile_controller import CreateProfileController
from entity.user_profile import UserProfile


def test_controller_returns_the_user_profile_entity_returns() -> None:
    result = CreateProfileController().create_profile(
        role="admin", description="Full access"
    )

    assert isinstance(result, UserProfile)
    assert result.role == "admin"
    assert result.description == "Full access"
    assert result.profile_id == "prof_001"


def test_controller_forwards_entity_return_value_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sentinel = UserProfile(
        role="sentinel", description="forwarded", profile_id="prof_999"
    )
    monkeypatch.setattr(
        UserProfile, "create_profile", classmethod(lambda cls, role, description: sentinel)
    )

    result = CreateProfileController().create_profile(role="x", description="y")

    assert result is sentinel
