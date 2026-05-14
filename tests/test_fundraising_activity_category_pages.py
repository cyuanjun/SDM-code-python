"""Smoke + validation tests for the four Sprint 4 category boundary pages
(US-34, US-35 / US-38 reuse, US-36, US-37)."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.create_fundraising_activity_category_page import (
    CreateFundraisingActivityCategoryPage,
)
from boundary.update_fundraising_activity_category_page import (
    UpdateFundraisingActivityCategoryPage,
)
from boundary.view_fundraising_activity_categories_page import (
    ViewFundraisingActivityCategoriesPage,
)
from boundary.view_fundraising_activity_category_page import (
    ViewFundraisingActivityCategoryPage,
)


def test_pages_are_importable_and_have_render() -> None:
    for cls in (
        CreateFundraisingActivityCategoryPage,
        ViewFundraisingActivityCategoryPage,
        UpdateFundraisingActivityCategoryPage,
        ViewFundraisingActivityCategoriesPage,
    ):
        assert callable(cls().render)


def test_create_validation_accepts_well_formed_input() -> None:
    assert (
        CreateFundraisingActivityCategoryPage.validate_category("Health", "x")
        is True
    )


def test_create_validation_rejects_blank() -> None:
    assert (
        CreateFundraisingActivityCategoryPage.validate_category("", "x")
        is False
    )
    assert (
        CreateFundraisingActivityCategoryPage.validate_category("x", "")
        is False
    )


def test_update_validation_accepts_well_formed_input() -> None:
    assert (
        UpdateFundraisingActivityCategoryPage.validate_category("Health", "x")
        is True
    )


def test_update_validation_rejects_blank() -> None:
    assert (
        UpdateFundraisingActivityCategoryPage.validate_category("", "x")
        is False
    )


def test_search_validation_rejects_blank() -> None:
    assert ViewFundraisingActivityCategoriesPage.validate_criteria("") is False


def test_create_page_render_does_not_raise() -> None:
    script = """
from boundary.create_fundraising_activity_category_page import CreateFundraisingActivityCategoryPage
CreateFundraisingActivityCategoryPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_view_page_render_does_not_raise_when_empty() -> None:
    script = """
from boundary.view_fundraising_activity_category_page import ViewFundraisingActivityCategoryPage
ViewFundraisingActivityCategoryPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_view_page_render_does_not_raise_with_categories() -> None:
    script = """
from entity.fundraising_activity_category import FundraisingActivityCategory
from boundary.view_fundraising_activity_category_page import ViewFundraisingActivityCategoryPage
FundraisingActivityCategory.create_category("Health", "medical")
ViewFundraisingActivityCategoryPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_update_page_render_does_not_raise_when_empty() -> None:
    script = """
from boundary.update_fundraising_activity_category_page import UpdateFundraisingActivityCategoryPage
UpdateFundraisingActivityCategoryPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_search_page_render_does_not_raise() -> None:
    script = """
from boundary.view_fundraising_activity_categories_page import ViewFundraisingActivityCategoriesPage
ViewFundraisingActivityCategoriesPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
