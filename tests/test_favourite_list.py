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


# ---- Sprint 3 ----

def test_delete_favourite_removes_row():
    account_id, activity_id = _make_account_and_activity()
    FavouriteList.save_fundraising_activity(account_id, activity_id)
    assert FavouriteList.delete_favourite(activity_id, account_id) is True
    assert FavouriteList.view_favourite_list(str(account_id)) == []


def test_delete_favourite_returns_false_when_no_match():
    account_id, _ = _make_account_and_activity()
    assert FavouriteList.delete_favourite(99999, account_id) is False


def test_submit_search_criteria_favourite_filters_by_text_and_account():
    profile = UserProfile.create_profile("donee", "x")
    me = UserAccount.create_account(
        "me@x.com", "pw", "M", "1990-01-01", "1", profile.profile_id
    )
    them = UserAccount.create_account(
        "them@x.com", "pw", "T", "1990-01-01", "2", profile.profile_id
    )

    a1 = FundraisingActivity(
        title="Animal Shelter", description="d", target_amount=1.0,
        category="community", start_date="2026-01-01", end_date="2026-02-01",
        status="active",
    )
    a1.save_fundraising_activity()
    a2 = FundraisingActivity(
        title="Education Drive", description="d", target_amount=1.0,
        category="education", start_date="2026-01-01", end_date="2026-02-01",
        status="active",
    )
    a2.save_fundraising_activity()

    FavouriteList.save_fundraising_activity(me.account_id, a1.activity_id)
    FavouriteList.save_fundraising_activity(me.account_id, a2.activity_id)
    FavouriteList.save_fundraising_activity(them.account_id, a1.activity_id)

    matches = FavouriteList.submit_search_criteria(
        "animal", account_id=me.account_id
    )
    assert {f.activity_id for f in matches} == {a1.activity_id}

    no_match = FavouriteList.submit_search_criteria(
        "zzz", account_id=me.account_id
    )
    assert no_match == []
