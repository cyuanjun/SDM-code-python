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
