"""Run pytest and print a TC-by-TC pass/fail table.

Each TC in docs/test_cases.md is backed by one or more pytest tests under
tests/. This script holds the TC -> pytest mapping, runs the suite once,
parses the verbose output, and prints a per-TC verdict grouped by sprint.

Usage:
    python scripts/verify_tcs.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TC_MAP: dict[str, str] = {
    # Sprint 1
    "TC-1.1":  "tests/test_user_profile.py::test_create_profile_persists_and_returns_profile_with_prefixed_id",
    "TC-1.2":  "tests/test_user_profile.py::test_create_profile_returns_none_for_duplicate_role",
    "TC-6.1":  "tests/test_user_account.py::test_create_account_persists_and_returns_account_with_prefixed_id",
    "TC-6.2":  "tests/test_user_account.py::test_create_account_returns_none_for_duplicate_email",
    "TC-11.1": "tests/test_user_account.py::test_login_returns_user_account_on_matching_credentials",
    "TC-11.2": "tests/test_user_account.py::test_login_returns_none_when_password_does_not_match",
    "TC-12.1": "tests/test_logout_page.py::test_render_does_not_raise_when_user_in_session",
    "TC-12.2": "tests/test_logout_page.py::test_render_does_not_raise_when_no_user_in_session",
    "TC-13.1": "tests/test_fundraising_activity.py::test_create_fundraising_activity_persists_and_returns_with_prefixed_id",
    "TC-13.2": "tests/test_create_fundraising_activity_page.py::test_validate_activity_rejects_start_date_in_the_past",
    "TC-18.1": "tests/test_user_account.py::test_login_returns_user_account_on_matching_credentials",
    "TC-18.2": "tests/test_user_account.py::test_login_returns_none_when_password_does_not_match",
    "TC-19.1": "tests/test_logout_page.py::test_render_does_not_raise_when_user_in_session",
    "TC-19.2": "tests/test_logout_page.py::test_render_does_not_raise_when_no_user_in_session",
    "TC-21.1": "tests/test_fundraising_activity.py::test_view_fundraising_activity_returns_activity_for_existing_id",
    "TC-21.2": "tests/test_fundraising_activity.py::test_view_fundraising_activity_returns_none_for_missing_id",
    "TC-26.1": "tests/test_user_account.py::test_login_returns_user_account_on_matching_credentials",
    "TC-26.2": "tests/test_user_account.py::test_login_returns_none_when_password_does_not_match",
    "TC-27.1": "tests/test_logout_page.py::test_render_does_not_raise_when_user_in_session",
    "TC-27.2": "tests/test_logout_page.py::test_render_does_not_raise_when_no_user_in_session",
    "TC-39.1": "tests/test_user_account.py::test_login_returns_user_account_on_matching_credentials",
    "TC-39.2": "tests/test_user_account.py::test_login_returns_none_when_password_does_not_match",
    "TC-40.1": "tests/test_logout_page.py::test_render_does_not_raise_when_user_in_session",
    "TC-40.2": "tests/test_logout_page.py::test_render_does_not_raise_when_no_user_in_session",
    # Sprint 2
    "TC-2.1":  "tests/test_user_profile.py::test_view_user_profile_returns_profile_for_existing_id",
    "TC-2.2":  "tests/test_user_profile.py::test_view_user_profile_returns_none_for_missing_id",
    "TC-3.1":  "tests/test_user_profile.py::test_update_user_profile_returns_true_on_success_and_persists_changes",
    "TC-3.2":  "tests/test_user_profile.py::test_update_user_profile_returns_false_for_duplicate_role",
    "TC-7.1":  "tests/test_user_account.py::test_view_user_account_returns_account_for_existing_id",
    "TC-7.2":  "tests/test_user_account.py::test_view_user_account_returns_none_for_missing_id",
    "TC-8.1":  "tests/test_user_account.py::test_update_user_account_returns_true_on_success_and_persists_changes",
    "TC-8.2":  "tests/test_user_account.py::test_update_user_account_returns_false_for_duplicate_email",
    "TC-14.1": "tests/test_fundraising_activity.py::test_view_my_fundraising_activity_returns_activity_for_correct_owner",
    "TC-14.2": "tests/test_fundraising_activity.py::test_view_my_fundraising_activity_returns_none_for_wrong_owner",
    "TC-15.1": "tests/test_fundraising_activity.py::test_update_my_fundraising_activity_returns_true_for_correct_owner",
    "TC-15.2": "tests/test_fundraising_activity.py::test_update_my_fundraising_activity_returns_false_for_wrong_owner",
    "TC-20.1": "tests/test_fundraising_activity.py::test_search_fundraising_activity_matches_title_substring",
    "TC-20.2": "tests/test_fundraising_activity.py::test_search_fundraising_activity_hides_suspended_from_donees",
    "TC-22.1": "tests/test_favourite.py::test_save_fundraising_activity_returns_true_on_first_save",
    "TC-22.2": "tests/test_favourite.py::test_save_fundraising_activity_returns_false_on_duplicate",
    "TC-24.1": "tests/test_favourite.py::test_view_favourite_list_scopes_to_the_account",
    "TC-24.2": "tests/test_favourite.py::test_view_favourite_list_hides_favourites_pointing_at_suspended_activities",
    # Sprint 3
    "TC-4.1":  "tests/test_user_profile.py::test_suspend_user_profile_returns_true_and_sets_suspended_flag",
    "TC-4.2":  "tests/test_user_profile.py::test_suspend_user_profile_returns_false_for_missing_id",
    "TC-5.1":  "tests/test_user_profile.py::test_search_user_profile_matches_role_substring_case_insensitive",
    "TC-5.2":  "tests/test_user_profile.py::test_search_user_profile_returns_empty_for_no_match",
    "TC-9.1":  "tests/test_user_account.py::test_suspend_user_account_returns_true_and_sets_suspended_flag",
    "TC-9.2":  "tests/test_user_account.py::test_suspend_user_account_returns_false_for_missing_id",
    "TC-10.1": "tests/test_user_account.py::test_search_user_account_matches_email_substring_case_insensitive",
    "TC-10.2": "tests/test_user_account.py::test_search_user_account_returns_empty_for_no_match",
    "TC-16.1": "tests/test_fundraising_activity.py::test_suspend_my_fundraising_activity_returns_true_for_correct_owner",
    "TC-16.2": "tests/test_fundraising_activity.py::test_suspend_my_fundraising_activity_returns_false_for_wrong_owner",
    "TC-17.1": "tests/test_fundraising_activity.py::test_search_my_fundraising_activity_scopes_to_owner_and_matches_criteria",
    "TC-17.2": "tests/test_fundraising_activity.py::test_search_my_fundraising_activity_returns_empty_for_no_activities",
    "TC-23.1": "tests/test_favourite.py::test_remove_favourite_returns_true_when_pair_exists",
    "TC-23.2": "tests/test_favourite.py::test_remove_favourite_returns_false_when_pair_missing",
    "TC-25.1": "tests/test_favourite.py::test_search_favourite_matches_activity_fields_for_the_donee",
    "TC-25.2": "tests/test_favourite.py::test_search_favourite_hides_favourites_pointing_at_suspended_activities",
    "TC-30.1": "tests/test_fundraising_activity.py::test_search_my_completed_fundraising_activity_matches_only_completed_and_owner_scoped",
    "TC-30.2": "tests/test_fundraising_activity.py::test_search_my_completed_fundraising_activity_returns_empty_for_no_matches",
    "TC-31.1": "tests/test_fundraising_activity.py::test_view_my_completed_fundraising_activities_returns_only_completed_for_owner",
    "TC-31.2": "tests/test_fundraising_activity.py::test_view_my_completed_fundraising_activities_returns_empty_for_no_completed",
    "TC-32.1": "tests/test_donation.py::test_search_my_donation_history_matches_activity_fields_for_the_donee",
    "TC-32.2": "tests/test_donation.py::test_search_my_donation_history_returns_empty_for_no_match",
    "TC-33.1": "tests/test_donation.py::test_view_my_donation_histories_returns_list_for_the_donee",
    "TC-33.2": "tests/test_donation.py::test_view_my_donation_histories_excludes_other_donees",
    # Sprint 4
    "TC-28.1": "tests/test_fundraising_activity.py::test_increment_view_count_bumps_by_one",
    "TC-28.2": "tests/test_fundraising_activity.py::test_view_fundraising_activity_view_count_returns_zero_for_missing_id",
    "TC-29.1": "tests/test_fundraising_activity.py::test_increment_save_count_supports_positive_and_negative_delta",
    "TC-29.2": "tests/test_fundraising_activity.py::test_view_fundraising_activity_save_count_returns_zero_for_missing_id",
    "TC-34.1": "tests/test_fundraising_activity_category.py::test_create_category_persists_and_returns_with_prefixed_id",
    "TC-34.2": "tests/test_fundraising_activity_category.py::test_create_category_returns_none_for_duplicate_name",
    "TC-35.1": "tests/test_fundraising_activity_category.py::test_view_fundraising_activity_category_returns_for_existing_id",
    "TC-35.2": "tests/test_fundraising_activity_category.py::test_view_fundraising_activity_category_returns_none_for_missing_id",
    "TC-36.1": "tests/test_fundraising_activity_category.py::test_update_fra_category_returns_true_and_persists_changes",
    "TC-36.2": "tests/test_fundraising_activity_category.py::test_update_fra_category_returns_false_for_duplicate_name",
    "TC-37.1": "tests/test_fundraising_activity_category.py::test_search_fra_category_matches_name_substring_case_insensitive",
    "TC-37.2": "tests/test_fundraising_activity_category.py::test_search_fra_category_returns_empty_for_no_match",
    "TC-38.1": "tests/test_fundraising_activity_category.py::test_suspend_fra_category_returns_true_and_sets_flag",
    "TC-38.2": "tests/test_fundraising_activity_category.py::test_suspend_fra_category_returns_false_for_missing_id",
    "TC-41.1": "tests/test_report.py::test_generate_daily_report_persists_with_prefixed_id_and_correct_type",
    "TC-41.2": "tests/test_report.py::test_generate_report_zero_amount_when_no_donations",
    "TC-42.1": "tests/test_report.py::test_generate_weekly_report_records_correct_type",
    "TC-42.2": "tests/test_report.py::test_generate_weekly_report_zero_amount_when_no_donations",
    "TC-43.1": "tests/test_report.py::test_generate_monthly_report_records_correct_type",
    "TC-43.2": "tests/test_report.py::test_generate_monthly_report_zero_amount_when_no_donations",
}

US_TO_SPRINT = {
    **{n: 1 for n in (1, 6, 11, 12, 13, 18, 19, 21, 26, 27, 39, 40)},
    **{n: 2 for n in (2, 3, 7, 8, 14, 15, 20, 22, 24)},
    **{n: 3 for n in (4, 5, 9, 10, 16, 17, 23, 25, 30, 31, 32, 33)},
    **{n: 4 for n in (28, 29, 34, 35, 36, 37, 38, 41, 42, 43)},
}


def run_pytest_and_parse() -> dict[str, str]:
    print("Running pytest (streaming output below)...\n", flush=True)
    proc = subprocess.Popen(
        ["pytest", "-v", "--tb=no", "--no-header"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1, cwd=ROOT,
    )
    assert proc.stdout is not None

    statuses: dict[str, str] = {}
    line_re = re.compile(r"^(tests/\S+::\S+?)\s+(PASSED|FAILED|ERROR|SKIPPED)")
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        m = line_re.match(line)
        if m:
            statuses[m.group(1)] = m.group(2)
    proc.wait()
    return statuses


def tc_sort_key(tc_id: str) -> tuple[int, int, int]:
    us, sub = tc_id.removeprefix("TC-").split(".")
    return (US_TO_SPRINT[int(us)], int(us), int(sub))


def main() -> int:
    statuses = run_pytest_and_parse()

    rows: list[tuple[str, str, str]] = []
    n_pass = 0
    n_total = len(TC_MAP)

    for tc_id in sorted(TC_MAP, key=tc_sort_key):
        node = TC_MAP[tc_id]
        status = statuses.get(node, "NOT COLLECTED")
        if status == "PASSED":
            n_pass += 1
        rows.append((tc_id, status, node))

    current_sprint = 0
    print(f"\n{'TC':<8} {'Status':<14} Pytest node")
    print("-" * 110)
    for tc_id, status, node in rows:
        us = int(tc_id.removeprefix("TC-").split(".")[0])
        sprint = US_TO_SPRINT[us]
        if sprint != current_sprint:
            current_sprint = sprint
            print(f"\n--- Sprint {sprint} ---")
        mark = "PASS" if status == "PASSED" else status
        print(f"{tc_id:<8} {mark:<14} {node}")

    print("\n" + "=" * 110)
    print(f"Summary: {n_pass}/{n_total} TCs pass")
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
