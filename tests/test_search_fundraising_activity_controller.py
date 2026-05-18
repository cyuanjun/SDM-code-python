"""Delegation tests for SearchFundraisingActivityController (US-20)."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.search_fundraising_activity_controller import (
    SearchFundraisingActivityController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_entity_list_unchanged() -> None:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    account = UserAccount.create_account(
        email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
        phone_num="0400000021", profile_id=profile.profile_id,
    )
    FundraisingActivity.create_fundraising_activity(
        title="Hospital fund", description="d",
        target_amount=Decimal("1"), fra_cat_id="cat_001",
        start_date=date(2026, 1, 1), end_date=date(2026, 1, 2),
        owner_account_id=account.account_id,
    )

    results = SearchFundraisingActivityController().search_fundraising_activity(
        "hospital"
    )

    assert [a.title for a in results] == ["Hospital fund"]


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Negative-path mirror: empty result forwarded unchanged."""
    monkeypatch.setattr(
        FundraisingActivity,
        "search_fundraising_activity",
        classmethod(lambda cls, search_criteria: []),
    )

    assert (
        SearchFundraisingActivityController().search_fundraising_activity(
            "anything"
        )
        == []
    )
