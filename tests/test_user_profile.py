from entity.user_profile import UserProfile


def test_create_profile_persists_record():
    profile = UserProfile.create_profile("fundraiser", "Verified charity")
    assert profile is not None
    assert profile.profile_id is not None
    assert profile.role == "fundraiser"
    assert profile.description == "Verified charity"


def test_view_all_profiles_returns_every_active_profile():
    UserProfile.create_profile("admin", "First admin")
    UserProfile.create_profile("donee", "First donee")
    UserProfile.create_profile("fundraiser", "First fundraiser")

    profiles = UserProfile.view_all_profiles()
    assert len(profiles) == 3
    assert {p.role for p in profiles} == {"admin", "donee", "fundraiser"}


def test_view_all_profiles_returns_empty_when_no_records():
    assert UserProfile.view_all_profiles() == []


def test_view_user_profile_returns_profile_by_id():
    created = UserProfile.create_profile("admin", "Top admin")
    assert created and created.profile_id is not None
    fetched = UserProfile.view_user_profile(str(created.profile_id))
    assert fetched is not None
    assert fetched.role == "admin"


def test_view_user_profile_returns_none_for_missing_id():
    assert UserProfile.view_user_profile("99999") is None


def test_update_user_profile_persists_changes():
    created = UserProfile.create_profile("donee", "Old desc")
    assert created and created.profile_id is not None
    updated = UserProfile(
        role="donee",
        description="New desc",
        profile_id=created.profile_id,
    )
    assert UserProfile.update_user_profile(str(created.profile_id), updated) is True

    fetched = UserProfile.view_user_profile(str(created.profile_id))
    assert fetched is not None
    assert fetched.description == "New desc"


def test_update_user_profile_returns_false_for_missing_id():
    dummy = UserProfile(role="x", description="x", profile_id=99999)
    assert UserProfile.update_user_profile("99999", dummy) is False
