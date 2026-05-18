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

from data.seed import (
    DEFAULT_PASSWORD,
    TC_ADMIN_EMAIL,
    TC_ADMIN_PHONE,
    TC_DONEE_EMAIL,
    TC_DONEE_PHONE,
    TC_FUNDRAISER_EMAIL,
    TC_FUNDRAISER_PHONE,
)
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _seed_profile(role: str = "admin", description: str = "Full access") -> UserProfile:
    return UserProfile.create_profile(role=role, description=description)


def test_create_account_persists_and_returns_account_with_prefixed_id() -> None:
    profile = _seed_profile()

    account = UserAccount.create_account(
        email=TC_ADMIN_EMAIL,
        password=DEFAULT_PASSWORD,
        name="TC - Admin",
        dob=date(2000, 1, 1),
        phone_num=TC_ADMIN_PHONE,
        profile_id=profile.profile_id,
    )

    assert account.account_id == "acc_001"
    assert account.email == TC_ADMIN_EMAIL
    assert account.password == DEFAULT_PASSWORD
    assert account.name == "TC - Admin"
    assert account.dob == date(2000, 1, 1)
    assert account.phone_num == TC_ADMIN_PHONE
    assert account.profile_id == profile.profile_id
    assert account.suspended is False


def test_create_account_assigns_sequential_ids() -> None:
    profile = _seed_profile()

    first = UserAccount.create_account(
        email="a@x.com", password="p", name="A", dob=date(2000, 1, 1),
        phone_num="0400000053", profile_id=profile.profile_id,
    )
    second = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(2000, 1, 1),
        phone_num="0400000057", profile_id=profile.profile_id,
    )

    assert first.account_id == "acc_001"
    assert second.account_id == "acc_002"


def test_create_account_links_to_profile_via_foreign_key() -> None:
    profile = _seed_profile(role="fundraiser", description="Runs campaigns")

    account = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1995, 6, 6),
        phone_num="0400000069", profile_id=profile.profile_id,
    )

    assert account.profile_id == profile.profile_id


def test_create_account_returns_none_for_nonexistent_profile_id() -> None:
    """Negative path: profile_id is a FK to user_profile.profile_id. Passing
    a profileId that doesn't reference an existing row trips PRAGMA
    foreign_keys = ON, and create_account catches the IntegrityError and
    returns None (same contract as the duplicate-email path)."""
    result = UserAccount.create_account(
        email="ghost@x.com", password="p", name="Ghost",
        dob=date(2000, 1, 1), phone_num="0400000082", profile_id="prof_999",
    )

    assert result is None


def test_create_account_returns_none_for_duplicate_email() -> None:
    """Negative path: email is UNIQUE (lecturer instruction 2026-05-15).
    create_account returns None on conflict and the second row is rejected."""
    profile = _seed_profile()

    first = UserAccount.create_account(
        email=TC_FUNDRAISER_EMAIL, password=DEFAULT_PASSWORD, name="TC - Fundraiser",
        dob=date(2000, 1, 1), phone_num=TC_FUNDRAISER_PHONE,
        profile_id=profile.profile_id,
    )
    second = UserAccount.create_account(
        email=TC_FUNDRAISER_EMAIL, password=DEFAULT_PASSWORD, name="Other",
        dob=date(2000, 1, 1), phone_num="0411111111",
        profile_id=profile.profile_id,
    )

    assert first is not None
    assert second is None
    assert UserAccount.view_user_account(first.account_id) is not None


def test_create_account_returns_none_for_duplicate_phone_num() -> None:
    """Negative path: phone_num is UNIQUE (added 2026-05-18).
    create_account returns None on conflict and the second row is rejected."""
    profile = _seed_profile()

    first = UserAccount.create_account(
        email="a@x.com", password="p1", name="A", dob=date(2000, 1, 1),
        phone_num="0411222333", profile_id=profile.profile_id,
    )
    second = UserAccount.create_account(
        email="b@x.com", password="p2", name="B", dob=date(2000, 1, 1),
        phone_num="0411222333", profile_id=profile.profile_id,
    )

    assert first is not None
    assert second is None
    assert UserAccount.view_user_account(first.account_id) is not None


def test_update_user_account_returns_false_for_duplicate_phone_num() -> None:
    """Negative path: changing phone to one already used by a different
    account hits the UNIQUE constraint; update_user_account returns False
    and the row is unchanged."""
    profile = _seed_profile()
    first = _seed_account(email="a@x.com", profile=profile)
    second = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1990, 1, 1),
        phone_num="0411222333", profile_id=profile.profile_id,
    )
    assert second is not None

    clashing = UserAccount(
        email="b@x.com", password="p", name="B-renamed",
        dob=date(1990, 1, 1), phone_num=first.phone_num,
        profile_id=profile.profile_id,
    )
    assert UserAccount.update_user_account(second.account_id, clashing) is False
    reloaded = UserAccount.view_user_account(second.account_id)
    assert reloaded is not None
    assert reloaded.phone_num == "0411222333"


def _seed_account(
    email: str = TC_ADMIN_EMAIL,
    password: str = DEFAULT_PASSWORD,
    profile: UserProfile | None = None,
    phone_num: str = TC_ADMIN_PHONE,
) -> UserAccount:
    return UserAccount.create_account(
        email=email,
        password=password,
        name="TC - Admin",
        dob=date(2000, 1, 1),
        phone_num=phone_num,
        profile_id=(profile or _seed_profile()).profile_id,
    )


def test_login_returns_user_account_on_matching_credentials() -> None:
    _seed_account()

    account = UserAccount.login(TC_ADMIN_EMAIL, DEFAULT_PASSWORD)

    assert account is not None
    assert account.email == TC_ADMIN_EMAIL
    assert account.account_id == "acc_001"
    assert account.profile_id == "prof_001"


def test_login_returns_none_when_email_does_not_match() -> None:
    _seed_account()

    assert UserAccount.login("nobody@x.com", DEFAULT_PASSWORD) is None


def test_login_returns_none_when_password_does_not_match() -> None:
    _seed_account()

    assert UserAccount.login(TC_ADMIN_EMAIL, "wrong-password") is None


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
        phone_num="0400000177", profile_id=profile.profile_id,
    )
    UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1990, 1, 1),
        phone_num="0400000181", profile_id=profile.profile_id,
    )
    UserAccount.create_account(
        email="c@x.com", password="p", name="C", dob=date(1990, 1, 1),
        phone_num="0400000185", profile_id=profile.profile_id,
    )

    accounts = UserAccount.view_all_user_accounts()

    assert [a.account_id for a in accounts] == ["acc_001", "acc_002", "acc_003"]
    assert [a.email for a in accounts] == ["a@x.com", "b@x.com", "c@x.com"]


def test_update_user_account_returns_true_on_success_and_persists_changes() -> None:
    profile = _seed_profile()
    created = _seed_account(profile=profile)

    updated = UserAccount(
        email=TC_ADMIN_EMAIL,
        password=DEFAULT_PASSWORD,
        name="TC - Admin (renamed)",
        dob=date(2000, 1, 1),
        phone_num=TC_ADMIN_PHONE,
        profile_id=profile.profile_id,
        suspended=True,
    )
    assert UserAccount.update_user_account(created.account_id, updated) is True

    fetched = UserAccount.view_user_account(created.account_id)
    assert fetched is not None
    assert fetched.email == TC_ADMIN_EMAIL
    assert fetched.name == "TC - Admin (renamed)"
    assert fetched.dob == date(2000, 1, 1)
    assert fetched.phone_num == TC_ADMIN_PHONE
    assert fetched.suspended is True


def test_update_user_account_returns_false_for_missing_id() -> None:
    """Negative path: no row matches account_id."""
    updated = UserAccount(
        email="x@x.com", password="p", name="X", dob=date(2000, 1, 1),
        phone_num="0400000222", profile_id="prof_001",
    )
    assert UserAccount.update_user_account("acc_999", updated) is False


def test_update_user_account_returns_false_for_duplicate_email() -> None:
    """Negative path: changing email to one already used by a different
    account hits the UNIQUE constraint; update_user_account returns False
    and the row is unchanged."""
    profile = _seed_profile()
    first = _seed_account(
        email=TC_FUNDRAISER_EMAIL, profile=profile, phone_num=TC_FUNDRAISER_PHONE,
    )
    second = UserAccount.create_account(
        email=TC_DONEE_EMAIL, password=DEFAULT_PASSWORD, name="TC - Donee",
        dob=date(2000, 1, 1), phone_num=TC_DONEE_PHONE,
        profile_id=profile.profile_id,
    )
    assert second is not None

    clashing = UserAccount(
        email=TC_FUNDRAISER_EMAIL, password=DEFAULT_PASSWORD, name="TC - Donee (renamed)",
        dob=date(2000, 1, 1), phone_num="0411111111",
        profile_id=profile.profile_id,
    )
    assert UserAccount.update_user_account(second.account_id, clashing) is False
    reloaded = UserAccount.view_user_account(second.account_id)
    assert reloaded is not None
    assert reloaded.email == TC_DONEE_EMAIL


def test_update_user_account_does_not_mutate_other_rows() -> None:
    profile = _seed_profile()
    first = _seed_account(email="a@x.com", profile=profile)
    second = UserAccount.create_account(
        email="b@x.com", password="p", name="B", dob=date(1990, 1, 1),
        phone_num="0400000255", profile_id=profile.profile_id,
    )

    updated = UserAccount(
        email="renamed@x.com", password="p", name="renamed",
        dob=date(1990, 1, 1), phone_num="0400000260",
        profile_id=profile.profile_id,
    )
    UserAccount.update_user_account(first.account_id, updated)

    untouched = UserAccount.view_user_account(second.account_id)
    assert untouched is not None
    assert untouched.email == "b@x.com"
    assert untouched.name == "B"


def test_suspend_user_account_returns_true_and_sets_suspended_flag() -> None:
    created = _seed_account()
    assert created.suspended is False

    assert UserAccount.suspend_user_account(created.account_id) is True

    fetched = UserAccount.view_user_account(created.account_id)
    assert fetched is not None
    assert fetched.suspended is True


def test_suspend_user_account_returns_false_for_missing_id() -> None:
    assert UserAccount.suspend_user_account("acc_999") is False


def test_suspended_account_cannot_log_in() -> None:
    """Negative path: suspending an account should block its login. This is
    a behavioural consequence of the suspended flag; the login query will
    need to filter out suspended rows."""
    created = _seed_account(email="suspend-me@x.com", password="secret")

    UserAccount.suspend_user_account(created.account_id)

    assert UserAccount.login("suspend-me@x.com", "secret") is None


def test_search_user_account_matches_email_substring_case_insensitive() -> None:
    profile = _seed_profile()
    UserAccount.create_account(
        email=TC_ADMIN_EMAIL, password=DEFAULT_PASSWORD, name="TC - Admin",
        dob=date(2000, 1, 1), phone_num=TC_ADMIN_PHONE,
        profile_id=profile.profile_id,
    )
    UserAccount.create_account(
        email="other@y.com", password=DEFAULT_PASSWORD, name="Other",
        dob=date(2000, 1, 1), phone_num="0411111111",
        profile_id=profile.profile_id,
    )

    results = UserAccount.search_user_account("TC-")
    assert [a.email for a in results] == [TC_ADMIN_EMAIL]


def test_search_user_account_matches_name_substring() -> None:
    profile = _seed_profile()
    UserAccount.create_account(
        email="a@x.com", password="p", name="Alice Smith", dob=date(1990, 1, 1),
        phone_num="0400000316", profile_id=profile.profile_id,
    )
    UserAccount.create_account(
        email="b@x.com", password="p", name="Bob Jones", dob=date(1990, 1, 1),
        phone_num="0400000320", profile_id=profile.profile_id,
    )

    results = UserAccount.search_user_account("smith")
    assert [a.name for a in results] == ["Alice Smith"]


def test_search_user_account_returns_empty_for_no_match() -> None:
    profile = _seed_profile()
    UserAccount.create_account(
        email=TC_ADMIN_EMAIL, password=DEFAULT_PASSWORD, name="TC - Admin",
        dob=date(2000, 1, 1), phone_num=TC_ADMIN_PHONE,
        profile_id=profile.profile_id,
    )
    assert UserAccount.search_user_account("zzz-no-match") == []


def test_search_user_account_returns_empty_on_empty_db() -> None:
    assert UserAccount.search_user_account("anything") == []
