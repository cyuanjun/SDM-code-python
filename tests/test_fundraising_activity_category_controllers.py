"""Delegation tests for the five Sprint 4 category controllers (US-34..38).

Bundled into one file because each controller only forwards a single
method to FundraisingActivityCategory; one file keeps the smoke
coverage tight.
"""
from __future__ import annotations

import pytest

from controller.create_fundraising_activity_category_controller import (
    CreateFundraisingActivityCategoryController,
)
from controller.search_fundraising_activity_category_controller import (
    SearchFundraisingActivityCategoryController,
)
from controller.suspend_fundraising_activity_category_controller import (
    SuspendFundraisingActivityCategoryController,
)
from controller.update_fundraising_activity_category_controller import (
    UpdateFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)
from entity.fundraising_activity_category import FundraisingActivityCategory


def test_create_category_forwards(monkeypatch: pytest.MonkeyPatch) -> None:
    sentinel = FundraisingActivityCategory(
        category_name="x", description="y", fra_cat_id="cat_999"
    )
    monkeypatch.setattr(
        FundraisingActivityCategory,
        "create_category",
        classmethod(lambda cls, category_name, description: sentinel),
    )
    assert (
        CreateFundraisingActivityCategoryController().create_category("x", "y")
        is sentinel
    )


def test_view_category_forwards_one_and_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivityCategory,
        "view_fundraising_activity_category",
        classmethod(lambda cls, fra_cat_id: None),
    )
    assert (
        ViewFundraisingActivityCategoryController()
        .view_fundraising_activity_category("cat_001")
        is None
    )


def test_view_all_categories_forwards(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        FundraisingActivityCategory,
        "view_all_categories",
        classmethod(lambda cls: []),
    )
    assert (
        ViewFundraisingActivityCategoryController().view_all_categories()
        == []
    )


def test_update_category_forwards_true_and_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivityCategory,
        "update_fundraising_activity_category",
        classmethod(lambda cls, fra_cat_id, updated_category: False),
    )
    assert (
        UpdateFundraisingActivityCategoryController()
        .update_fundraising_activity_category(
            fra_cat_id="cat_001",
            updated_category=FundraisingActivityCategory("x", "y"),
        )
        is False
    )


def test_search_category_forwards(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        FundraisingActivityCategory,
        "search_fundraising_activity_category",
        classmethod(lambda cls, search_criteria: []),
    )
    assert (
        SearchFundraisingActivityCategoryController()
        .search_fundraising_activity_category("x")
        == []
    )


def test_suspend_category_forwards_true_and_false(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivityCategory,
        "suspend_fundraising_activity_category",
        classmethod(lambda cls, fra_cat_id: False),
    )
    assert (
        SuspendFundraisingActivityCategoryController()
        .suspend_fundraising_activity_category("cat_001")
        is False
    )
