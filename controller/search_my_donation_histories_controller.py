"""SearchMyDonationHistoriesController <<Controller>>."""
from __future__ import annotations

from entity.donation import Donation


class SearchMyDonationHistoriesController:
    def search_my_donation_history(
        self, account_id: str, search_criteria: str
    ) -> list[Donation]:
        return Donation.search_my_donation_history(
            account_id=account_id, search_criteria=search_criteria
        )
