"""ViewMyDonationHistoriesController <<Controller>>."""
from __future__ import annotations

from entity.donation import Donation


class ViewMyDonationHistoriesController:
    def view_my_donation_histories(self, account_id: str) -> list[Donation]:
        return Donation.view_my_donation_histories(account_id=account_id)
