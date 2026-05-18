"""Delegation tests for SearchUserAccountController (US-10)."""
from __future__ import annotations

from datetime import date

import pytest

from controller.search_user_account_controller import (
    SearchUserAccountController,
)
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def test_controller_returns_entity_list_unchanged() -> None:
    profile = UserProfile.create_profile(role="admin", description="a")
    UserAccount.create_account(
        email="ada@x.com", password="p", name="Ada", dob=date(1990, 1, 1),
        phone_num="0400000019", profile_id=profile.profile_id,
    )

    results = SearchUserAccountController().search_user_account("ada")
    assert [a.email for a in results] == ["ada@x.com"]


def test_controller_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserAccount,
        "search_user_account",
        classmethod(lambda cls, search_criteria: []),
    )
    assert SearchUserAccountController().search_user_account("x") == []
