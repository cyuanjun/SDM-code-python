"""SearchDonationHistoryController <<Controller>> — Sprint 3 US-32.

Pure delegator.
"""
from __future__ import annotations

from entity.donation import Donation


class SearchDonationHistoryController:
    def search_donation_history(
        self, search_criteria: str, account_id: str
    ) -> list[Donation]:
        return Donation.search_donation_history(
            search_criteria=search_criteria, account_id=account_id
        )
