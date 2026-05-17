"""ViewMyDonationHistoriesController <<Controller>> — Sprint 3 US-33.

Pure delegator. Re-shaped 2026-05-18: was ViewMyDonationHistoryController
hosting a per-id `view_my_donation_history` + an Exception A list. The
new US-33 diagram folds these into a single diagram-defined list method.
"""
from __future__ import annotations

from entity.donation import Donation


class ViewMyDonationHistoriesController:
    def view_my_donation_histories(self, account_id: str) -> list[Donation]:
        return Donation.view_my_donation_histories(account_id=account_id)
