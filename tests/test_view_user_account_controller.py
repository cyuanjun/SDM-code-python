"""Delegation tests for ViewUserAccountController (US-7 + Exception A)."""
from __future__ import annotations

from datetime import date

import pytest

from controller.view_user_account_controller import ViewUserAccountController
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_account() -> UserAccount:
    profile = UserProfile.create_profile(role="admin", description="a")
    return UserAccount.create_account(
        email="a@x.com", password="p", name="A", dob=date(1990, 1, 1),
        phone_num="0400000017", profile_id=profile.profile_id,
    )


def test_view_user_account_returns_account_when_entity_returns_one() -> None:
    created = _seed_account()

    result = ViewUserAccountController().view_user_account(created.account_id)

    assert isinstance(result, UserAccount)
    assert result.account_id == created.account_id


def test_view_user_account_returns_none_when_entity_returns_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserAccount,
        "view_user_account",
        classmethod(lambda cls, account_id: None),
    )

    assert ViewUserAccountController().view_user_account("anything") is None


def test_view_all_user_accounts_returns_entity_list_unchanged() -> None:
    _seed_account()

    accounts = ViewUserAccountController().view_all_user_accounts()

    assert [a.account_id for a in accounts] == ["acc_001"]


def test_view_all_user_accounts_returns_empty_list_when_entity_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserAccount,
        "view_all_user_accounts",
        classmethod(lambda cls: []),
    )

    assert ViewUserAccountController().view_all_user_accounts() == []
