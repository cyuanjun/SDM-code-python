"""Sprint 4 — FundraisingActivityCategory entity tests (US-34..US-38).

Diagram-as-contract notes (see docs/todo.md "Sprint 4 naming deviations" and
"Sprint 4 diagram typos"):
- Method names use the full-word `fundraising_activity_category` form instead
  of the diagram's `FRACategory` shorthand, to match Sprint 1–3 conventions
  (e.g. `suspend_fundraising_activity`).
- `submit_search_criteria` is used in place of the diagram's
  `submitSeachCriteria` (typo) — same name already in use on
  `FundraisingActivity` and `UserProfile`.
"""
from entity.fundraising_activity_category import FundraisingActivityCategory


def test_create_category_persists_record():
    ok = FundraisingActivityCategory.create_category("medical", "Medical emergencies")
    assert ok is True
    rows = FundraisingActivityCategory.view_all_categories()
    assert {r.category_name for r in rows} == {"medical"}


def test_create_category_returns_false_on_duplicate_name():
    assert FundraisingActivityCategory.create_category("medical", "first") is True
    assert FundraisingActivityCategory.create_category("medical", "duplicate") is False


def test_view_fundraising_activity_category_returns_record_by_id():
    FundraisingActivityCategory.create_category("education", "Schools")
    created = FundraisingActivityCategory.view_all_categories()[0]
    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        created.category_id
    )
    assert fetched is not None
    assert fetched.category_name == "education"
    assert fetched.description == "Schools"
    assert fetched.status == "active"


def test_view_fundraising_activity_category_returns_none_for_missing_id():
    assert FundraisingActivityCategory.view_fundraising_activity_category(99999) is None


def test_view_all_categories_returns_every_row():
    FundraisingActivityCategory.create_category("medical", "Medical")
    FundraisingActivityCategory.create_category("community", "Community")
    rows = FundraisingActivityCategory.view_all_categories()
    assert {r.category_name for r in rows} == {"medical", "community"}


def test_view_all_categories_returns_empty_when_no_rows():
    assert FundraisingActivityCategory.view_all_categories() == []


def test_update_fundraising_activity_category_persists_changes():
    FundraisingActivityCategory.create_category("medical", "Medical")
    created = FundraisingActivityCategory.view_all_categories()[0]
    updated = FundraisingActivityCategory(
        category_id=created.category_id,
        category_name="medical_emergency",
        description="Urgent medical needs",
        status="active",
    )
    assert (
        FundraisingActivityCategory.update_fundraising_activity_category(
            created.category_id, updated
        )
        is True
    )
    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        created.category_id
    )
    assert fetched.category_name == "medical_emergency"
    assert fetched.description == "Urgent medical needs"


def test_update_fundraising_activity_category_returns_false_for_missing_id():
    dummy = FundraisingActivityCategory(
        category_id=99999, category_name="x", description="x", status="active"
    )
    assert (
        FundraisingActivityCategory.update_fundraising_activity_category(99999, dummy)
        is False
    )


def test_submit_search_criteria_matches_name_or_description():
    FundraisingActivityCategory.create_category("medical", "Medical emergencies")
    FundraisingActivityCategory.create_category("education", "Schools and tuition")
    FundraisingActivityCategory.create_category("community", "Local neighbourhood")

    assert {r.category_name for r in FundraisingActivityCategory.submit_search_criteria("medical")} == {"medical"}
    assert {r.category_name for r in FundraisingActivityCategory.submit_search_criteria("schools")} == {"education"}
    assert FundraisingActivityCategory.submit_search_criteria("zzzz") == []


def test_suspend_fundraising_activity_category_marks_suspended():
    FundraisingActivityCategory.create_category("medical", "Medical")
    created = FundraisingActivityCategory.view_all_categories()[0]
    assert (
        FundraisingActivityCategory.suspend_fundraising_activity_category(
            created.category_id
        )
        is True
    )
    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        created.category_id
    )
    assert fetched.status == "suspended"


def test_suspend_fundraising_activity_category_returns_false_for_missing_id():
    assert (
        FundraisingActivityCategory.suspend_fundraising_activity_category(99999)
        is False
    )
