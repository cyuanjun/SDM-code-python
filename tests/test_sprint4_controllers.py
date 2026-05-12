"""Sprint 4 controllers — pin pure-delegation contract."""
from controller.create_fundraising_activity_category_controller import (
    CreateFundraisingActivityCategoryController,
)
from controller.generate_daily_report_controller import GenerateDailyReportController
from controller.generate_monthly_report_controller import (
    GenerateMonthlyReportController,
)
from controller.generate_weekly_report_controller import GenerateWeeklyReportController
from controller.search_fundraising_activity_category_controller import (
    SearchFundraisingActivityCategoryController,
)
from controller.suspend_fundraising_activity_category_controller import (
    SuspendFundraisingActivityCategoryController,
)
from controller.update_fundraising_activity_category_controller import (
    UpdateFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_category_controller import (
    ViewFundraisingActivityCategoryController,
)
from controller.view_fundraising_activity_save_count_controller import (
    ViewFundraisingActivitySaveCountController,
)
from controller.view_fundraising_activity_view_count_controller import (
    ViewFundraisingActivityViewCountController,
)
from entity.fundraising_activity import FundraisingActivity
from entity.fundraising_activity_category import FundraisingActivityCategory


def test_create_category_controller_delegates():
    assert CreateFundraisingActivityCategoryController().create_category(
        "medical", "Medical emergencies"
    ) is True


def test_view_fra_category_controller_delegates():
    FundraisingActivityCategory.create_category("medical", "Medical")
    created = FundraisingActivityCategory.view_all_categories()[0]
    fetched = ViewFundraisingActivityCategoryController().view_fundraising_activity_category(
        created.category_id
    )
    assert fetched is not None and fetched.category_name == "medical"


def test_view_all_categories_controller_delegates():
    FundraisingActivityCategory.create_category("medical", "Medical")
    FundraisingActivityCategory.create_category("education", "Education")
    result = ViewFundraisingActivityCategoryController().view_all_categories()
    assert {c.category_name for c in result} == {"medical", "education"}


def test_update_fra_category_controller_delegates():
    FundraisingActivityCategory.create_category("medical", "Medical")
    created = FundraisingActivityCategory.view_all_categories()[0]
    updated = FundraisingActivityCategory(
        category_id=created.category_id,
        category_name="medical_v2",
        description="updated",
        status="active",
    )
    assert UpdateFundraisingActivityCategoryController().update_fundraising_activity_category(
        created.category_id, updated
    ) is True


def test_search_fra_category_controller_delegates():
    FundraisingActivityCategory.create_category("medical", "Medical emergencies")
    FundraisingActivityCategory.create_category("education", "Schools")
    results = SearchFundraisingActivityCategoryController().submit_search_criteria(
        "schools"
    )
    assert {c.category_name for c in results} == {"education"}


def test_suspend_fra_category_controller_delegates():
    FundraisingActivityCategory.create_category("medical", "Medical")
    created = FundraisingActivityCategory.view_all_categories()[0]
    assert SuspendFundraisingActivityCategoryController().suspend_fundraising_activity_category(
        created.category_id
    ) is True


def _activity():
    activity = FundraisingActivity(
        title="t", description="d", target_amount=100.0, category="x",
        start_date="2026-01-01", end_date="2026-02-01", status="active",
    )
    activity.save_fundraising_activity()
    return activity


def test_view_fundraising_activity_view_count_controller_delegates():
    activity = _activity()
    FundraisingActivity.increment_view_count(activity.activity_id)
    FundraisingActivity.increment_view_count(activity.activity_id)
    assert ViewFundraisingActivityViewCountController().view_fundraising_activity_view_count(
        activity.activity_id
    ) == 2


def test_view_fundraising_activity_save_count_controller_delegates():
    activity = _activity()
    FundraisingActivity.increment_save_count(activity.activity_id, +5)
    assert ViewFundraisingActivitySaveCountController().view_fundraising_activity_save_count(
        activity.activity_id
    ) == 5


def test_generate_daily_report_controller_delegates():
    report = GenerateDailyReportController().generate_daily_report(
        "2026-05-01", "2026-05-01", None
    )
    assert report.report_type == "daily"
    assert report.start_date == "2026-05-01"
    assert report.platform_manager_id is None


def test_generate_weekly_report_controller_delegates():
    report = GenerateWeeklyReportController().generate_weekly_report(
        "2026-05-01", "2026-05-07", None
    )
    assert report.report_type == "weekly"
    assert report.platform_manager_id is None


def test_generate_monthly_report_controller_delegates():
    report = GenerateMonthlyReportController().generate_monthly_report(
        "2026-05-01", "2026-05-31", None
    )
    assert report.report_type == "monthly"
    assert report.platform_manager_id is None
