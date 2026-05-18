"""Delegation tests for ViewProfilesController (Exception A)."""
from __future__ import annotations

import pytest

from controller.non_diagram.view_profiles_controller import ViewProfilesController
from entity.user_profile import UserProfile


def test_controller_returns_entity_list_unchanged() -> None:
    UserProfile.create_profile(role="admin", description="a")
    UserProfile.create_profile(role="donee", description="b")

    profiles = ViewProfilesController().view_all_profiles()

    assert [p.profile_id for p in profiles] == ["prof_001", "prof_002"]


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: when the entity returns [] (no rows), the
    controller must forward that unchanged."""
    monkeypatch.setattr(
        UserProfile, "view_all_profiles", classmethod(lambda cls: [])
    )

    assert ViewProfilesController().view_all_profiles() == []
