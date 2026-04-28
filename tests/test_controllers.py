"""Controllers are pure delegators. These tests pin that contract so any
business logic that sneaks into a controller breaks the build.
"""
from controller.create_account_controller import CreateAccountController
from controller.create_fundraising_activity_controller import (
    CreateFundraisingActivityController,
)
from controller.create_profile_controller import CreateProfileController
from controller.login_controller import LoginController
from controller.view_fundraising_activity_controller import (
    ViewFundraisingActivityController,
)
from controller.view_profiles_controller import ViewProfilesController
from entity.user_profile import UserProfile


def test_create_profile_controller_delegates():
    profile = CreateProfileController().create_profile("admin", "Top-level admin")
    assert profile is not None and profile.role == "admin"


def test_view_profiles_controller_returns_all_profiles():
    CreateProfileController().create_profile("admin", "x")
    CreateProfileController().create_profile("donee", "y")
    profiles = ViewProfilesController().view_all_profiles()
    assert len(profiles) == 2


def test_create_account_and_login_controllers_round_trip():
    profile = UserProfile.create_profile("donee", "Test")
    assert profile and profile.profile_id is not None

    account = CreateAccountController().create_account(
        email="x@y.com",
        password="pw1234",
        name="X",
        dob="1990-01-01",
        phone_num="123",
        profile_id=profile.profile_id,
    )
    assert account is not None

    user = LoginController().login("x@y.com", "pw1234")
    assert user is not None
    assert user.email == "x@y.com"


def test_create_and_view_fundraising_activity_controllers():
    from datetime import date

    success = CreateFundraisingActivityController().create_fundraising_activity(
        title="Test FSA",
        description="desc",
        target_amount=1000.0,
        category="community",
        start_date=date(2026, 5, 1),
        end_date=date(2026, 6, 1),
        owner_email=None,
    )
    assert success is True

    activity = ViewFundraisingActivityController().view_fundraising_activity_details("1")
    assert activity is not None
    assert activity.title == "Test FSA"


def test_view_all_fundraising_activities_controller_returns_list():
    from datetime import date

    ctrl = CreateFundraisingActivityController()
    ctrl.create_fundraising_activity(
        title="One", description="d", target_amount=100.0, category="x",
        start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
    )
    ctrl.create_fundraising_activity(
        title="Two", description="d", target_amount=200.0, category="x",
        start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
    )
    activities = ViewFundraisingActivityController().view_all_fundraising_activities()
    assert {a.title for a in activities} == {"One", "Two"}
