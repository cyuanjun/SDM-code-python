"""Tests for the FundraisingActivityCategory entity (US-34..US-38).

Diagram contracts:
    US-34: createCategory(categoryName, description): FundraisingActivityCategory
    US-35: viewFundraisingActivityCategory(FRACatId): FundraisingActivityCategory
    US-36: updateFundraisingActivityCategory(FRACatId, updatedFRACategory): Boolean
    US-37: searchFundraisingActivityCategory(searchCriteria): List<FundraisingActivityCategory>
    US-38: suspendFundraisingActivityCategory(FRACatId): Boolean
"""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


def test_create_category_persists_and_returns_with_prefixed_id() -> None:
    cat = FundraisingActivityCategory.create_category(
        category_name="TC - Health",
        description="TC scenario active category",
    )

    assert cat.fra_cat_id == "cat_001"
    assert cat.category_name == "TC - Health"
    assert cat.description == "TC scenario active category"
    assert cat.suspended is False


def test_create_category_assigns_sequential_ids() -> None:
    first = FundraisingActivityCategory.create_category(
        category_name="Health", description="a"
    )
    second = FundraisingActivityCategory.create_category(
        category_name="Education", description="b"
    )
    assert first.fra_cat_id == "cat_001"
    assert second.fra_cat_id == "cat_002"


def test_create_category_defaults_suspended_to_false() -> None:
    """Negative path: suspended not in the signature; defaults to False."""
    cat = FundraisingActivityCategory.create_category(
        category_name="X", description=""
    )
    assert cat.suspended is False


def test_create_category_returns_none_for_duplicate_name() -> None:
    """Negative path: category_name is UNIQUE per the schema. A second
    create with the same name must return None rather than persist a
    duplicate."""
    first = FundraisingActivityCategory.create_category(
        category_name="TC - Health", description="primary"
    )
    second = FundraisingActivityCategory.create_category(
        category_name="TC - Health", description="duplicate"
    )

    assert first is not None
    assert second is None


def test_update_fra_category_returns_false_for_duplicate_name() -> None:
    """Negative path: updating one category's name to a name already
    taken by another category must return False (UNIQUE constraint)."""
    health = FundraisingActivityCategory.create_category(
        category_name="TC - Health", description="a"
    )
    education = FundraisingActivityCategory.create_category(
        category_name="TC - Education", description="b"
    )
    assert health is not None and education is not None

    ok = FundraisingActivityCategory.update_fundraising_activity_category(
        education.fra_cat_id,
        category_name="TC - Health",
        description="b",
    )
    assert ok is False
    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        education.fra_cat_id
    )
    assert fetched is not None and fetched.category_name == "TC - Education"


def test_view_fundraising_activity_category_returns_for_existing_id() -> None:
    created = FundraisingActivityCategory.create_category(
        category_name="TC - Health", description="TC scenario active category"
    )

    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        created.fra_cat_id
    )
    assert fetched is not None
    assert fetched.category_name == "TC - Health"


def test_view_fundraising_activity_category_returns_none_for_missing_id() -> None:
    """Negative path."""
    assert (
        FundraisingActivityCategory.view_fundraising_activity_category(
            "cat_999"
        )
        is None
    )


def test_update_fra_category_returns_true_and_persists_changes() -> None:
    created = FundraisingActivityCategory.create_category(
        category_name="TC - Health", description="initial"
    )

    ok = FundraisingActivityCategory.update_fundraising_activity_category(
        fra_cat_id=created.fra_cat_id,
        category_name="TC - Health (renamed)",
        description="revised description",
    )
    assert ok is True

    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        created.fra_cat_id
    )
    assert fetched is not None
    assert fetched.category_name == "TC - Health (renamed)"
    assert fetched.description == "revised description"
    # suspended is not updatable via this method any more (per the flattened
    # 2026-05-18 signature) — defaults from create stay in place.
    assert fetched.suspended is False


def test_update_fra_category_returns_false_for_missing_id() -> None:
    assert (
        FundraisingActivityCategory.update_fundraising_activity_category(
            fra_cat_id="cat_999",
            category_name="x",
            description="y",
        )
        is False
    )


def test_search_fra_category_matches_name_substring_case_insensitive() -> None:
    FundraisingActivityCategory.create_category("TC - Health", "TC scenario active category")
    FundraisingActivityCategory.create_category("TC - Education", "TC scenario active category")
    FundraisingActivityCategory.create_category("TC - Sports", "TC scenario suspended category")

    results = (
        FundraisingActivityCategory.search_fundraising_activity_category(
            "TC - "
        )
    )
    assert [c.category_name for c in results] == [
        "TC - Health", "TC - Education", "TC - Sports",
    ]


def test_search_fra_category_matches_description() -> None:
    FundraisingActivityCategory.create_category("A", "medical")
    FundraisingActivityCategory.create_category("B", "schooling")

    results = (
        FundraisingActivityCategory.search_fundraising_activity_category(
            "school"
        )
    )
    assert [c.category_name for c in results] == ["B"]


def test_search_fra_category_returns_empty_for_no_match() -> None:
    """Negative path."""
    FundraisingActivityCategory.create_category("TC - Health", "a")
    assert (
        FundraisingActivityCategory.search_fundraising_activity_category(
            "zzz-no-match"
        )
        == []
    )


def test_suspend_fra_category_returns_true_and_sets_flag() -> None:
    created = FundraisingActivityCategory.create_category("TC - Health", "a")
    assert created.suspended is False

    assert (
        FundraisingActivityCategory.suspend_fundraising_activity_category(
            created.fra_cat_id
        )
        is True
    )
    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        created.fra_cat_id
    )
    assert fetched is not None
    assert fetched.suspended is True


def test_suspend_fra_category_returns_false_for_missing_id() -> None:
    assert (
        FundraisingActivityCategory.suspend_fundraising_activity_category(
            "cat_999"
        )
        is False
    )


def test_view_all_categories_returns_empty_on_empty_db() -> None:
    """Exception A: list-all for the boundary picker."""
    assert FundraisingActivityCategory.view_all_categories() == []


def test_view_all_categories_returns_all_in_insertion_order() -> None:
    FundraisingActivityCategory.create_category("Health", "a")
    FundraisingActivityCategory.create_category("Education", "b")
    FundraisingActivityCategory.create_category("Animals", "c")

    cats = FundraisingActivityCategory.view_all_categories()
    assert [c.category_name for c in cats] == ["Health", "Education", "Animals"]
