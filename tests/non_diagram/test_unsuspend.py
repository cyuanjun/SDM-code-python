"""Tests for the Exception A unsuspend entity methods + controllers.

Mirror tests for the suspend methods — same happy + negative shape.
"""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from controller.non_diagram.unsuspend_fundraising_activity_category_controller import (
    UnsuspendFundraisingActivityCategoryController,
)
from controller.non_diagram.unsuspend_my_fundraising_activity_controller import (
    UnsuspendMyFundraisingActivityController,
)
from controller.non_diagram.unsuspend_user_account_controller import (
    UnsuspendUserAccountController,
)
from controller.non_diagram.unsuspend_user_profile_controller import (
    UnsuspendUserProfileController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.fundraising_activity_category import FundraisingActivityCategory
from entity.user_account import UserAccount
from entity.user_profile import UserProfile


# ----- UserProfile ----------------------------------------------------------


def test_unsuspend_user_profile_returns_true_and_clears_flag() -> None:
    profile = UserProfile.create_profile(role="admin", description="a")
    UserProfile.suspend_user_profile(profile.profile_id)

    assert UserProfile.unsuspend_user_profile(profile.profile_id) is True

    fetched = UserProfile.view_user_profile(profile.profile_id)
    assert fetched is not None
    assert fetched.suspended is False


def test_unsuspend_user_profile_returns_false_for_missing_id() -> None:
    """Negative path: no row matches profile_id."""
    assert UserProfile.unsuspend_user_profile("prof_999") is False


def test_unsuspend_user_profile_controller_delegates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserProfile,
        "unsuspend_user_profile",
        classmethod(lambda cls, profile_id: True),
    )
    assert (
        UnsuspendUserProfileController().unsuspend_user_profile("prof_001")
        is True
    )


# ----- UserAccount ----------------------------------------------------------


def _seed_account() -> UserAccount:
    profile = UserProfile.create_profile(role="admin", description="a")
    return UserAccount.create_account(
        email="a@x.com", password="p", name="A", dob=date(1990, 1, 1),
        phone_num="0400000070", profile_id=profile.profile_id,
    )


def test_unsuspend_user_account_returns_true_and_clears_flag() -> None:
    account = _seed_account()
    UserAccount.suspend_user_account(account.account_id)

    assert UserAccount.unsuspend_user_account(account.account_id) is True

    fetched = UserAccount.view_user_account(account.account_id)
    assert fetched is not None
    assert fetched.suspended is False


def test_unsuspend_user_account_returns_false_for_missing_id() -> None:
    assert UserAccount.unsuspend_user_account("acc_999") is False


def test_unsuspended_account_can_log_in_again() -> None:
    """Negative path of suspended-blocks-login: after unsuspend, login
    works again."""
    account = _seed_account()
    UserAccount.suspend_user_account(account.account_id)
    assert UserAccount.login("a@x.com", "p") is None  # suspended → no login

    UserAccount.unsuspend_user_account(account.account_id)
    assert UserAccount.login("a@x.com", "p") is not None


def test_unsuspend_user_account_controller_delegates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        UserAccount,
        "unsuspend_user_account",
        classmethod(lambda cls, account_id: False),
    )
    assert (
        UnsuspendUserAccountController().unsuspend_user_account("acc_001")
        is False
    )


# ----- FundraisingActivity (ownership-scoped) -------------------------------


def _seed_owner_and_activity() -> tuple[UserAccount, FundraisingActivity]:
    profile = UserProfile.create_profile(role="fundraiser", description="r")
    owner = UserAccount.create_account(
        email="o@x.com", password="p", name="O", dob=date(1990, 1, 1),
        phone_num="0400000121", profile_id=profile.profile_id,
    )
    activity = FundraisingActivity.create_fundraising_activity(
        title="A", description="d", target_amount=Decimal("100"),
        fra_cat_id="cat_001", start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
        owner_account_id=owner.account_id,
    )
    return owner, activity


def test_unsuspend_my_fra_returns_true_and_clears_flag() -> None:
    owner, activity = _seed_owner_and_activity()
    FundraisingActivity.suspend_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=activity.fra_id
    )

    ok = FundraisingActivity.unsuspend_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=activity.fra_id
    )
    assert ok is True

    fetched = FundraisingActivity.view_fundraising_activity(activity.fra_id)
    assert fetched is not None
    assert fetched.suspended is False


def test_unsuspend_my_fra_returns_false_for_wrong_owner() -> None:
    """Negative path: another fundraiser can't unsuspend someone else's
    activity even if they know the FRAId."""
    owner, activity = _seed_owner_and_activity()
    FundraisingActivity.suspend_my_fundraising_activity(
        owner_account_id=owner.account_id, fra_id=activity.fra_id
    )

    other = UserAccount.create_account(
        email="other@x.com", password="p", name="Other",
        dob=date(1990, 1, 1), phone_num="0400000157",
        profile_id=owner.profile_id,
    )

    ok = FundraisingActivity.unsuspend_my_fundraising_activity(
        owner_account_id=other.account_id, fra_id=activity.fra_id
    )
    assert ok is False
    fetched = FundraisingActivity.view_fundraising_activity(activity.fra_id)
    assert fetched is not None
    assert fetched.suspended is True


def test_unsuspend_my_fra_controller_delegates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivity,
        "unsuspend_my_fundraising_activity",
        classmethod(lambda cls, owner_account_id, fra_id: True),
    )
    assert (
        UnsuspendMyFundraisingActivityController()
        .unsuspend_my_fundraising_activity(
            owner_account_id="acc_001", fra_id="fra_001"
        )
        is True
    )


# ----- FundraisingActivityCategory ------------------------------------------


def test_unsuspend_fra_category_returns_true_and_clears_flag() -> None:
    cat = FundraisingActivityCategory.create_category("Health", "medical")
    FundraisingActivityCategory.suspend_fundraising_activity_category(
        cat.fra_cat_id
    )

    ok = (
        FundraisingActivityCategory
        .unsuspend_fundraising_activity_category(cat.fra_cat_id)
    )
    assert ok is True

    fetched = FundraisingActivityCategory.view_fundraising_activity_category(
        cat.fra_cat_id
    )
    assert fetched is not None
    assert fetched.suspended is False


def test_unsuspend_fra_category_returns_false_for_missing_id() -> None:
    assert (
        FundraisingActivityCategory
        .unsuspend_fundraising_activity_category("cat_999")
        is False
    )


def test_unsuspend_fra_category_controller_delegates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        FundraisingActivityCategory,
        "unsuspend_fundraising_activity_category",
        classmethod(lambda cls, fra_cat_id: False),
    )
    assert (
        UnsuspendFundraisingActivityCategoryController()
        .unsuspend_fundraising_activity_category("cat_001")
        is False
    )
