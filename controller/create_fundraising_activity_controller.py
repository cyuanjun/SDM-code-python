"""CreateFundraisingActivityController <<Controller>> — pure delegator, see Sprint 1 diagram US-13."""
from __future__ import annotations

from datetime import date

from entity.fundraising_activity import FundraisingActivity


class CreateFundraisingActivityController:
    def create_fundraising_activity(
        self,
        title: str,
        description: str,
        target_amount: float,
        category: str,
        start_date: date,
        end_date: date,
        owner_email: str | None = None,
    ) -> bool:
        activity = FundraisingActivity(
            title=title,
            description=description,
            target_amount=target_amount,
            category=category,
            start_date=start_date.isoformat() if hasattr(start_date, "isoformat") else str(start_date),
            end_date=end_date.isoformat() if hasattr(end_date, "isoformat") else str(end_date),
            status="active",
            owner_email=owner_email,
        )
        return activity.save_fundraising_activity()
