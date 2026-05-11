"""ViewFundraisingActivityCategoryController <<Controller>> — pure delegator, US-35.

Also exposes view_all_categories() for the category-list helper used by other
pages (Exception A in CLAUDE.md). Logged in docs/todo.md.
"""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity_category import FundraisingActivityCategory


class ViewFundraisingActivityCategoryController:
    def view_fundraising_activity_category(
        self, category_id: int
    ) -> Optional[FundraisingActivityCategory]:
        return FundraisingActivityCategory.view_fundraising_activity_category(
            category_id
        )

    def view_all_categories(self) -> list[FundraisingActivityCategory]:
        return FundraisingActivityCategory.view_all_categories()
