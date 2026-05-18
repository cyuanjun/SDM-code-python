# Test cases — diagram-derived user stories only

One table per sprint. Test cases cover the 43 diagram-defined user stories (US-1 … US-43). Off-diagram code (Exception A methods, the 8 consolidated boundaries, the debug page) is not in scope here — that's verified separately by the smoke tests under `tests/non_diagram/`.

The bold sentence at the start of each "Test Data" cell describes what the case verifies; what follows is the concrete input. All "Actual Result" entries are the observed outcome from the pytest suite (**404 tests** pass on `revamp-final-diagrams` as of 2026-05-18). Each ID maps to one or more tests under `tests/` (paths listed in [implementation_2026-05-18.md](implementation_2026-05-18.md)).

## Sprint 1 — User accounts, profiles, login/logout, fundraising activity create/view

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-1.1 | **Verifies a fresh user profile is persisted with the first sequential id.** `role="admin"`, `description="Full access"` | New `UserProfile` persisted with `profile_id="prof_001"` and the supplied fields; `suspended=False` by default | Matches expected | Pass |
| TC-1.2 | **Verifies the boundary rejects blank input before calling the controller.** `role=""` (blank) | Boundary shows "Role and description are both required"; no controller / entity call made | Matches expected | Pass |
| TC-1.3 | **Verifies the role UNIQUE constraint rejects a second profile with the same role.** First create `role="admin"`; then attempt second create with `role="admin"` | First returns the profile; second returns `None` (IntegrityError caught); boundary surfaces "A profile with that role already exists." | Matches expected | Pass |
| TC-6.1 | **Verifies a new user account is persisted and FK-linked to an existing profile.** `email="a@x.com"`, `password="p"`, `name="A"`, `dob=1990-01-01`, `phone="0"`, `profile_id="prof_001"` (existing) | New `UserAccount` persisted with `account_id="acc_001"`, FK to the profile, `suspended=False` | Matches expected | Pass |
| TC-6.2 | **Verifies the email UNIQUE constraint rejects a duplicate.** `email="a@x.com"` reused after a successful create with the same email | `create_account` returns `None` (UNIQUE constraint on `email` triggers `IntegrityError`); Boundary shows "email already in use" | Matches expected | Pass |
| TC-11.1 | **Verifies a valid login returns the account and updates session/sidebar.** `email="a001@a.com"`, `password="123"` (seeded admin) | `login` returns the `UserAccount`; sidebar gains admin pages; caption shows the user's name | Matches expected | Pass |
| TC-11.2 | **Verifies a wrong password fails closed (no session change).** `email="a001@a.com"`, `password="wrong"` | `login` returns `None`; Boundary shows "Invalid credentials"; session unchanged | Matches expected | Pass |
| TC-12.1 | **Verifies logout clears the session and restores the logged-out sidebar.** Click "Log Out" while signed in as admin | `st.session_state["user"]` cleared; sidebar reverts to logged-out allow-list (`Log In` + `.info (debug)`) | Matches expected | Pass |
| TC-12.2 | **Verifies a logout when no user is in session is a graceful no-op.** Trigger `logout()` with `"user"` absent from session state | `st.session_state.pop("user", None)` does not raise; sidebar already in the logged-out state, no change | Matches expected | Pass |
| TC-13.1 | **Verifies a fundraising activity is persisted with sensible defaults and the curated category FK resolves.** `title="Hospital fund"`, `description="…"`, `targetAmount=Decimal("1000")`, `FRACatId="cat_001"` (existing curated category), `startDate=2099-01-01`, `endDate=2099-12-31`, `ownerAccountId="acc_002"` | New `FundraisingActivity` persisted with `fra_id="fra_001"`, `suspended=False`, `view_count=0`, `save_count=0`. `completed` is a derived `@property` (`end_date < today`), `False` for a future end-date | Matches expected | Pass |
| TC-13.2 | **Verifies the boundary rejects a non-positive target amount.** `targetAmount=Decimal("-1")` (negative) | Boundary rejects with format-validation error; no controller call | Matches expected | Pass |
| TC-13.3 | **Verifies the boundary rejects a start_date in the past (new 2026-05-18 guard).** `startDate=2025-12-31`, `endDate=2026-06-01`, anchored to `today=2026-01-01` | `validate_activity` returns `False`; boundary surfaces the past-date error; no controller call | Matches expected | Pass |
| TC-13.4 | **Verifies the boundary accepts start_date equal to today.** `startDate=today`, `endDate=today+months`, anchored to `today=2026-01-01` | `validate_activity` returns `True`; activity is created | Matches expected | Pass |
| TC-18.1 | **Verifies a fundraiser logs in and gains fundraiser-only sidebar entries.** `email="fr001@a.com"`, `password="123"` | `login` returns the `UserAccount`; sidebar shows fundraiser pages | Matches expected | Pass |
| TC-18.2 | **Verifies a fundraiser login with a wrong password fails closed.** `email="fr001@a.com"`, `password="wrong"` | `login` returns `None`; Boundary shows "Invalid credentials"; session unchanged | Matches expected | Pass |
| TC-19.1 | **Verifies a fundraiser logout restores the logged-out sidebar.** Click "Log Out" while signed in as fundraiser | Session cleared; sidebar back to logged-out | Matches expected | Pass |
| TC-19.2 | **Verifies a fundraiser logout when no user is in session is a graceful no-op.** Trigger `logout()` with `"user"` absent from session state | `pop` does not raise; sidebar unchanged | Matches expected | Pass |
| TC-21.1 | **Verifies a donee can view an existing activity's details (and view_count is bumped).** `activityId="fra_001"` (existing) | `view_fundraising_activity` returns the matching `FundraisingActivity`; view_count incremented by Exception A side-effect | Matches expected | Pass |
| TC-21.2 | **Verifies viewing a missing activity returns None rather than raising.** `activityId="fra_999"` (missing) | Returns `None`; boundary shows "Activity not found" | Matches expected | Pass |
| TC-26.1 | **Verifies a donee logs in and gains donee-only sidebar entries.** `email="d001@a.com"`, `password="123"` | `login` returns the `UserAccount`; sidebar shows donee pages | Matches expected | Pass |
| TC-26.2 | **Verifies a donee login with a wrong password fails closed.** `email="d001@a.com"`, `password="wrong"` | `login` returns `None`; Boundary shows "Invalid credentials"; session unchanged | Matches expected | Pass |
| TC-27.1 | **Verifies a donee logout restores the logged-out sidebar.** Click "Log Out" while signed in as donee | Session cleared; sidebar back to logged-out | Matches expected | Pass |
| TC-27.2 | **Verifies a donee logout when no user is in session is a graceful no-op.** Trigger `logout()` with `"user"` absent from session state | `pop` does not raise; sidebar unchanged | Matches expected | Pass |
| TC-39.1 | **Verifies a platform manager logs in and gains PM-only sidebar entries.** `email="pm001@a.com"`, `password="123"` | `login` returns the `UserAccount`; sidebar shows PM pages | Matches expected | Pass |
| TC-39.2 | **Verifies a PM login with a wrong password fails closed.** `email="pm001@a.com"`, `password="wrong"` | `login` returns `None`; Boundary shows "Invalid credentials"; session unchanged | Matches expected | Pass |
| TC-40.1 | **Verifies a PM logout restores the logged-out sidebar.** Click "Log Out" while signed in as PM | Session cleared; sidebar back to logged-out | Matches expected | Pass |
| TC-40.2 | **Verifies a PM logout when no user is in session is a graceful no-op.** Trigger `logout()` with `"user"` absent from session state | `pop` does not raise; sidebar unchanged | Matches expected | Pass |

## Sprint 2 — View / update / search profiles + accounts, view-my-activity, update-my-activity, donee search, favourites

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-2.1 | **Verifies viewing an existing profile returns the full record.** `profile_id="prof_001"` (existing) | `view_user_profile` returns the matching `UserProfile` with all attributes | Matches expected | Pass |
| TC-2.2 | **Verifies viewing a missing profile returns None.** `profile_id="prof_999"` (missing) | Returns `None`; boundary shows "Profile not found" | Matches expected | Pass |
| TC-3.1 | **Verifies a profile update persists and is reflected on next read.** `profile_id="prof_001"`, `updatedProfile=UserProfile(role="admin", description="changed", suspended=False)` | `update_user_profile` returns `True`; row updated; `view_user_profile` reflects the change | Matches expected | Pass |
| TC-3.2 | **Verifies update returns False when no row matches the id.** `profile_id="prof_999"` (missing), valid `updatedProfile` | Returns `False` (rowcount=0); no row written | Matches expected | Pass |
| TC-3.3 | **Verifies the role UNIQUE constraint rejects an update that would collide.** Two profiles exist (`admin`, `donee`); attempt to update `donee` profile's role to `admin` | Returns `False` (IntegrityError caught); donee profile's role unchanged | Matches expected | Pass |
| TC-7.1 | **Verifies viewing an existing account returns the full record.** `account_id="acc_001"` (existing) | `view_user_account` returns the matching `UserAccount` | Matches expected | Pass |
| TC-7.2 | **Verifies viewing a missing account returns None.** `account_id="acc_999"` (missing) | Returns `None` | Matches expected | Pass |
| TC-8.1 | **Verifies an account update persists and is reflected on next read.** `account_id="acc_001"`, `updatedAccount` with new `email`, `name`, etc. | `update_user_account` returns `True`; row updated | Matches expected | Pass |
| TC-8.2 | **Verifies the email UNIQUE constraint rejects an update that would collide.** `account_id="acc_002"`, `updatedAccount.email="a001@a.com"` (already taken) | Returns `False`; boundary shows "email already in use" | Matches expected | Pass |
| TC-14.1 | **Verifies a fundraiser views one of their own activities.** `owner_account_id="acc_002"`, `fra_id="fra_001"` (owned) | `view_my_fundraising_activity` returns the activity | Matches expected | Pass |
| TC-14.2 | **Verifies cross-owner access is refused at the entity layer.** `owner_account_id="acc_003"` (different owner), `fra_id="fra_001"` | Returns `None` — cross-owner access refused via `WHERE … AND owner_account_id = ?` | Matches expected | Pass |
| TC-15.1 | **Verifies a fundraiser can update one of their own activities (6 unpacked fields per the 2026-05-18 diagram).** `owner_account_id="acc_002"`, `fra_id="fra_001"`, `title="New title"`, `description="New desc"`, `target_amount=Decimal("999.99")`, `fra_cat_id="cat_001"`, `start_date=2025-01-01`, `end_date=2025-12-31` | `update_my_fundraising_activity` returns `True`; row updated; derived `completed` flips to `True` because new `end_date < today` | Matches expected | Pass |
| TC-15.2 | **Verifies a fundraiser cannot update another fundraiser's activity.** `owner_account_id="acc_003"` (wrong owner), `fra_id="fra_001"`, valid unpacked fields | Returns `False`; no row mutated | Matches expected | Pass |
| TC-15.3 | **Verifies update returns False when no FRAId matches.** `owner_account_id="acc_002"`, `fra_id="fra_999"` (missing), valid unpacked fields | Returns `False`; no row mutated | Matches expected | Pass |
| TC-15.4 | **Verifies the boundary rejects end_date in the past (new 2026-05-18 guard).** Existing activity has past `start_date`; user attempts to set `end_date=2025-12-31` against `today=2026-01-01` | `validate_activity` returns `False`; boundary surfaces the past-end-date error; no entity call | Matches expected | Pass |
| TC-15.5 | **Verifies the boundary accepts a past start_date paired with a future end_date.** Already-running activity: `start_date=2025-06-01`, `end_date=2026-06-01`, anchored to `today=2026-01-01` | `validate_activity` returns `True`; user can extend the end date on a running activity | Matches expected | Pass |
| TC-20.1 | **Verifies search filters activities by title/description/category_name (case-insensitive, JOIN'd from `fundraising_activity_category`).** `searchCriteria="hospital"` against seeded "Hospital fund" + "Animal rescue" | Returns list with only "Hospital fund"; case-insensitive `LIKE` on title/description/category_name (post-2026-05-18 FRACatId refactor) | Matches expected | Pass |
| TC-20.2 | **Verifies search returns an empty list when nothing matches.** `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-20.3 | **Verifies donee-facing search hides suspended activities (new 2026-05-18 rule).** One ongoing + one suspended activity, both titles match the criteria | Returns only the ongoing activity; the suspended one is filtered out via `WHERE a.suspended = 0`. Owner-scoped `search_my_fundraising_activity` still includes it. | Matches expected | Pass |
| TC-22.1 | **Verifies a donee can favourite an activity (and save_count is bumped).** `accountId="acc_003"` (donee), `FRAId="fra_001"` (not yet favourited) | `save_fundraising_activity` returns `True`; new `favourite` row; `save_count` on activity incremented by 1 | Matches expected | Pass |
| TC-22.2 | **Verifies a duplicate favourite returns False (no double-increment).** Same `(accountId, FRAId)` as TC-22.1 called twice in a row | Second call returns `False` (duplicate); `save_count` not incremented twice | Matches expected | Pass |
| TC-24.1 | **Verifies the donee's favourites list is returned.** `accountId="acc_003"` (donee) with 2 saved favourites against ongoing activities | `view_favourite_list` returns list of 2 `Favourite` rows | Matches expected | Pass |
| TC-24.2 | **Verifies an empty favourites list returns [].** `accountId="acc_003"` with no favourites | Returns `[]`; boundary shows "You haven't favourited any activities yet." | Matches expected | Pass |
| TC-24.3 | **Verifies favourites pointing at suspended activities are hidden (and reappear after unsuspend).** Donee favourites 2 activities; owner suspends one | First call returns only the still-active favourite (JOIN `WHERE a.suspended = 0`). After the owner unsuspends, the suspended-favourite row reappears in the list | Matches expected | Pass |

## Sprint 3 — Suspend / search profiles + accounts, suspend / search my activities, remove + search favourites, donation history, completed-activity history

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-4.1 | **Verifies an admin can suspend an existing profile.** `profile_id="prof_001"` (existing, not yet suspended) | `suspend_user_profile` returns `True`; `suspended=1` in DB | Matches expected | Pass |
| TC-4.2 | **Verifies suspend returns False when no row matches.** `profile_id="prof_999"` (missing) | Returns `False`; no row mutated | Matches expected | Pass |
| TC-5.1 | **Verifies profile search filters on role/description (case-insensitive).** `searchCriteria="admin"` against profiles with roles "admin", "donee", "fundraiser" | Returns list with only the admin profile | Matches expected | Pass |
| TC-5.2 | **Verifies profile search returns [] when nothing matches.** `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-9.1 | **Verifies a suspended account is blocked from logging in.** `account_id="acc_001"` (existing) | `suspend_user_account` returns `True`; subsequent login attempts blocked (`suspended=0` clause in login) | Matches expected | Pass |
| TC-9.2 | **Verifies account suspend returns False when no row matches.** `account_id="acc_999"` (missing) | Returns `False` | Matches expected | Pass |
| TC-10.1 | **Verifies account search filters on email/name (case-insensitive).** `searchCriteria="a@"` against accounts with emails `a001@a.com`, `fr001@a.com` | Returns the matching admin account | Matches expected | Pass |
| TC-10.2 | **Verifies account search returns [] when nothing matches.** `searchCriteria="zzz"` | Returns `[]` | Matches expected | Pass |
| TC-16.1 | **Verifies a fundraiser can suspend their own activity.** `owner_account_id="acc_002"`, `fra_id="fra_001"` (owned) | `suspend_my_fundraising_activity` returns `True`; `suspended=1` on the row | Matches expected | Pass |
| TC-16.2 | **Verifies a fundraiser cannot suspend another fundraiser's activity.** `owner_account_id="acc_003"` (wrong owner), `fra_id="fra_001"` | Returns `False`; row not mutated (cross-owner refused) | Matches expected | Pass |
| TC-17.1 | **Verifies a fundraiser's own-activity search is scoped to themselves.** `owner_account_id="acc_002"`, `searchCriteria="hospital"` with one matching owned activity | Returns list with that activity only; `WHERE owner_account_id = ?` scopes it | Matches expected | Pass |
| TC-17.2 | **Verifies own-activity search returns [] for a user with no activities.** `owner_account_id="acc_003"` (donee with no activities), `searchCriteria="anything"` | Returns `[]` | Matches expected | Pass |
| TC-23.1 | **Verifies a donee can remove a favourite (and save_count drops).** `FRAId="fra_001"`, `accountId="acc_003"` (donee with that favourite) | `remove_favourite` returns `True`; row deleted; `save_count` decremented by 1 | Matches expected | Pass |
| TC-23.2 | **Verifies remove returns False when the favourite pair doesn't exist.** `FRAId="fra_001"`, `accountId="acc_003"` with no existing favourite row | Returns `False`; `save_count` unchanged | Matches expected | Pass |
| TC-25.1 | **Verifies favourites search filters by joined-activity fields.** `accountId="acc_003"`, `searchCriteria="hospital"` with 2 favourites whose activities match | Returns list of those 2 favourites; JOINs on `fundraising_activity` + `fundraising_activity_category` and matches title/description/category_name | Matches expected | Pass |
| TC-25.2 | **Verifies favourites search returns [] when nothing matches.** `accountId="acc_003"`, `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-25.3 | **Verifies search hides favourites pointing at suspended activities.** Donee has one favourite; owner suspends its target | `search_favourite` returns `[]` even when the search term matches the activity title — same suspended-hidden rule as US-24 | Matches expected | Pass |
| TC-30.1 | **Verifies completed-activity search filters by `end_date < today` (derived `completed`, post-2026-05-18 refactor).** `owner_account_id="acc_002"`, `searchCriteria="hospital"` with 1 past-end + 1 future-end matching activity | Returns only the past-end one (`WHERE a.end_date < today`). The stored `completed` column was dropped; the entity exposes `completed` as a Python `@property`. | Matches expected | Pass |
| TC-30.2 | **Verifies completed-activity search returns [] when no past-end rows exist.** `owner_account_id="acc_003"` (no activities), `searchCriteria="hospital"` | Returns `[]` | Matches expected | Pass |
| TC-31.1 | **Verifies the full completed-activity list is returned for the owner.** `owner_account_id="acc_002"` with 2 past-end + 1 future-end activity | `view_my_completed_fundraising_activities` returns list of 2 past-end activities (same end_date filter as TC-30) | Matches expected | Pass |
| TC-31.2 | **Verifies completed-activity list returns [] when no past-end rows exist.** `owner_account_id="acc_003"` (no past-end activities) | Returns `[]` | Matches expected | Pass |
| TC-32.1 | **Verifies donation history search filters by joined-activity fields.** `accountId="acc_003"`, `searchCriteria="hospital"` with 3 seeded donations against the Hospital activity | Returns the 3 matching donations; JOINs on `fundraising_activity` + `fundraising_activity_category` and matches title/description/category_name | Matches expected | Pass |
| TC-32.2 | **Verifies donation history search returns [] when nothing matches.** `accountId="acc_003"`, `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-33.1 | **Verifies the donee can view the full list of their donations (list semantics per the 2026-05-18 diagram).** `accountId="acc_003"` with 3 seeded donations | `view_my_donation_histories` returns the list of 3 `Donation` rows | Matches expected | Pass |
| TC-33.2 | **Verifies cross-account donation access is refused.** Two donees, donations seeded for donee A; query for donee B | Returns `[]` — `WHERE account_id = ?` scopes to the caller; donee B never sees donee A's history | Matches expected | Pass |

## Sprint 4 — View/save counts, FRA category CRUD, reports

| Test Case ID | Test Data | Expected Result | Actual Result | Pass / Fail |
|---|---|---|---|---|
| TC-28.1 | **Verifies the view count for an existing activity reads back accurately.** `fra_id="fra_001"` (existing, opened by donee 3 times) | `view_fundraising_activity_view_count` returns `3` | Matches expected | Pass |
| TC-28.2 | **Verifies a missing activity yields 0 rather than raising.** `fra_id="fra_999"` (missing) | Returns `0` (graceful — `None` row maps to 0 rather than raising) | Matches expected | Pass |
| TC-29.1 | **Verifies the save count reflects current favourites.** `fra_id="fra_001"` (existing, favourited by 2 donees) | `view_fundraising_activity_save_count` returns `2` | Matches expected | Pass |
| TC-29.2 | **Verifies a missing activity yields 0 rather than raising.** `fra_id="fra_999"` (missing) | Returns `0` | Matches expected | Pass |
| TC-34.1 | **Verifies a PM can create a new fundraising-activity category.** `categoryName="Health"`, `description="Medical causes"` | New `FundraisingActivityCategory` persisted with `fra_cat_id="cat_001"`, `suspended=False` | Matches expected | Pass |
| TC-34.2 | **Verifies the boundary rejects blank input before calling the controller.** `categoryName=""` (blank) | Boundary rejects with "Category name is required"; no controller call | Matches expected | Pass |
| TC-34.3 | **Verifies the category_name UNIQUE constraint rejects a duplicate.** First create `categoryName="Health"`; then attempt second create with `categoryName="Health"` | First returns the category; second returns `None` (IntegrityError caught); boundary surfaces "A category with that name already exists." | Matches expected | Pass |
| TC-35.1 | **Verifies viewing an existing category returns the full record.** `FRACatId="cat_001"` (existing) | `view_fundraising_activity_category` returns the matching category | Matches expected | Pass |
| TC-35.2 | **Verifies viewing a missing category returns None.** `FRACatId="cat_999"` (missing) | Returns `None` | Matches expected | Pass |
| TC-36.1 | **Verifies a category update persists.** `FRACatId="cat_001"`, `updatedFRACategory` with new `categoryName` | `update_fundraising_activity_category` returns `True`; row updated | Matches expected | Pass |
| TC-36.2 | **Verifies update returns False when no row matches the id.** `FRACatId="cat_999"` (missing), valid `updatedFRACategory` | Returns `False`; no row mutated | Matches expected | Pass |
| TC-36.3 | **Verifies the category_name UNIQUE constraint rejects an update that would collide.** Two categories exist (`Health`, `Education`); attempt to update `Education`'s name to `Health` | Returns `False` (IntegrityError caught); `Education` category's name unchanged | Matches expected | Pass |
| TC-37.1 | **Verifies category search filters on name/description (case-insensitive).** `searchCriteria="health"` against categories "Health", "Education" | Returns list with only "Health" | Matches expected | Pass |
| TC-37.2 | **Verifies category search returns [] when nothing matches.** `searchCriteria="nothing"` | Returns `[]` | Matches expected | Pass |
| TC-38.1 | **Verifies a PM can suspend an existing category.** `FRACatId="cat_001"` (existing, not yet suspended) | `suspend_fundraising_activity_category` returns `True`; `suspended=1` on the row | Matches expected | Pass |
| TC-38.2 | **Verifies category suspend returns False when no row matches.** `FRACatId="cat_999"` (missing) | Returns `False` | Matches expected | Pass |
| TC-41.1 | **Verifies a daily report is generated, persisted, and aggregates correctly over the window.** `startDate=2026-01-01`, `endDate=2026-01-31`, `platformManagerId="acc_004"` | `generate_daily_report` returns a `Report` with `report_type="daily"`, aggregated totals over the window, persisted to `report` table with `report_id="rep_001"` | Matches expected | Pass |
| TC-41.2 | **Verifies an empty window aggregates to zero rather than failing.** Window with no donations / activities | Returns `Report` with zeros for all totals (graceful aggregation) | Matches expected | Pass |
| TC-41.3 | **Verifies the boundary single-date helper derives a daily window (new 2026-05-18 UX).** `window_for("daily", date(2026, 5, 14))` | Returns `(2026-05-14, 2026-05-14)` — same day twice | Matches expected | Pass |
| TC-42.1 | **Verifies a weekly report is generated with the correct report_type.** `startDate=2026-01-01`, `endDate=2026-01-07`, `platformManagerId="acc_004"` | `generate_weekly_report` returns a `Report` with `report_type="weekly"`; same shape as US-41 | Matches expected | Pass |
| TC-42.2 | **Verifies an empty week aggregates to zero rather than failing.** Empty week (no donations) | Returns `Report` with all zero totals | Matches expected | Pass |
| TC-42.3 | **Verifies the boundary helper derives the ISO Monday→Sunday week containing the picked date.** `window_for("weekly", date(2026, 5, 14))` (Thursday) | Returns `(2026-05-11, 2026-05-17)` — Monday→Sunday of the ISO week containing 2026-05-14 | Matches expected | Pass |
| TC-42.4 | **Verifies the weekly window walks backward when the picked date is the Sunday.** `window_for("weekly", date(2026, 5, 17))` (Sunday) | Returns `(2026-05-11, 2026-05-17)` — same Mon→Sun week (does not roll forward to the next week) | Matches expected | Pass |
| TC-43.1 | **Verifies a monthly report is generated with the correct report_type.** `startDate=2026-01-01`, `endDate=2026-01-31`, `platformManagerId="acc_004"` | `generate_monthly_report` returns a `Report` with `report_type="monthly"`; same shape as US-41/42 | Matches expected | Pass |
| TC-43.2 | **Verifies an empty month aggregates to zero rather than failing.** Empty month (no donations) | Returns `Report` with all zero totals | Matches expected | Pass |
| TC-43.3 | **Verifies the boundary helper derives the first→last day of the month containing the picked date.** `window_for("monthly", date(2026, 5, 14))` | Returns `(2026-05-01, 2026-05-31)` | Matches expected | Pass |
| TC-43.4 | **Verifies the monthly window handles variable-length February (leap vs non-leap year).** `window_for("monthly", date(2024, 2, 14))` and `window_for("monthly", date(2025, 2, 14))` | Returns `(2024-02-01, 2024-02-29)` for the leap year and `(2025-02-01, 2025-02-28)` for the non-leap year | Matches expected | Pass |

---

## Coverage summary

| Sprint | USes covered | Test cases |
|---|---|---|
| Sprint 1 | 12 | 27 |
| Sprint 2 | 9 | 24 |
| Sprint 3 | 12 | 25 |
| Sprint 4 | 10 | 27 |
| **Total** | **43** | **103** |

**Every user story has at least one positive and one negative test case.** Negative-path cases cover the failure branches the diagrams imply: missing row → `None`/`False`/`[]`, cross-owner access refused, blank inputs rejected by Boundary, the three UNIQUE constraints (`user_account.email`, `user_profile.role`, `fundraising_activity_category.category_name`) rejecting duplicates, the suspended-hidden filter on the four donee-facing read paths (US-20, US-21, US-24, US-25), past-date guards on create/update (US-13/US-15), and graceful no-op behaviour for logout-when-not-signed-in.

For each diagram-defined Entity method, the corresponding pytest happy + negative tests live in `tests/test_<entity>.py`. Controller delegation tests live in `tests/test_<controller>_controller.py`. Per-US Boundary smoke tests live in `tests/test_<page>_page.py`. The pytest suite passes (**404 tests** as of 2026-05-18) — that's the underlying evidence behind every "Pass" entry above.
