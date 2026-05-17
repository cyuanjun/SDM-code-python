"""Smoke tests for the debug-only InfoPage."""
from __future__ import annotations

from streamlit.testing.v1 import AppTest

from boundary.non_diagram.info_page import InfoPage


def test_info_page_is_importable_and_has_render() -> None:
    assert callable(InfoPage().render)


def test_info_page_renders_on_empty_db() -> None:
    script = """
from boundary.non_diagram.info_page import InfoPage
InfoPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception


def test_info_page_renders_with_data() -> None:
    script = """
from datetime import date
from decimal import Decimal
from entity.user_profile import UserProfile
from entity.user_account import UserAccount
from entity.fundraising_activity import FundraisingActivity
from entity.favourite import Favourite
from entity.donation import Donation
from entity.fundraising_activity_category import FundraisingActivityCategory
from entity.report import Report
from boundary.non_diagram.info_page import InfoPage

donee_profile = UserProfile.create_profile(role='donee', description='r')
fr_profile = UserProfile.create_profile(role='fundraiser', description='r')
pm_profile = UserProfile.create_profile(role='platform_manager', description='PM')
donee = UserAccount.create_account(
    email='d@x.com', password='p', name='D', dob=date(1990, 1, 1),
    phone_num='0', profile_id=donee_profile.profile_id,
)
fr = UserAccount.create_account(
    email='f@x.com', password='p', name='F', dob=date(1990, 1, 1),
    phone_num='0', profile_id=fr_profile.profile_id,
)
pm = UserAccount.create_account(
    email='pm@x.com', password='p', name='PM', dob=date(1980, 1, 1),
    phone_num='0', profile_id=pm_profile.profile_id,
)
activity = FundraisingActivity.create_fundraising_activity(
    title='A', description='d', target_amount=Decimal('100'),
    category='x', start_date=date(2026, 1, 1), end_date=date(2026, 2, 1),
    owner_account_id=fr.account_id,
)
Favourite.save_fundraising_activity(account_id=donee.account_id, fra_id=activity.fra_id)
Donation.create_donation(
    account_id=donee.account_id, fra_id=activity.fra_id,
    amount=Decimal('50'), donation_date=date(2026, 1, 15),
)
FundraisingActivityCategory.create_category('Health', 'medical')
Report.generate_daily_report(
    start_date=date(2026, 1, 1), end_date=date(2026, 1, 31),
    platform_manager_id=pm.account_id,
)
InfoPage().render()
"""
    at = AppTest.from_string(script)
    at.run()
    assert not at.exception
