"""Sprint 3 controllers — pin pure-delegation contract for the new use cases."""
from controller.delete_favourite_controller import DeleteFavouriteController
from controller.delete_user_profile_controller import DeleteUserProfileController
from controller.search_completed_activity_controller import (
    SearchCompletedActivityController,
)
from controller.search_favourite_controller import SearchFavouriteController
from controller.search_fundraising_activity_controller import (
    SearchFundraisingActivityController,
)
from controller.search_user_account_controller import SearchUserAccountController
from controller.search_user_profile_controller import SearchUserProfileController
from controller.suspend_fundraising_activity_controller import (
    SuspendFundraisingActivityController,
)
from controller.suspend_user_account_controller import SuspendUserAccountController
from controller.view_completed_activity_controller import (
    ViewCompletedActivityController,
)
from entity.favourite_list import FavouriteList
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _profile_and_account(role="donee", email="x@y.com"):
    profile = UserProfile.create_profile(role, "test")
    account = UserAccount.create_account(
        email, "pw1234", "N", "1990-01-01", "1", profile.profile_id
    )
    return profile, account


def _activity(owner_account_id=None, title="t", status="active"):
    activity = FundraisingActivity(
        title=title, description="d", target_amount=100.0, category="x",
        start_date="2026-01-01", end_date="2026-02-01", status=status,
        owner_account_id=owner_account_id,
    )
    activity.save_fundraising_activity()
    return activity


def test_delete_user_profile_controller_delegates():
    profile = UserProfile.create_profile("admin", "x")
    assert DeleteUserProfileController().delete_user_profile(
        str(profile.profile_id)
    ) is True


def test_search_user_profile_controller_delegates():
    UserProfile.create_profile("admin", "x")
    UserProfile.create_profile("donee", "y")
    results = SearchUserProfileController().submit_search_criteria("admin")
    assert {p.role for p in results} == {"admin"}


def test_suspend_user_account_controller_delegates():
    _, account = _profile_and_account()
    assert SuspendUserAccountController().suspend_user_account(
        str(account.account_id)
    ) is True


def test_search_user_account_controller_delegates():
    _profile_and_account(email="alice@x.com")
    _profile_and_account(email="bob@y.com")
    results = SearchUserAccountController().submit_search_criteria("alice")
    assert {a.email for a in results} == {"alice@x.com"}


def test_suspend_fundraising_activity_controller_delegates():
    activity = _activity()
    assert SuspendFundraisingActivityController().suspend_fundraising_activity(
        str(activity.activity_id)
    ) is True


def test_search_fundraising_activity_controller_delegates_with_owner():
    _, owner = _profile_and_account(role="fundraiser", email="own@x.com")
    _activity(owner_account_id=owner.account_id, title="Mine")
    _activity(owner_account_id=None, title="Theirs")
    results = SearchFundraisingActivityController().submit_search_criteria(
        "", owner_account_id=owner.account_id
    )
    assert {a.title for a in results} == {"Mine"}


def test_delete_favourite_controller_delegates():
    _, account = _profile_and_account()
    activity = _activity()
    FavouriteList.save_fundraising_activity(account.account_id, activity.activity_id)
    assert DeleteFavouriteController().delete_favourite(
        activity.activity_id, account.account_id
    ) is True


def test_search_favourite_controller_delegates():
    _, account = _profile_and_account()
    a1 = _activity(title="Animal Shelter")
    a2 = _activity(title="Education Drive")
    FavouriteList.save_fundraising_activity(account.account_id, a1.activity_id)
    FavouriteList.save_fundraising_activity(account.account_id, a2.activity_id)
    results = SearchFavouriteController().submit_search_criteria(
        "animal", account_id=account.account_id
    )
    assert {f.activity_id for f in results} == {a1.activity_id}


def test_search_completed_activity_controller_delegates():
    _, owner = _profile_and_account(role="fundraiser", email="own@x.com")
    _activity(owner_account_id=owner.account_id, title="Done", status="completed")
    _activity(owner_account_id=owner.account_id, title="Active", status="active")
    results = SearchCompletedActivityController().submit_search_criteria(
        "", owner_account_id=owner.account_id, status="completed"
    )
    assert {a.title for a in results} == {"Done"}


def test_view_completed_activity_controller_delegates():
    activity = _activity(title="Finished", status="completed")
    fetched = ViewCompletedActivityController().view_completed_activity(
        str(activity.activity_id)
    )
    assert fetched is not None and fetched.title == "Finished"
