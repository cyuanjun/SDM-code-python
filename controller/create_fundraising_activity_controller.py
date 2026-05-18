"""CreateFundraisingActivityController <<Controller>>."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from entity.fundraising_activity import FundraisingActivity


class CreateFundraisingActivityController:
    def create_fundraising_activity(
        self,
        title: str,
        description: str,
        target_amount: Decimal,
        fra_cat_id: str,
        start_date: date,
        end_date: date,
        owner_account_id: str,
    ) -> FundraisingActivity:
        return FundraisingActivity.create_fundraising_activity(
            title=title,
            description=description,
            target_amount=target_amount,
            fra_cat_id=fra_cat_id,
            start_date=start_date,
            end_date=end_date,
            owner_account_id=owner_account_id,
        )
