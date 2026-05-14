"""CreateFundraisingActivityCategoryController — Sprint 4 US-34. Pure delegator."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class CreateFundraisingActivityCategoryController:
    def create_category(
        self, category_name: str, description: str
    ) -> FundraisingActivityCategory:
        return FundraisingActivityCategory.create_category(
            category_name=category_name, description=description
        )
