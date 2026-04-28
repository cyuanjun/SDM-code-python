"""Sprint 2 controllers — pin pure-delegation contract for the new use cases."""
from controller.save_fundraiser_activity_controller import (
    SaveFundraiserActivityController,
)
from controller.search_fundraiser_activity_controller import (
    SearchFundraiserActivityController,
)
from controller.update_fundraiser_activity_controller import (
    UpdateFundraiserActivityController,
)
from controller.update_user_account_controller import UpdateUserAccountController
from controller.update_user_profile_controller import UpdateUserProfileController
from controller.view_favourite_list_controller import ViewFavouriteListController
from controller.view_fundraiser_activity_controller import (
    ViewFundraiserActivityController,
)
from controller.view_user_account_controller import ViewUserAccountController
from controller.view_user_profile_controller import ViewUserProfileController
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _make_profile_and_account():
    profile = UserProfile.create_profile("donee", "test")
    account = UserAccount.create_account(
        "c@x.com", "pw1234", "C", "1990-01-01", "1", profile.profile_id
    )
    return profile, account


def _make_activity(owner_account_id=None):
    activity = FundraisingActivity(
        title="t", description="d", target_amount=100.0, category="x",
        start_date="2026-01-01", end_date="2026-02-01", status="active",
        owner_account_id=owner_account_id,
    )
    activity.save_fundraising_activity()
    return activity


def test_view_user_profile_controller():
    profile, _ = _make_profile_and_account()
    fetched = ViewUserProfileController().view_user_profile(str(profile.profile_id))
    assert fetched is not None and fetched.role == "donee"


def test_update_user_profile_controller():
    profile, _ = _make_profile_and_account()
    updated = UserProfile(
        role="donee", description="new", profile_id=profile.profile_id
    )
    assert UpdateUserProfileController().update_user_profile(
        str(profile.profile_id), updated
    ) is True


def test_view_user_account_controller():
    _, account = _make_profile_and_account()
    fetched = ViewUserAccountController().view_user_account(str(account.account_id))
    assert fetched is not None and fetched.email == "c@x.com"


def test_update_user_account_controller():
    profile, account = _make_profile_and_account()
    updated = UserAccount(
        email="c@x.com", password="pw1234", name="New", dob="1990-01-01",
        phone_num="2", profile_id=profile.profile_id, account_id=account.account_id,
    )
    assert UpdateUserAccountController().update_user_account(
        str(account.account_id), updated
    ) is True


def test_view_fundraiser_activity_controller():
    activity = _make_activity()
    assert ViewFundraiserActivityController().view_fundraiser_activity(
        str(activity.activity_id)
    ) is not None


def test_update_fundraiser_activity_controller():
    activity = _make_activity()
    updated = FundraisingActivity(
        title="Edited", description="d", target_amount=200.0, category="x",
        start_date="2026-01-01", end_date="2026-02-01", status="active",
    )
    assert UpdateFundraiserActivityController().update_fundraiser_activity(
        str(activity.activity_id), updated
    ) is True


def test_search_controller_returns_matches():
    _make_activity()
    FundraisingActivity(
        title="Search target", description="d", target_amount=1.0, category="x",
        start_date="2026-01-01", end_date="2026-02-01", status="active",
    ).save_fundraising_activity()
    results = SearchFundraiserActivityController().submit_search_criteria("Search")
    assert any(r.title == "Search target" for r in results)


def test_save_and_view_favourite_controllers():
    profile, account = _make_profile_and_account()
    activity = _make_activity()
    assert SaveFundraiserActivityController().save_fundraising_activity(
        account.account_id, activity.activity_id
    ) is True
    favourites = ViewFavouriteListController().view_favourite_list(
        str(account.account_id)
    )
    assert len(favourites) == 1
