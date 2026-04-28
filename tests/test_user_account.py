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
