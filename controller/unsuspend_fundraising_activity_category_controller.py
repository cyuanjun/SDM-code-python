"""UnsuspendFundraisingActivityCategoryController — Exception A (UX).
Pure delegator."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class UnsuspendFundraisingActivityCategoryController:
    def unsuspend_fundraising_activity_category(self, fra_cat_id: str) -> bool:
        return (
            FundraisingActivityCategory
            .unsuspend_fundraising_activity_category(fra_cat_id)
        )
