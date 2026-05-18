"""CreateFundraisingActivityCategoryController <<Controller>>."""
from __future__ import annotations

from typing import Optional

from entity.fundraising_activity_category import FundraisingActivityCategory


class CreateFundraisingActivityCategoryController:
    def create_category(
        self, category_name: str, description: str
    ) -> Optional[FundraisingActivityCategory]:
        return FundraisingActivityCategory.create_category(
            category_name=category_name, description=description
        )
