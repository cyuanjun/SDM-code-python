from entity.user_account import UserAccount
from entity.user_profile import UserProfile


def _make_profile() -> int:
    profile = UserProfile.create_profile("donee", "Test donee profile")
    assert profile and profile.profile_id is not None
    return profile.profile_id


def test_create_account_returns_account():
    profile_id = _make_profile()
    account = UserAccount.create_account(
        email="alice@example.com",
        password="secret123",
        name="Alice",
        dob="1995-06-01",
        phone_num="123456789",
        profile_id=profile_id,
    )
    assert account is not None
    assert account.email == "alice@example.com"
    assert account.account_id is not None


def test_create_account_rejects_duplicate_email():
    profile_id = _make_profile()
    UserAccount.create_account(
        "dup@example.com", "pw", "Dup", "1990-01-01", "111", profile_id
    )
    second = UserAccount.create_account(
        "dup@example.com", "pw", "Dup2", "1991-01-01", "222", profile_id
    )
    assert second is None


def test_login_returns_account_on_correct_credentials():
    profile_id = _make_profile()
    UserAccount.create_account(
        "bob@example.com", "pw123", "Bob", "1990-01-01", "999", profile_id
    )
    user = UserAccount.login("bob@example.com", "pw123")
    assert user is not None
    assert user.email == "bob@example.com"


def test_login_returns_none_on_wrong_password():
    profile_id = _make_profile()
    UserAccount.create_account(
        "carol@example.com", "right", "Carol", "1990-01-01", "555", profile_id
    )
    assert UserAccount.login("carol@example.com", "wrong") is None


def test_view_user_account_returns_account_by_id():
    profile_id = _make_profile()
    created = UserAccount.create_account(
        "viewme@example.com", "pw", "View Me", "1990-01-01", "111", profile_id
    )
    assert created and created.account_id is not None

    fetched = UserAccount.view_user_account(str(created.account_id))
    assert fetched is not None
    assert fetched.email == "viewme@example.com"


def test_view_user_account_returns_none_for_missing_id():
    assert UserAccount.view_user_account("99999") is None


def test_view_all_user_accounts_returns_every_account():
    profile_id = _make_profile()
    UserAccount.create_account("a@x.com", "pw", "A", "1990-01-01", "1", profile_id)
    UserAccount.create_account("b@x.com", "pw", "B", "1990-01-01", "2", profile_id)

    accounts = UserAccount.view_all_user_accounts()
    assert {a.email for a in accounts} == {"a@x.com", "b@x.com"}


def test_update_user_account_persists_changes():
    profile_id = _make_profile()
    created = UserAccount.create_account(
        "u@x.com", "pw", "Old Name", "1990-01-01", "111", profile_id
    )
    assert created and created.account_id is not None

    updated = UserAccount(
        email="u@x.com",
        password="pw",
        name="New Name",
        dob="1990-01-01",
        phone_num="222",
        profile_id=profile_id,
        account_id=created.account_id,
    )
    success = UserAccount.update_user_account(str(created.account_id), updated)
    assert success is True

    fetched = UserAccount.view_user_account(str(created.account_id))
    assert fetched is not None
    assert fetched.name == "New Name"
    assert fetched.phone_num == "222"


def test_update_user_account_returns_false_for_missing_id():
    profile_id = _make_profile()
    dummy = UserAccount(
        email="x@y.com", password="pw", name="X", dob="1990-01-01",
        phone_num="1", profile_id=profile_id, account_id=99999,
    )
    assert UserAccount.update_user_account("99999", dummy) is False
