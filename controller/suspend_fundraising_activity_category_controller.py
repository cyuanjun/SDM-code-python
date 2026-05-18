"""SuspendFundraisingActivityCategoryController <<Controller>>."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class SuspendFundraisingActivityCategoryController:
    def suspend_fundraising_activity_category(self, fra_cat_id: str) -> bool:
        return FundraisingActivityCategory.suspend_fundraising_activity_category(
            fra_cat_id
        )
