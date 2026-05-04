# Implementation Reference — Sprint 1 + Sprint 2 + Sprint 3

A complete index of what is implemented in the codebase as of Sprint 3. Cross-references every file, class, method, and the user story it serves. For deferred work and known shortcuts, see [todo.md](todo.md). For active design gaps, see [issues.md](issues.md). For architecture rules, see [../CLAUDE.md](../CLAUDE.md).

---

## 1. Stack & tooling

| Concern | Choice |
|---|---|
| Language | Python 3 |
| UI | Streamlit (`layout="wide"`) |
| Persistence | SQLite via stdlib `sqlite3` (single file `app.db`) |
| Tests | pytest (68 tests as of Sprint 3) |
| Seed data | Faker — `RECORD_COUNT` rows per table (default 10 for fast dev; bump to 100 for the marking demo) |
| CI | GitHub Actions |

## 2. Directory layout

```
SDM-code/
├── app.py                     # Streamlit entry + sidebar router (26 pages)
├── boundary/                  # 26 Boundary classes (incl. InfoPage debug utility)
├── controller/                # 25 Controller classes
├── entity/                    # 4 Entity classes
├── persistence/               # db.py + schema.sql (unchanged in Sprint 3)
├── data/seed.py               # record generator (RECORD_COUNT, default 10)
├── tests/                     # 68 pytest tests
├── docs/                      # implementation.md + todo.md + issues.md + differences.md
├── diagrams/                  # source UML class + sequence diagrams (per sprint)
├── .github/workflows/ci.yml   # pytest on push/PR
├── requirements.txt
├── README.md
├── CLAUDE.md
└── .gitignore
```

## 3. User-story coverage

### Sprint 1 — 12 stories

| US | Story | Boundary | Controller | Entity method |
|---|---|---|---|---|
| US-1  | Admin: create user profile | `CreateProfilePage` | `CreateProfileController` | `UserProfile.create_profile` |
| US-6  | Admin: create user account | `CreateAccountPage` | `CreateAccountController` + `ViewProfilesController` | `UserAccount.create_account`, `UserProfile.view_all_profiles` |
| US-11 | Admin: log in | `LoginPage` | `LoginController` | `UserAccount.login` |
| US-12 | Admin: log out | `LogoutPage` | — | — |
| US-13 | Fundraiser: create fundraising activity | `CreateFundraisingActivityPage` | `CreateFundraisingActivityController` | `FundraisingActivity.save_fundraising_activity` |
| US-18 | Fundraiser: log in | `LoginPage` (shared) | `LoginController` | `UserAccount.login` |
| US-19 | Fundraiser: log out | `LogoutPage` (shared) | — | — |
| US-21 | Donee: view fundraising activity | `ViewFundraisingActivityPage` | `ViewFundraisingActivityController` | `FundraisingActivity.view_fundraising_activity_details` |
| US-26 | Donee: log in | `LoginPage` (shared) | `LoginController` | `UserAccount.login` |
| US-27 | Donee: log out | `LogoutPage` (shared) | — | — |
| US-39 | Platform Manager: log in | `LoginPage` (shared) | `LoginController` | `UserAccount.login` |
| US-40 | Platform Manager: log out | `LogoutPage` (shared) | — | — |

### Sprint 2 — 9 stories

| US | Story | Boundary | Controller | Entity method |
|---|---|---|---|---|
| US-2  | Admin: view user profile | `ViewUserProfilePage` | `ViewUserProfileController` | `UserProfile.view_user_profile` |
| US-3  | Admin: update user profile | `UpdateUserProfilePage` | `UpdateUserProfileController` | `UserProfile.update_user_profile` |
| US-7  | Admin: view user account | `ViewUserAccountPage` | `ViewUserAccountController` | `UserAccount.view_user_account` |
| US-8  | Admin: update user account | `UpdateUserAccountPage` | `UpdateUserAccountController` | `UserAccount.update_user_account` |
| US-14 | Fundraiser: view their FSA | `ViewFundraiserActivityPage` | `ViewFundraiserActivityController` | `FundraisingActivity.view_fundraiser_activity` |
| US-15 | Fundraiser: update their FSA | `UpdateFundraiserActivityPage` | `UpdateFundraiserActivityController` | `FundraisingActivity.update_fundraiser_activity` |
| US-20 | Donee: search FSAs | `SearchFundraiserActivityPage` | `SearchFundraiserActivityController` | `FundraisingActivity.submit_search_criteria` |
| US-22 | Donee: save FSA to favourites | `SaveFundraiserActivityPage` | `SaveFundraiserActivityController` | `FavouriteList.save_fundraising_activity` |
| US-24 | Donee: view favourites list | `ViewFavouriteListPage` | `ViewFavouriteListController` | `FavouriteList.view_favourite_list` |

### Sprint 3 — 10 stories

| US | Story | Boundary | Controller | Entity method |
|---|---|---|---|---|
| US-4  | Admin: delete user profile | `DeleteUserProfilePage` | `DeleteUserProfileController` | `UserProfile.delete_user_profile` |
| US-5  | Admin: search user profiles | `SearchUserProfilePage` | `SearchUserProfileController` | `UserProfile.submit_search_criteria` |
| US-9  | Admin: suspend user account | `SuspendUserAccountPage` | `SuspendUserAccountController` | `UserAccount.suspend_user_account` |
| US-10 | Admin: search user accounts | `SearchUserAccountPage` | `SearchUserAccountController` | `UserAccount.submit_search_criteria` |
| US-16 | Fundraiser: suspend their FSA | `SuspendFundraisingActivityPage` | `SuspendFundraisingActivityController` | `FundraisingActivity.suspend_fundraising_activity` |
| US-17 | Fundraiser: search their FSAs | `SearchFundraisingActivityPage` | `SearchFundraisingActivityController` | `FundraisingActivity.submit_search_criteria` (with `owner_account_id`) |
| US-23 | Donee: delete a favourite | `DeleteFavouritePage` | `DeleteFavouriteController` | `FavouriteList.delete_favourite` |
| US-25 | Donee: search favourites | `SearchFavouritePage` | `SearchFavouriteController` | `FavouriteList.submit_search_criteria` (with `account_id`) |
| US-30 | Fundraiser: search completed FSAs | `SearchCompletedActivityPage` | `SearchCompletedActivityController` | `FundraisingActivity.submit_search_criteria` (with `owner_account_id`, `status="completed"`) |
| US-31 | Fundraiser: view completed FSA | `ViewCompletedActivityPage` | `ViewCompletedActivityController` | `FundraisingActivity.view_completed_activity` |

US-32 and US-33 (donee donation history) were planned for Sprint 3 but deferred to Sprint 4 — donations are not yet modelled. See [issues.md](issues.md).

---

## 4. Entity layer ([entity/](../entity/))

Four entities. Each owns its SQL via `persistence.db.get_connection()`.

### `UserProfile` — [entity/user_profile.py](../entity/user_profile.py)
Fields: `role: str`, `description: str`, `profile_id: int | None`, `suspended: bool`.
- `create_profile(role, description) -> UserProfile | None` (classmethod) — US-1
- `view_all_profiles() -> list[UserProfile]` (classmethod, **not yet in class diagram**)
- `view_user_profile(profile_id) -> UserProfile | None` (classmethod) — US-2
- `update_user_profile(profile_id, updated_profile) -> bool` (classmethod) — US-3
- `delete_user_profile(profile_id) -> bool` (classmethod) — US-4. Returns False on FK violation when an account references the profile
- `submit_search_criteria(search_criteria) -> list[UserProfile]` (classmethod) — US-5. LIKE on role/description

### `UserAccount` — [entity/user_account.py](../entity/user_account.py)
Fields: `email, password, name, dob, phone_num, profile_id, account_id, suspended`.
- `login(email, password) -> UserAccount | None` (classmethod) — US-11/18/26/39. Suspended accounts are rejected
- `create_account(email, password, name, dob, phone_num, profile_id) -> UserAccount | None` (classmethod) — US-6. Returns None on duplicate email
- `view_user_account(account_id) -> UserAccount | None` (classmethod) — US-7
- `view_all_user_accounts() -> list[UserAccount]` (classmethod, **not yet in class diagram**)
- `update_user_account(account_id, updated_account) -> bool` (classmethod) — US-8
- `suspend_user_account(account_id) -> bool` (classmethod) — US-9. Sets `suspended=1`; future logins blocked
- `submit_search_criteria(search_criteria) -> list[UserAccount]` (classmethod) — US-10. LIKE on email/name

### `FundraisingActivity` — [entity/fundraising_activity.py](../entity/fundraising_activity.py)
Fields: `title, description, target_amount, category, start_date, end_date, status, activity_id, owner_account_id`.
- `save_fundraising_activity() -> bool` (instance method) — US-13
- `view_fundraising_activity_details(activity_id) -> FundraisingActivity | None` (classmethod) — US-21
- `view_all_fundraising_activities() -> list[FundraisingActivity]` (classmethod, **not yet in class diagram**)
- `view_fundraiser_activity(activity_id) -> FundraisingActivity | None` (classmethod) — US-14
- `view_activities_by_owner(owner_account_id) -> list[FundraisingActivity]` (classmethod, **not yet in class diagram**)
- `update_fundraiser_activity(activity_id, updated_fundraiser) -> bool` (classmethod) — US-15
- `submit_search_criteria(search_criteria, owner_account_id=None, status=None) -> list[FundraisingActivity]` (classmethod, LIKE on title/description/category, optional filters) — US-17/US-20/US-30. **Sprint 3 widened the diagram signature; see todo.md.**
- `suspend_fundraising_activity(activity_id) -> bool` (classmethod) — US-16. Sets `status='suspended'`
- `view_completed_activity(activity_id) -> FundraisingActivity | None` (classmethod) — US-31. Returns None unless `status='completed'`

### `FavouriteList` — [entity/favourite_list.py](../entity/favourite_list.py) (NEW Sprint 2, extended Sprint 3)
Fields: `account_id: int`, `activity_id: int`. Composite PK (account_id, activity_id) with ON DELETE CASCADE.
- `save_fundraising_activity(account_id, activity_id) -> bool` (classmethod) — US-22. Returns False on duplicate or FK violation
- `view_favourite_list(account_id) -> list[FavouriteList]` (classmethod) — US-24
- `delete_favourite(activity_id, account_id) -> bool` (classmethod) — US-23. Note diagram-matching param order `(activityId, accountId)`. Replaces the Sprint 2 `remove_favourite` placeholder
- `submit_search_criteria(search_criteria, account_id=None) -> list[FavouriteList]` (classmethod) — US-25. JOINs onto fundraising_activity for the LIKE; `account_id` scopes to one donee (Sprint 3 added the param; see todo.md)

---

## 5. Controller layer ([controller/](../controller/))

All controllers are pure delegators: each method is a one-liner that calls one Entity method.

| Controller | Method | Delegates to |
|---|---|---|
| `LoginController` | `login(email, password)` | `UserAccount.login` |
| `CreateProfileController` | `create_profile(role, description)` | `UserProfile.create_profile` |
| `CreateAccountController` | `create_account(...)` | `UserAccount.create_account` |
| `CreateFundraisingActivityController` | `create_fundraising_activity(...)` | `FundraisingActivity.save_fundraising_activity` |
| `ViewFundraisingActivityController` | `view_fundraising_activity_details(activity_id)` | `FundraisingActivity.view_fundraising_activity_details` |
| `ViewFundraisingActivityController` | `view_all_fundraising_activities()` | `FundraisingActivity.view_all_fundraising_activities` |
| `ViewProfilesController` | `view_all_profiles()` | `UserProfile.view_all_profiles` |
| `ViewUserProfileController` | `view_user_profile(profile_id)` | `UserProfile.view_user_profile` |
| `UpdateUserProfileController` | `update_user_profile(profile_id, updated_profile)` | `UserProfile.update_user_profile` |
| `ViewUserAccountController` | `view_user_account(account_id)` | `UserAccount.view_user_account` |
| `ViewUserAccountController` | `view_all_user_accounts()` | `UserAccount.view_all_user_accounts` |
| `UpdateUserAccountController` | `update_user_account(account_id, updated_account)` | `UserAccount.update_user_account` |
| `ViewFundraiserActivityController` | `view_fundraiser_activity(activity_id)` | `FundraisingActivity.view_fundraiser_activity` |
| `ViewFundraiserActivityController` | `view_activities_by_owner(owner_account_id)` | `FundraisingActivity.view_activities_by_owner` |
| `UpdateFundraiserActivityController` | `update_fundraiser_activity(activity_id, updated)` | `FundraisingActivity.update_fundraiser_activity` |
| `SearchFundraiserActivityController` | `submit_search_criteria(search_criteria, owner_account_id=None, status=None)` | `FundraisingActivity.submit_search_criteria` |
| `SaveFundraiserActivityController` | `save_fundraising_activity(account_id, activity_id)` | `FavouriteList.save_fundraising_activity` |
| `ViewFavouriteListController` | `view_favourite_list(account_id)` | `FavouriteList.view_favourite_list` |
| `DeleteUserProfileController` | `delete_user_profile(profile_id)` | `UserProfile.delete_user_profile` |
| `SearchUserProfileController` | `submit_search_criteria(search_criteria)` | `UserProfile.submit_search_criteria` |
| `SuspendUserAccountController` | `suspend_user_account(account_id)` | `UserAccount.suspend_user_account` |
| `SearchUserAccountController` | `submit_search_criteria(search_criteria)` | `UserAccount.submit_search_criteria` |
| `SuspendFundraisingActivityController` | `suspend_fundraising_activity(activity_id)` | `FundraisingActivity.suspend_fundraising_activity` |
| `SearchFundraisingActivityController` | `submit_search_criteria(search_criteria, owner_account_id=None, status=None)` | `FundraisingActivity.submit_search_criteria` |
| `DeleteFavouriteController` | `delete_favourite(activity_id, account_id)` | `FavouriteList.delete_favourite` |
| `SearchFavouriteController` | `submit_search_criteria(search_criteria, account_id=None)` | `FavouriteList.submit_search_criteria` |
| `SearchCompletedActivityController` | `submit_search_criteria(search_criteria, owner_account_id=None, status=None)` | `FundraisingActivity.submit_search_criteria` |
| `ViewCompletedActivityController` | `view_completed_activity(activity_id)` | `FundraisingActivity.view_completed_activity` |

Pragmatic methods not yet on any class diagram (logged in [todo.md](todo.md) for diagram catchup):
- `view_all_profiles`, `view_all_fundraising_activities`, `view_all_user_accounts`, `view_activities_by_owner`
- Sprint 3 signature additions on `submit_search_criteria` (FundraisingActivity gains `owner_account_id`/`status`; FavouriteList gains `account_id`)

---

## 6. Boundary layer ([boundary/](../boundary/))

All input/format validation lives here. None of these classes import from `entity/` directly — they go through Controllers.

### Sprint 1 (unchanged behaviour, new account_id wiring)

- `LoginPage` — US-11/18/26/39
- `LogoutPage` — US-12/19/27/40 (self-contained, no Controller per diagram)
- `CreateProfilePage` — US-1
- `CreateAccountPage` — US-6 (profile picked via dropdown sourced from `ViewProfilesController`)
- `CreateFundraisingActivityPage` — US-13 (now stamps `owner_account_id` from `st.session_state["user"].account_id`)
- `ViewFundraisingActivityPage` — US-21 (clickable table → details + back)
- `InfoPage` — debug utility (row-click delete with FK error handling); hide before final demo

### Sprint 2 (new)

- `ViewUserProfilePage` — US-2. Click-to-select table of profiles → details panel
- `UpdateUserProfilePage` — US-3. Select profile → pre-filled form → save / cancel
- `ViewUserAccountPage` — US-7. Click-to-select table of accounts → details panel
- `UpdateUserAccountPage` — US-8. Select account → pre-filled form (profile dropdown reused, dob converted to `date.fromisoformat`)
- `ViewFundraiserActivityPage` — US-14. Scoped to `st.session_state["user"].account_id`. Ownership check on detail view
- `UpdateFundraiserActivityPage` — US-15. Same ownership scoping. Reuses `DEFAULT_CATEGORIES` from `CreateFundraisingActivityPage`
- `SearchFundraiserActivityPage` — US-20. Free-text search → results table
- `SaveFundraiserActivityPage` — US-22. Donee picks an FSA from the public list → favourite saved (idempotent: duplicates display "already in your favourites")
- `ViewFavouriteListPage` — US-24. Joins favourites with FSA details into a single table

### Sprint 3 (new)

- `DeleteUserProfilePage` — US-4. Profile dropdown → delete button → success/error (FK violation reported as "in use by an existing account")
- `SearchUserProfilePage` — US-5. Free-text search on role/description → results table
- `SuspendUserAccountPage` — US-9. Active-account dropdown → suspend button. Already-suspended accounts excluded from the dropdown
- `SearchUserAccountPage` — US-10. Free-text search on email/name → results table
- `SuspendFundraisingActivityPage` — US-16. Dropdown of the fundraiser's non-suspended activities → suspend button. Owner scoped via `st.session_state["user"].account_id`
- `SearchFundraisingActivityPage` — US-17. Owner-scoped free-text search → results table. Distinct from the Sprint 2 `SearchFundraiserActivityPage` (donee, all activities)
- `DeleteFavouritePage` — US-23. Dropdown of the donee's favourites → delete button. Account scoped via session
- `SearchFavouritePage` — US-25. Free-text search on linked activity's title/description/category → results joined with activity details
- `SearchCompletedActivityPage` — US-30. Owner-scoped + `status="completed"` → results table
- `ViewCompletedActivityPage` — US-31. Lists fundraiser's completed activities → click row for details. Detail view also enforces ownership

### Method names that mirror the diagrams' message arrows
- `LoginPage.display_success / display_error`
- `CreateProfilePage.display_success / display_error`
- `CreateAccountPage.display_success / display_error`
- `CreateFundraisingActivityPage.validate_fundraising_activity / display_fundraising_activity_confirmation / display_fundraising_activity_validation_error`
- `ViewFundraisingActivityPage.select_fundraising_activity / display_fundraising_activity_details`
- `ViewUserProfilePage.click_user_profile / display_user_profile`
- `UpdateUserProfilePage.click_edit_option / display_update_page / display_success / display_error`
- `ViewUserAccountPage.click_user_account / display_user_account`
- `UpdateUserAccountPage.click_edit_option / display_update_page / display_success / display_error`
- `ViewFundraiserActivityPage.click_fundraising_activity / display_fundraising_activity`
- `UpdateFundraiserActivityPage.click_edit_option / display_update_page / display_success / display_error`
- `SearchFundraiserActivityPage.display_search_page / display_matching_fundraising_activities`
- `SaveFundraiserActivityPage.click_save_option / display_success`
- `ViewFavouriteListPage.display_favourite_list`
- `DeleteUserProfilePage.click_delete_button / display_success / display_error`
- `SearchUserProfilePage.display_search_page / display_matching_user_profile`
- `SuspendUserAccountPage.click_suspend_user_account_option / display_success / display_error`
- `SearchUserAccountPage.display_search_page / display_matching_user_account`
- `SuspendFundraisingActivityPage.click_suspend_fundraising_activity_option / display_success / display_error`
- `SearchFundraisingActivityPage.display_search_page / display_matching_fundraising_activity`
- `DeleteFavouritePage.click_delete_favourite_option / display_success / display_error`
- `SearchFavouritePage.display_search_page / display_matching_favourite`
- `SearchCompletedActivityPage.display_search_page / display_matching_completed_activity`
- `ViewCompletedActivityPage.click_completed_activity / display_completed_activity`

---

## 7. Persistence ([persistence/](../persistence/))

### [persistence/schema.sql](../persistence/schema.sql)

| Table | Columns | Notes |
|---|---|---|
| `user_profile` | `profile_id` (PK, AUTOINC), `role`, `description`, `suspended` | |
| `user_account` | `account_id` (PK, AUTOINC), `email` (UNIQUE NOT NULL), `password`, `name`, `dob`, `phone_num`, `profile_id` (FK), `suspended` | **Sprint 2 migration:** `account_id` added; `email` demoted from PK to UNIQUE |
| `fundraising_activity` | `activity_id` (PK, AUTOINC), `title`, `description`, `target_amount`, `category`, `start_date`, `end_date`, `status`, `owner_account_id` (FK) | **Sprint 2 migration:** `owner_email` → `owner_account_id` |
| `favourite_list` | `account_id` (FK), `activity_id` (FK), composite PK | **NEW Sprint 2.** `ON DELETE CASCADE` on both FKs |

Sprint 3 added no new tables or columns — `status` and `suspended` were already present.

### [persistence/db.py](../persistence/db.py)
- `get_connection() -> sqlite3.Connection` — row factory `Row`, foreign keys ON
- `init_db() -> None` — runs `schema.sql`

---

## 8. Application entry ([app.py](../app.py))

Streamlit entry. `layout="wide"`. Sidebar shows sign-in status and a radio for the 26 pages, prefixed by actor (`[Admin]`, `[Fundraiser]`, `[Donee]`, plus `.info (debug)`). No role-based gating yet — see [issues.md](issues.md) ("Admin pages have no authentication / RBAC gate").

---

## 9. Tests ([tests/](../tests/))

68 tests, all green.

| File | What it covers |
|---|---|
| [tests/conftest.py](../tests/conftest.py) | `fresh_db` autouse fixture — fresh schema before every test |
| [tests/test_user_profile.py](../tests/test_user_profile.py) | create / view / view-all / update / update-missing-id; **Sprint 3:** delete / delete-with-FK / search |
| [tests/test_user_account.py](../tests/test_user_account.py) | create / duplicate / login / view / view-all / update / update-missing-id; **Sprint 3:** suspend / suspend-blocks-login / search |
| [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) | save / view-details / view-all / view-fundraiser-activity / view-by-owner / update / search; **Sprint 3:** suspend / view-completed / search-by-owner / search-by-status / search-by-owner-and-status |
| [tests/test_favourite_list.py](../tests/test_favourite_list.py) | save / duplicate / view-empty; **Sprint 3:** delete-favourite / delete-no-match / search-by-text-and-account |
| [tests/test_controllers.py](../tests/test_controllers.py) | Sprint 1 controller delegation contracts |
| [tests/test_sprint2_controllers.py](../tests/test_sprint2_controllers.py) | All 9 Sprint 2 controllers — pure-delegation pin |
| [tests/test_sprint3_controllers.py](../tests/test_sprint3_controllers.py) | All 10 Sprint 3 controllers — pure-delegation pin |

Run with `pytest`.

---

## 10. Seed data ([data/seed.py](../data/seed.py))

Idempotent (drops & recreates `app.db`). Row counts are governed by `RECORD_COUNT` at the top of the file (default **10**, intended to be bumped to **100** before the marking demo per the project spec). Populates:

- `RECORD_COUNT` user profiles (random role + Faker sentence)
- `RECORD_COUNT` user accounts (Faker name/email/dob/phone, password `password123`, random profile FK)
- `RECORD_COUNT` fundraising activities (random category/status/dates/amount, random `owner_account_id` FK)
- `RECORD_COUNT * 2` favourite-list save attempts (deduped by composite PK)

Run with `python -m data.seed`.

---

## 11. CI ([.github/workflows/ci.yml](../.github/workflows/ci.yml))

Triggers: push or PR to `main` / `master`. Steps: checkout → Python 3.11 → install deps → `pytest -v`. Satisfies the project's CI/CD evidence requirement once the repo is pushed.

---

## 12. Conventions enforced

See [../CLAUDE.md](../CLAUDE.md) for the full list including the two documented exceptions (pragmatic Entity extensions for UX, and debug-only utilities).

---

## 13. What is **not** implemented (intentional)

See [todo.md](todo.md) for the full list and [issues.md](issues.md) for active design gaps. Highlights still deferred after Sprint 3:

- Password hashing (any sprint, hardening)
- Role-based menu / route guards — admin pages currently reachable by anonymous visitors. Tracked as **High** in [issues.md](issues.md)
- Entity-layer ownership check on `update_fundraiser_activity` and `suspend_fundraising_activity` — boundary filters today, no defense-in-depth. Tracked as **Medium** in [issues.md](issues.md)
- US-28 / US-29 (FSA view & favourite counts) — Sprint 4
- US-32 / US-33 (donee donation-history search & view) — blocked on a `donation` entity + table; deferred to Sprint 4 alongside the donate flow ([issues.md](issues.md))
- US-34..US-38 (platform manager category management) — categories still hardcoded
- US-41..US-43 (reports)
