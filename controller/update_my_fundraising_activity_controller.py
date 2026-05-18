"""UpdateMyFundraisingActivityController <<Controller>>."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

from entity.fundraising_activity import FundraisingActivity


class UpdateMyFundraisingActivityController:
    def update_my_fundraising_activity(
        self,
        owner_account_id: str,
        fra_id: str,
        title: str,
        description: str,
        target_amount: Decimal,
        fra_cat_id: str,
        start_date: date,
        end_date: date,
    ) -> bool:
        return FundraisingActivity.update_my_fundraising_activity(
            owner_account_id=owner_account_id,
            fra_id=fra_id,
            title=title,
            description=description,
            target_amount=target_amount,
            fra_cat_id=fra_cat_id,
            start_date=start_date,
            end_date=end_date,
        )
