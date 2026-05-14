"""ViewMyDonationHistoryController <<Controller>> — Sprint 3 US-33.

Pure delegator. Hosts view_my_donation_history (per US-33 diagram) and
view_my_donations (Exception A) so the boundary can show a picker.
"""
from __future__ import annotations

from typing import Optional

from entity.donation import Donation


class ViewMyDonationHistoryController:
    def view_my_donation_history(
        self, account_id: str, donation_id: str
    ) -> Optional[Donation]:
        return Donation.view_my_donation_history(
            account_id=account_id, donation_id=donation_id
        )

    def view_my_donations(self, account_id: str) -> list[Donation]:
        return Donation.view_my_donations(account_id=account_id)
