"""Tests for the UserAccount entity (US-6).

Diagram contract (US-06.jpg):
    createAccount(
        email: String, password: String, name: String, DOB: Date,
        phoneNum: String, profileId: String,
    ): UserAccount

`profileId` is the prefixed string form (`prof_NNN`); the entity parses
it back to the underlying INTEGER FK on the way in.
"""
from __future__ import annotations

from datetime import date

import pytest

from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_profile(role: str = "admin", description: str = "Full access") -> UserProfile:
    return UserProfile.create_profile(role=role, description=description)


def test_create_account_persists_and_returns_account_with_prefixed_id() -> None:
    profile = _seed_profile()

    account = UserAccount.create_account(
        email="ada@example.com",
        password="hunter2",
        name="Ada",
        dob=date(1990, 1, 15),
        phone_num="0400000000",
        profile_id=profile.profile_id,
    )

    assert account.account_id == "acc_001"
    assert account.email == "ada@example.com"
    assert account.password == "hunter2"
    assert account.name == "Ada"
    assert account.dob == date(1990, 1, 15)
    assert account.phone_num == "0400000000"
    assert account.profile_id == profile.profile_id
    assert account.suspended is False


def test_create_account_assigns_sequential_ids() -> None:
    profile = _seed_profile()

    first = UserAccount.create_account(
        email="a@x.com", password="p", name="A", dob=date(2000, 1, 1),
        phone_num="1", profile_id=profile.profile_id,
    )
    second = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(2000, 1, 1),
        phone_num="2", profile_id=profile.profile_id,
    )

    assert first.account_id == "acc_001"
    assert second.account_id == "acc_002"


def test_create_account_links_to_profile_via_foreign_key() -> None:
    profile = _seed_profile(role="fundraiser", description="Runs campaigns")

    account = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1995, 6, 6),
        phone_num="0", profile_id=profile.profile_id,
    )

    assert account.profile_id == profile.profile_id


def test_create_account_raises_on_nonexistent_profile_id() -> None:
    """Negative path: profile_id is a FK to user_profile.profile_id. Passing
    a profileId that doesn't reference an existing row must fail loudly.
    SQLite raises sqlite3.IntegrityError under PRAGMA foreign_keys = ON."""
    import sqlite3

    with pytest.raises(sqlite3.IntegrityError):
        UserAccount.create_account(
            email="ghost@x.com", password="p", name="Ghost",
            dob=date(2000, 1, 1), phone_num="0", profile_id="prof_999",
        )


def test_create_account_allows_duplicate_emails() -> None:
    """Negative path: the diagram does not declare email as unique. Two
    accounts with the same email both persist with distinct account_ids.
    Logged as an architectural concern — login will need to handle this."""
    profile = _seed_profile()

    first = UserAccount.create_account(
        email="dup@x.com", password="p1", name="A", dob=date(2000, 1, 1),
        phone_num="1", profile_id=profile.profile_id,
    )
    second = UserAccount.create_account(
        email="dup@x.com", password="p2", name="B", dob=date(2000, 1, 1),
        phone_num="2", profile_id=profile.profile_id,
    )

    assert first.account_id != second.account_id
    assert first.email == second.email


def _seed_account(
    email: str = "ada@x.com",
    password: str = "hunter2",
    profile: UserProfile | None = None,
) -> UserAccount:
    return UserAccount.create_account(
        email=email,
        password=password,
        name="Ada",
        dob=date(1990, 1, 15),
        phone_num="0400000000",
        profile_id=(profile or _seed_profile()).profile_id,
    )


def test_login_returns_user_account_on_matching_credentials() -> None:
    _seed_account()

    account = UserAccount.login("ada@x.com", "hunter2")

    assert account is not None
    assert account.email == "ada@x.com"
    assert account.account_id == "acc_001"
    assert account.profile_id == "prof_001"


def test_login_returns_none_when_email_does_not_match() -> None:
    _seed_account()

    assert UserAccount.login("nobody@x.com", "hunter2") is None


def test_login_returns_none_when_password_does_not_match() -> None:
    _seed_account()

    assert UserAccount.login("ada@x.com", "wrong-password") is None


def test_login_returns_none_when_database_is_empty() -> None:
    """Negative path: login against an empty user_account table returns
    None, never crashes."""
    assert UserAccount.login("anyone@x.com", "anything") is None


def test_view_user_account_returns_account_for_existing_id() -> None:
    created = _seed_account()

    fetched = UserAccount.view_user_account(created.account_id)

    assert fetched is not None
    assert fetched.account_id == created.account_id
    assert fetched.email == created.email
    assert fetched.name == created.name
    assert fetched.profile_id == created.profile_id


def test_view_user_account_returns_none_for_missing_id() -> None:
    """Negative path: id with the right prefix but no matching row."""
    assert UserAccount.view_user_account("acc_999") is None


def test_view_all_user_accounts_returns_empty_list_when_none_exist() -> None:
    """Negative path: caller gets [] back, not None."""
    assert UserAccount.view_all_user_accounts() == []


def test_view_all_user_accounts_returns_all_in_insertion_order() -> None:
    profile = _seed_profile()
    UserAccount.create_account(
        email="a@x.com", password="p", name="A", dob=date(1990, 1, 1),
        phone_num="1", profile_id=profile.profile_id,
    )
    UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1990, 1, 1),
        phone_num="2", profile_id=profile.profile_id,
    )
    UserAccount.create_account(
        email="c@x.com", password="p", name="C", dob=date(1990, 1, 1),
        phone_num="3", profile_id=profile.profile_id,
    )

    accounts = UserAccount.view_all_user_accounts()

    assert [a.account_id for a in accounts] == ["acc_001", "acc_002", "acc_003"]
    assert [a.email for a in accounts] == ["a@x.com", "b@x.com", "c@x.com"]


def test_update_user_account_returns_true_on_success_and_persists_changes() -> None:
    profile = _seed_profile()
    created = _seed_account(profile=profile)

    updated = UserAccount(
        email="ada-new@x.com",
        password="new-secret",
        name="Ada (renamed)",
        dob=date(1985, 6, 6),
        phone_num="0411111111",
        profile_id=profile.profile_id,
        suspended=True,
    )
    assert UserAccount.update_user_account(created.account_id, updated) is True

    fetched = UserAccount.view_user_account(created.account_id)
    assert fetched is not None
    assert fetched.email == "ada-new@x.com"
    assert fetched.name == "Ada (renamed)"
    assert fetched.dob == date(1985, 6, 6)
    assert fetched.phone_num == "0411111111"
    assert fetched.suspended is True


def test_update_user_account_returns_false_for_missing_id() -> None:
    """Negative path: no row matches account_id."""
    updated = UserAccount(
        email="x@x.com", password="p", name="X", dob=date(2000, 1, 1),
        phone_num="0", profile_id="prof_001",
    )
    assert UserAccount.update_user_account("acc_999", updated) is False


def test_update_user_account_does_not_mutate_other_rows() -> None:
    profile = _seed_profile()
    first = _seed_account(email="a@x.com", profile=profile)
    second = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1990, 1, 1),
        phone_num="2", profile_id=profile.profile_id,
    )

    updated = UserAccount(
        email="renamed@x.com", password="p", name="renamed",
        dob=date(1990, 1, 1), phone_num="9",
        profile_id=profile.profile_id,
    )
    UserAccount.update_user_account(first.account_id, updated)

    untouched = UserAccount.view_user_account(second.account_id)
    assert untouched is not None
    assert untouched.email == "b@x.com"
    assert untouched.name == "B"
