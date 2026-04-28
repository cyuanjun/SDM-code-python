from entity.fundraising_activity import FundraisingActivity


def _make_activity(**overrides) -> FundraisingActivity:
    defaults = dict(
        title="Help Animal Shelter",
        description="Raising funds for new kennels",
        target_amount=5000.0,
        category="community",
        start_date="2026-05-01",
        end_date="2026-06-01",
        status="active",
    )
    defaults.update(overrides)
    return FundraisingActivity(**defaults)


def test_save_fundraising_activity_persists_and_returns_true():
    activity = _make_activity()
    assert activity.save_fundraising_activity() is True
    assert activity.activity_id is not None


def test_view_fundraising_activity_details_returns_saved_activity():
    activity = _make_activity()
    activity.save_fundraising_activity()
    fetched = FundraisingActivity.view_fundraising_activity_details(activity.activity_id)
    assert fetched is not None
    assert fetched.title == activity.title
    assert fetched.target_amount == activity.target_amount


def test_view_fundraising_activity_details_returns_none_for_missing_id():
    assert FundraisingActivity.view_fundraising_activity_details("99999") is None


def test_view_all_fundraising_activities_returns_every_record():
    _make_activity(title="A").save_fundraising_activity()
    _make_activity(title="B").save_fundraising_activity()
    _make_activity(title="C").save_fundraising_activity()
    activities = FundraisingActivity.view_all_fundraising_activities()
    assert [a.title for a in activities] == ["A", "B", "C"]


def test_view_all_fundraising_activities_returns_empty_when_no_records():
    assert FundraisingActivity.view_all_fundraising_activities() == []


def test_view_fundraiser_activity_returns_activity():
    activity = _make_activity()
    activity.save_fundraising_activity()
    fetched = FundraisingActivity.view_fundraiser_activity(str(activity.activity_id))
    assert fetched is not None
    assert fetched.title == activity.title


def test_view_activities_by_owner_filters_by_owner():
    from entity.user_account import UserAccount
    from entity.user_profile import UserProfile

    profile = UserProfile.create_profile("fundraiser", "test")
    me = UserAccount.create_account(
        "me@x.com", "pw", "Me", "1990-01-01", "1", profile.profile_id
    )
    them = UserAccount.create_account(
        "them@x.com", "pw", "Them", "1990-01-01", "2", profile.profile_id
    )
    _make_activity(title="Mine", owner_account_id=me.account_id).save_fundraising_activity()
    _make_activity(title="Theirs", owner_account_id=them.account_id).save_fundraising_activity()
    mine = FundraisingActivity.view_activities_by_owner(me.account_id)
    assert {x.title for x in mine} == {"Mine"}


def test_update_fundraiser_activity_persists_changes():
    activity = _make_activity(title="Before")
    activity.save_fundraising_activity()
    updated = _make_activity(title="After")
    updated.activity_id = activity.activity_id
    assert FundraisingActivity.update_fundraiser_activity(
        str(activity.activity_id), updated
    ) is True
    fetched = FundraisingActivity.view_fundraising_activity_details(
        str(activity.activity_id)
    )
    assert fetched is not None and fetched.title == "After"


def test_update_fundraiser_activity_returns_false_for_missing_id():
    dummy = _make_activity()
    assert FundraisingActivity.update_fundraiser_activity("99999", dummy) is False


def test_submit_search_criteria_matches_title_substring():
    _make_activity(title="Help Animals", category="community").save_fundraising_activity()
    _make_activity(title="Education for All", category="education").save_fundraising_activity()
    _make_activity(title="Medical Relief", category="medical").save_fundraising_activity()
    assert {a.title for a in FundraisingActivity.submit_search_criteria("animals")} == {"Help Animals"}
    assert {a.title for a in FundraisingActivity.submit_search_criteria("education")} == {"Education for All"}
    assert FundraisingActivity.submit_search_criteria("zzzzz") == []
