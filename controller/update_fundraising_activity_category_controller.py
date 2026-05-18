"""UpdateFundraisingActivityCategoryController <<Controller>>."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class UpdateFundraisingActivityCategoryController:
    def update_fundraising_activity_category(
        self,
        fra_cat_id: str,
        category_name: str,
        description: str,
    ) -> bool:
        return FundraisingActivityCategory.update_fundraising_activity_category(
            fra_cat_id=fra_cat_id,
            category_name=category_name,
            description=description,
        )
