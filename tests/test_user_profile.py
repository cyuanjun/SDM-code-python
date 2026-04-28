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
