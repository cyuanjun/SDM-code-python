"""SuspendFundraisingActivityCategoryController <<Controller>> — pure delegator, US-38."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class SuspendFundraisingActivityCategoryController:
    def suspend_fundraising_activity_category(self, category_id: int) -> bool:
        return FundraisingActivityCategory.suspend_fundraising_activity_category(
            category_id
        )
