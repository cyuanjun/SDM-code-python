"""ViewFundraisingActivityCategoryController <<Controller>>."""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity_category import FundraisingActivityCategory


class ViewFundraisingActivityCategoryController:
    def view_fundraising_activity_category(
        self, fra_cat_id: str
    ) -> Optional[FundraisingActivityCategory]:
        return FundraisingActivityCategory.view_fundraising_activity_category(
            fra_cat_id
        )

    def view_all_categories(self) -> list[FundraisingActivityCategory]:
        return FundraisingActivityCategory.view_all_categories()
