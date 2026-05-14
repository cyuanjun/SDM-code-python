"""UpdateFundraisingActivityCategoryController — Sprint 4 US-36. Pure delegator."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class UpdateFundraisingActivityCategoryController:
    def update_fundraising_activity_category(
        self,
        fra_cat_id: str,
        updated_category: FundraisingActivityCategory,
    ) -> bool:
        return FundraisingActivityCategory.update_fundraising_activity_category(
            fra_cat_id=fra_cat_id, updated_category=updated_category
        )
