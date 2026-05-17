"""UpdateFundraisingActivityCategoryController — Sprint 4 US-36. Pure delegator.

Signature flattened 2026-05-18 per the new US-36 diagram — takes
(fra_cat_id, category_name, description) directly rather than a wrapping
entity object.
"""
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
