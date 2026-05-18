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


def test_create_profile_returns_none_for_duplicate_role() -> None:
    """Negative path: role is UNIQUE per the schema. A second profile
    with the same role must return None rather than persist a duplicate."""
    first = UserProfile.create_profile(role="admin", description="primary")
    second = UserProfile.create_profile(role="admin", description="backup")

    assert first is not None
    assert second is None


def test_update_user_profile_returns_false_for_duplicate_role() -> None:
    """Negative path: updating one profile to a role already taken by
    another profile must return False (UNIQUE constraint)."""
    admin = UserProfile.create_profile(role="admin", description="a")
    donee = UserProfile.create_profile(role="donee", description="b")
    assert admin is not None and donee is not None

    ok = UserProfile.update_user_profile(
        donee.profile_id,
        UserProfile(role="admin", description="b", suspended=False),
    )
    assert ok is False
    # Original role unchanged
    fetched = UserProfile.view_user_profile(donee.profile_id)
    assert fetched is not None and fetched.role == "donee"


def test_create_profile_defaults_suspended_to_false() -> None:
    """Negative path: the diagram method signature only takes (role, description).
    `suspended` is not a parameter and must default to a real Boolean false,
    not None or an empty string."""
    profile = UserProfile.create_profile(role="donee", description="")

    assert profile.suspended is False


def test_view_all_profiles_returns_empty_list_when_no_profiles_exist() -> None:
    """Negative path: caller must get [] back, not None."""
    assert UserProfile.view_all_profiles() == []


def test_view_all_profiles_returns_all_persisted_profiles_in_insertion_order() -> None:
    UserProfile.create_profile(role="admin", description="a")
    UserProfile.create_profile(role="fundraiser", description="b")
    UserProfile.create_profile(role="donee", description="c")

    profiles = UserProfile.view_all_profiles()

    assert [p.profile_id for p in profiles] == ["prof_001", "prof_002", "prof_003"]
    assert [p.role for p in profiles] == ["admin", "fundraiser", "donee"]


def test_view_user_profile_returns_profile_for_existing_id() -> None:
    created = UserProfile.create_profile(role="admin", description="Full access")

    fetched = UserProfile.view_user_profile(created.profile_id)

    assert fetched is not None
    assert fetched.profile_id == created.profile_id
    assert fetched.role == "admin"
    assert fetched.description == "Full access"
    assert fetched.suspended is False


def test_view_user_profile_returns_none_for_missing_id() -> None:
    """Negative path: profile_id with the right prefix but no matching row."""
    UserProfile.create_profile(role="admin", description="a")

    assert UserProfile.view_user_profile("prof_999") is None


def test_view_user_profile_returns_none_when_db_empty() -> None:
    assert UserProfile.view_user_profile("prof_001") is None


def test_update_user_profile_returns_true_on_success_and_persists_changes() -> None:
    created = UserProfile.create_profile(role="admin", description="initial")

    updated = UserProfile(
        profile_id=created.profile_id,
        role="superadmin",
        description="all permissions",
        suspended=True,
    )
    assert UserProfile.update_user_profile(created.profile_id, updated) is True

    fetched = UserProfile.view_user_profile(created.profile_id)
    assert fetched is not None
    assert fetched.role == "superadmin"
    assert fetched.description == "all permissions"
    assert fetched.suspended is True


def test_update_user_profile_returns_false_for_missing_id() -> None:
    """Negative path: updating a profile that doesn't exist returns False
    (UPDATE … WHERE no-match has rowcount 0)."""
    updated = UserProfile(role="admin", description="x", suspended=False)
    assert UserProfile.update_user_profile("prof_999", updated) is False


def test_update_user_profile_does_not_mutate_other_rows() -> None:
    """Negative path: updating one row must not touch siblings."""
    first = UserProfile.create_profile(role="admin", description="a")
    second = UserProfile.create_profile(role="donee", description="b")

    updated = UserProfile(role="renamed", description="z", suspended=False)
    UserProfile.update_user_profile(first.profile_id, updated)

    untouched = UserProfile.view_user_profile(second.profile_id)
    assert untouched is not None
    assert untouched.role == "donee"
    assert untouched.description == "b"


def test_suspend_user_profile_returns_true_and_sets_suspended_flag() -> None:
    created = UserProfile.create_profile(role="admin", description="a")
    assert created.suspended is False

    assert UserProfile.suspend_user_profile(created.profile_id) is True

    fetched = UserProfile.view_user_profile(created.profile_id)
    assert fetched is not None
    assert fetched.suspended is True


def test_suspend_user_profile_returns_false_for_missing_id() -> None:
    """Negative path: no row matches profile_id."""
    assert UserProfile.suspend_user_profile("prof_999") is False


def test_suspend_user_profile_is_idempotent_on_already_suspended() -> None:
    """Suspending an already-suspended profile still returns True (rowcount
    > 0); the row stays suspended."""
    created = UserProfile.create_profile(role="admin", description="a")
    UserProfile.suspend_user_profile(created.profile_id)

    again = UserProfile.suspend_user_profile(created.profile_id)
    assert again is True

    fetched = UserProfile.view_user_profile(created.profile_id)
    assert fetched is not None
    assert fetched.suspended is True


def test_search_user_profile_matches_role_substring_case_insensitive() -> None:
    UserProfile.create_profile(role="admin", description="full access")
    UserProfile.create_profile(role="donee", description="browse")
    UserProfile.create_profile(role="fundraiser", description="runs campaigns")

    results = UserProfile.search_user_profile("ADMIN")
    assert [p.role for p in results] == ["admin"]


def test_search_user_profile_matches_description_substring() -> None:
    UserProfile.create_profile(role="a", description="needs full access")
    UserProfile.create_profile(role="b", description="limited access")
    UserProfile.create_profile(role="c", description="no access")

    results = UserProfile.search_user_profile("limited")
    assert [p.role for p in results] == ["b"]


def test_search_user_profile_returns_empty_for_no_match() -> None:
    UserProfile.create_profile(role="admin", description="a")
    assert UserProfile.search_user_profile("nothing") == []


def test_search_user_profile_returns_empty_on_empty_db() -> None:
    assert UserProfile.search_user_profile("anything") == []
