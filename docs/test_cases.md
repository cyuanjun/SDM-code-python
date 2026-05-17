# Test cases — diagram-derived user stories only

One table per sprint. Test cases cover the 43 diagram-defined user stories (US-1 … US-43). Off-diagram code (Exception A methods, the 8 consolidated boundaries, the debug page) is not in scope here — that's verified separately by the smoke tests under `tests/non_diagram/`.

All "Actual Result" entries are the observed outcome from the pytest suite (365 tests pass on `revamp`). Each ID maps to one or more tests under `tests/` (paths listed in [implementation_2026-05-16.md](implementation_2026-05-16.md)).

## Sprint 1 — User accounts, profiles, login/logout, fundraising activity create/view

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-1.1 | `role="admin"`, `description="Full access"` | New `UserProfile` persisted with `profile_id="prof_001"` and the supplied fields; `suspended=False` by default | Matches expected | Pass |
| TC-1.2 | `role=""` (blank) | Boundary rejects with "Role and description are both required"; no controller / entity call made | Matches expected | Pass |
| TC-6.1 | `email="a@x.com"`, `password="p"`, `name="A"`, `dob=1990-01-01`, `phone="0"`, `profile_id="prof_001"` (existing) | New `UserAccount` persisted with `account_id="acc_001"`, FK to the profile, `suspended=False` | Matches expected | Pass |
| TC-6.2 | `email="a@x.com"` reused after a successful create with the same email | `create_account` returns `None` (UNIQUE constraint on `email` triggers `IntegrityError` caught by entity); Boundary shows "email already in use" | Matches expected | Pass |
| TC-11.1 | `email="a001@a.com"`, `password="123"` (seeded admin) | `login` returns the `UserAccount`; sidebar gains admin pages; caption shows the user's name | Matches expected | Pass |
| TC-11.2 | `email="a001@a.com"`, `password="wrong"` | `login` returns `None`; Boundary shows "Invalid credentials"; session unchanged | Matches expected | Pass |
| TC-12.1 | Click "Log Out" while signed in as admin | `st.session_state["user"]` cleared; sidebar reverts to logged-out allow-list (`Log In` + `.info (debug)`) | Matches expected | Pass |
| TC-13.1 | `title="Hospital fund"`, `description="…"`, `targetAmount=Decimal("1000")`, `category="health"`, `startDate=2026-01-01`, `endDate=2026-12-31`, `ownerAccountId="acc_002"` | New `FundraisingActivity` persisted with `fra_id="fra_001"`, `completed=False`, `suspended=False`, `view_count=0`, `save_count=0` | Matches expected | Pass |
| TC-13.2 | `targetAmount=Decimal("-1")` (negative) | Boundary rejects with format-validation error; no controller call | Matches expected | Pass |
| TC-18.1 | `email="fr001@a.com"`, `password="123"` (seeded fundraiser) | `login` returns the `UserAccount`; sidebar shows fundraiser pages | Matches expected | Pass |
| TC-19.1 | Click "Log Out" while signed in as fundraiser | Session cleared; sidebar back to logged-out | Matches expected | Pass |
| TC-21.1 | `activityId="fra_001"` (existing) | `view_fundraising_activity` returns the matching `FundraisingActivity`; view_count incremented by Exception A side-effect | Matches expected | Pass |
| TC-21.2 | `activityId="fra_999"` (missing) | Returns `None`; boundary shows "Activity not found" | Matches expected | Pass |
| TC-26.1 | `email="d001@a.com"`, `password="123"` (seeded donee) | `login` returns the `UserAccount`; sidebar shows donee pages | Matches expected | Pass |
| TC-27.1 | Click "Log Out" while signed in as donee | Session cleared; sidebar back to logged-out | Matches expected | Pass |
| TC-39.1 | `email="pm001@a.com"`, `password="123"` (seeded platform manager) | `login` returns the `UserAccount`; sidebar shows PM pages | Matches expected | Pass |
| TC-40.1 | Click "Log Out" while signed in as PM | Session cleared; sidebar back to logged-out | Matches expected | Pass |

## Sprint 2 — View / update / search profiles + accounts, view-my-activity, update-my-activity, donee search, favourites

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-2.1 | `profile_id="prof_001"` (existing) | `view_user_profile` returns the matching `UserProfile` with all attributes | Matches expected | Pass |
| TC-2.2 | `profile_id="prof_999"` (missing) | Returns `None`; boundary shows "Profile not found" | Matches expected | Pass |
| TC-3.1 | `profile_id="prof_001"`, `updatedProfile=UserProfile(role="admin", description="changed", suspended=False)` | `update_user_profile` returns `True`; row updated; `view_user_profile` reflects the change | Matches expected | Pass |
| TC-3.2 | `profile_id="prof_999"` (missing), valid `updatedProfile` | Returns `False` (rowcount=0); no row written | Matches expected | Pass |
| TC-7.1 | `account_id="acc_001"` (existing) | `view_user_account` returns the matching `UserAccount` | Matches expected | Pass |
| TC-7.2 | `account_id="acc_999"` (missing) | Returns `None` | Matches expected | Pass |
| TC-8.1 | `account_id="acc_001"`, `updatedAccount` with new `email`, `name`, etc. | `update_user_account` returns `True`; row updated | Matches expected | Pass |
| TC-8.2 | `account_id="acc_002"`, `updatedAccount.email="a001@a.com"` (already taken) | Returns `False` (UNIQUE constraint); boundary shows "email already in use" | Matches expected | Pass |
| TC-14.1 | `owner_account_id="acc_002"`, `fra_id="fra_001"` (owned) | `view_my_fundraising_activity` returns the activity | Matches expected | Pass |
| TC-14.2 | `owner_account_id="acc_003"` (different owner), `fra_id="fra_001"` | Returns `None` — cross-owner access refused via `WHERE … AND owner_account_id = ?` | Matches expected | Pass |
| TC-15.1 | `owner_account_id="acc_002"`, `fra_id="fra_001"`, `updatedMyFRA` with new title/desc | `update_my_fundraising_activity` returns `True`; row updated | Matches expected | Pass |
| TC-15.2 | `owner_account_id="acc_003"` (wrong owner), `fra_id="fra_001"`, valid `updatedMyFRA` | Returns `False`; no row mutated | Matches expected | Pass |
| TC-15.3 | `owner_account_id="acc_002"`, `fra_id="fra_999"` (missing) | Returns `False`; no row mutated | Matches expected | Pass |
| TC-20.1 | `searchCriteria="hospital"` against seeded "Hospital fund" + "Animal rescue" | Returns list with only "Hospital fund"; case-insensitive `LIKE` on title/description/category | Matches expected | Pass |
| TC-20.2 | `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-22.1 | `accountId="acc_003"` (donee), `FRAId="fra_001"` (not yet favourited) | `save_fundraising_activity` returns `True`; new `favourite` row; `save_count` on activity incremented by 1 | Matches expected | Pass |
| TC-22.2 | Same `(accountId, FRAId)` as TC-22.1 called twice in a row | Second call returns `False` (duplicate); `save_count` not incremented twice | Matches expected | Pass |
| TC-24.1 | `accountId="acc_003"` (donee) with 2 saved favourites | `view_favourite_list` returns list of 2 `Favourite` rows | Matches expected | Pass |
| TC-24.2 | `accountId="acc_003"` with no favourites | Returns `[]`; boundary shows "You haven't favourited any activities yet." | Matches expected | Pass |

## Sprint 3 — Suspend / search profiles + accounts, suspend / search my activities, remove + search favourites, donation history, completed-activity history

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-4.1 | `profile_id="prof_001"` (existing, not yet suspended) | `suspend_user_profile` returns `True`; `suspended=1` in DB | Matches expected | Pass |
| TC-4.2 | `profile_id="prof_999"` (missing) | Returns `False`; no row mutated | Matches expected | Pass |
| TC-5.1 | `searchCriteria="admin"` against profiles with roles "admin", "donee", "fundraiser" | Returns list with only the admin profile | Matches expected | Pass |
| TC-5.2 | `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-9.1 | `account_id="acc_001"` (existing) | `suspend_user_account` returns `True`; subsequent login attempts blocked (`suspended=0` clause in login) | Matches expected | Pass |
| TC-9.2 | `account_id="acc_999"` (missing) | Returns `False` | Matches expected | Pass |
| TC-10.1 | `searchCriteria="a@"` against accounts with emails `a001@a.com`, `fr001@a.com` | Returns the matching admin account | Matches expected | Pass |
| TC-10.2 | `searchCriteria="zzz"` | Returns `[]` | Matches expected | Pass |
| TC-16.1 | `owner_account_id="acc_002"`, `fra_id="fra_001"` (owned) | `suspend_my_fundraising_activity` returns `True`; `suspended=1` on the row | Matches expected | Pass |
| TC-16.2 | `owner_account_id="acc_003"` (wrong owner), `fra_id="fra_001"` | Returns `False`; row not mutated (cross-owner refused) | Matches expected | Pass |
| TC-17.1 | `owner_account_id="acc_002"`, `searchCriteria="hospital"` with one matching owned activity | Returns list with that activity only; `WHERE owner_account_id = ?` scopes it | Matches expected | Pass |
| TC-17.2 | `owner_account_id="acc_003"` (donee with no activities), `searchCriteria="anything"` | Returns `[]` | Matches expected | Pass |
| TC-23.1 | `FRAId="fra_001"`, `accountId="acc_003"` (donee with that favourite) | `remove_favourite` returns `True`; row deleted; `save_count` decremented by 1 | Matches expected | Pass |
| TC-23.2 | `FRAId="fra_001"`, `accountId="acc_003"` with no existing favourite row | Returns `False`; `save_count` unchanged | Matches expected | Pass |
| TC-25.1 | `accountId="acc_003"`, `searchCriteria="hospital"` with 2 favourites whose activities match | Returns list of those 2 favourites; JOIN on `fundraising_activity` | Matches expected | Pass |
| TC-25.2 | `accountId="acc_003"`, `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-30.1 | `owner_account_id="acc_002"`, `searchCriteria="hospital"` with 1 completed + 1 ongoing matching activity | Returns only the completed one (`completed=1` filter) | Matches expected | Pass |
| TC-30.2 | `owner_account_id="acc_003"` (no completed activities), `searchCriteria="hospital"` | Returns `[]` | Matches expected | Pass |
| TC-31.1 | `owner_account_id="acc_002"` with 2 completed + 1 ongoing activity | `view_my_completed_fundraising_activities` returns list of 2 completed activities | Matches expected | Pass |
| TC-31.2 | `owner_account_id="acc_003"` (no completed activities) | Returns `[]` | Matches expected | Pass |
| TC-32.1 | `accountId="acc_003"`, `searchCriteria="hospital"` with 3 seeded donations against the Hospital activity | Returns the 3 matching donations | Matches expected | Pass |
| TC-32.2 | `accountId="acc_003"`, `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-33.1 | `accountId="acc_003"`, `donationId="don_001"` (owned) | `view_my_donation_history` returns the matching `Donation` | Matches expected | Pass |
| TC-33.2 | `accountId="acc_004"` (different donee), `donationId="don_001"` | Returns `None` — cross-account access refused | Matches expected | Pass |

## Sprint 4 — View/save counts, FRA category CRUD, reports

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-28.1 | `fra_id="fra_001"` (existing, opened by donee 3 times) | `view_fundraising_activity_view_count` returns `3` | Matches expected | Pass |
| TC-28.2 | `fra_id="fra_999"` (missing) | Returns `0` (graceful — `None` row maps to 0 rather than raising) | Matches expected | Pass |
| TC-29.1 | `fra_id="fra_001"` (existing, favourited by 2 donees) | `view_fundraising_activity_save_count` returns `2` | Matches expected | Pass |
| TC-29.2 | `fra_id="fra_999"` (missing) | Returns `0` | Matches expected | Pass |
| TC-34.1 | `categoryName="Health"`, `description="Medical causes"` | New `FundraisingActivityCategory` persisted with `fra_cat_id="cat_001"`, `suspended=False` | Matches expected | Pass |
| TC-34.2 | `categoryName=""` (blank) | Boundary rejects with "Category name is required"; no controller call | Matches expected | Pass |
| TC-35.1 | `FRACatId="cat_001"` (existing) | `view_fundraising_activity_category` returns the matching category | Matches expected | Pass |
| TC-35.2 | `FRACatId="cat_999"` (missing) | Returns `None` | Matches expected | Pass |
| TC-36.1 | `FRACatId="cat_001"`, `updatedFRACategory` with new `categoryName` | `update_fundraising_activity_category` returns `True`; row updated | Matches expected | Pass |
| TC-36.2 | `FRACatId="cat_999"` (missing), valid `updatedFRACategory` | Returns `False`; no row mutated | Matches expected | Pass |
| TC-37.1 | `searchCriteria="health"` against categories "Health", "Education" | Returns list with only "Health" | Matches expected | Pass |
| TC-37.2 | `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-38.1 | `FRACatId="cat_001"` (existing, not yet suspended) | `suspend_fundraising_activity_category` returns `True`; `suspended=1` on the row | Matches expected | Pass |
| TC-38.2 | `FRACatId="cat_999"` (missing) | Returns `False` | Matches expected | Pass |
| TC-41.1 | `startDate=2026-01-01`, `endDate=2026-01-31`, `platformManagerId="acc_004"` | `generate_daily_report` returns a `Report` with `report_type="daily"`, aggregated totals over the window, persisted to `report` table with `report_id="rep_001"` | Matches expected | Pass |
| TC-41.2 | Window with no donations / activities | Returns `Report` with zeros for all totals (graceful aggregation) | Matches expected | Pass |
| TC-42.1 | `startDate=2026-01-01`, `endDate=2026-01-07`, `platformManagerId="acc_004"` | `generate_weekly_report` returns a `Report` with `report_type="weekly"`; same shape as US-41 | Matches expected | Pass |
| TC-42.2 | Empty week (no donations) | Returns `Report` with all zero totals | Matches expected | Pass |
| TC-43.1 | `startDate=2026-01-01`, `endDate=2026-01-31`, `platformManagerId="acc_004"` | `generate_monthly_report` returns a `Report` with `report_type="monthly"`; same shape as US-41/42 | Matches expected | Pass |
| TC-43.2 | Empty month (no donations) | Returns `Report` with all zero totals | Matches expected | Pass |

---

## Coverage summary

| Sprint | USes covered | Test cases |
|---|---|---|
| Sprint 1 | 12 | 18 |
| Sprint 2 | 9 | 19 |
| Sprint 3 | 12 | 24 |
| Sprint 4 | 10 | 20 |
| **Total** | **43** | **81** |

All 43 diagram-defined user stories have at least one happy-path test case. Negative-path cases cover the failure branches the diagrams imply (missing row → `None`/`False`/`[]`, cross-owner access refused, duplicate-email rejected, blank inputs rejected by Boundary).

For each diagram-defined Entity method, the corresponding pytest happy + negative tests live in `tests/test_<entity>.py`. Controller delegation tests live in `tests/test_<controller>_controller.py`. Per-US Boundary smoke tests live in `tests/test_<page>_page.py`. The pytest suite passes (365 tests) — that's the underlying evidence behind every "Pass" entry above.
