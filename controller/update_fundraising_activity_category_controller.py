"""UpdateFundraisingActivityCategoryController <<Controller>> — pure delegator, US-36."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class UpdateFundraisingActivityCategoryController:
    def update_fundraising_activity_category(
        self,
        category_id: int,
        updated_category: FundraisingActivityCategory,
    ) -> bool:
        return FundraisingActivityCategory.update_fundraising_activity_category(
            category_id, updated_category
        )
