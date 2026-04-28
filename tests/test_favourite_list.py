from entity.favourite_list import FavouriteList
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _make_account_and_activity():
    profile = UserProfile.create_profile("donee", "test")
    account = UserAccount.create_account(
        "fav@x.com", "pw", "Fav", "1990-01-01", "1", profile.profile_id
    )
    activity = FundraisingActivity(
        title="T", description="D", target_amount=100.0, category="x",
        start_date="2026-01-01", end_date="2026-02-01", status="active",
    )
    activity.save_fundraising_activity()
    return account.account_id, activity.activity_id


def test_save_fundraising_activity_persists_favourite():
    account_id, activity_id = _make_account_and_activity()
    assert FavouriteList.save_fundraising_activity(account_id, activity_id) is True
    favourites = FavouriteList.view_favourite_list(str(account_id))
    assert len(favourites) == 1
    assert favourites[0].activity_id == activity_id


def test_save_fundraising_activity_returns_false_on_duplicate():
    account_id, activity_id = _make_account_and_activity()
    FavouriteList.save_fundraising_activity(account_id, activity_id)
    assert FavouriteList.save_fundraising_activity(account_id, activity_id) is False


def test_view_favourite_list_returns_empty_when_none():
    assert FavouriteList.view_favourite_list("1") == []


def test_remove_favourite_deletes_row():
    account_id, activity_id = _make_account_and_activity()
    FavouriteList.save_fundraising_activity(account_id, activity_id)
    assert FavouriteList.remove_favourite(account_id, activity_id) is True
    assert FavouriteList.view_favourite_list(str(account_id)) == []
