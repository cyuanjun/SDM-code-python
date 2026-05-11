"""CreateFundraisingActivityCategoryController <<Controller>> — pure delegator, US-34."""
from __future__ import annotations

from entity.fundraising_activity_category import FundraisingActivityCategory


class CreateFundraisingActivityCategoryController:
    def create_category(self, category_name: str, description: str) -> bool:
        return FundraisingActivityCategory.create_category(category_name, description)
