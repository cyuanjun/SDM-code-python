"""Tests for the UserProfile entity (US-1).

Diagram contract: `createProfile(role: String, description: String): UserProfile`.
Returned `profileId` follows the `prof_NNN` scheme (see persistence/ids.py).
"""
from __future__ import annotations

from entity.user_profile import UserProfile


def test_create_profile_persists_and_returns_profile_with_prefixed_id() -> None:
    profile = UserProfile.create_profile(role="admin", description="Full access")

    assert profile.profile_id == "prof_001"
    assert profile.role == "admin"
    assert profile.description == "Full access"
    assert profile.suspended is False


def test_create_profile_assigns_sequential_ids() -> None:
    first = UserProfile.create_profile(role="admin", description="a")
    second = UserProfile.create_profile(role="fundraiser", description="b")
    third = UserProfile.create_profile(role="donee", description="c")

    assert first.profile_id == "prof_001"
    assert second.profile_id == "prof_002"
    assert third.profile_id == "prof_003"


def test_create_profile_allows_multiple_profiles_with_same_role() -> None:
    """Negative path: no implicit uniqueness on role. The diagram doesn't
    declare role as a unique key, so duplicate roles must both persist with
    distinct IDs."""
    first = UserProfile.create_profile(role="admin", description="primary")
    second = UserProfile.create_profile(role="admin", description="backup")

    assert first.profile_id != second.profile_id
    assert first.role == second.role == "admin"


def test_create_profile_defaults_suspended_to_false() -> None:
    """Negative path: the diagram method signature only takes (role, description).
    `suspended` is not a parameter and must default to a real Boolean false,
    not None or an empty string."""
    profile = UserProfile.create_profile(role="donee", description="")

    assert profile.suspended is False
