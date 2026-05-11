"""Sprint 4 — PlatformManager entity tests.

Minimal coverage: the diagrams introduce the actor without a login story,
so the entity only needs to support insert + list (the list is used by the
Report entity to source platformManagerId on the fly — see docs/issues.md
"Platform Manager actor has no login flow")."""
from entity.platform_manager import PlatformManager


def test_create_platform_manager_persists_record():
    pm = PlatformManager.create_platform_manager(
        username="pm1", password="pw", email="pm1@x.com", name="Pat Manager"
    )
    assert pm is not None
    assert pm.platform_manager_id is not None
    assert pm.username == "pm1"


def test_create_platform_manager_returns_none_on_duplicate_username():
    PlatformManager.create_platform_manager("pm1", "pw", "pm1@x.com", "Pat")
    assert (
        PlatformManager.create_platform_manager("pm1", "pw", "pm2@x.com", "Pat 2")
        is None
    )


def test_create_platform_manager_returns_none_on_duplicate_email():
    PlatformManager.create_platform_manager("pm1", "pw", "pm@x.com", "Pat")
    assert (
        PlatformManager.create_platform_manager("pm2", "pw", "pm@x.com", "Pat 2")
        is None
    )


def test_view_all_platform_managers_returns_every_row():
    PlatformManager.create_platform_manager("pm1", "pw", "pm1@x.com", "One")
    PlatformManager.create_platform_manager("pm2", "pw", "pm2@x.com", "Two")
    rows = PlatformManager.view_all_platform_managers()
    assert {pm.username for pm in rows} == {"pm1", "pm2"}


def test_view_all_platform_managers_returns_empty_when_no_rows():
    assert PlatformManager.view_all_platform_managers() == []
