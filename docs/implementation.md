# Implementation Reference — Sprint 1 + Sprint 2

A complete index of what is implemented in the codebase as of Sprint 2. Cross-references every file, class, method, and the user story it serves. For deferred work and known shortcuts, see [todo.md](todo.md). For architecture rules, see [../CLAUDE.md](../CLAUDE.md).

---

## 1. Stack & tooling

| Concern | Choice |
|---|---|
| Language | Python 3 |
| UI | Streamlit (`layout="wide"`) |
| Persistence | SQLite via stdlib `sqlite3` (single file `app.db`) |
| Tests | pytest (43 tests as of Sprint 2) |
| Seed data | Faker — `RECORD_COUNT` rows per table (default 10 for fast dev; bump to 100 for the marking demo) |
| CI | GitHub Actions |

## 2. Directory layout

```
SDM-code/
├── app.py                     # Streamlit entry + sidebar router (16 pages)
├── boundary/                  # 16 Boundary classes (incl. InfoPage debug utility)
├── controller/                # 15 Controller classes
├── entity/                    # 4 Entity classes
├── persistence/               # db.py + schema.sql
├── data/seed.py               # record generator (RECORD_COUNT, default 10)
├── tests/                     # 43 pytest tests
├── docs/                      # implementation.md + todo.md
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

---

## 4. Entity layer ([entity/](../entity/))

Four entities. Each owns its SQL via `persistence.db.get_connection()`.

### `UserProfile` — [entity/user_profile.py](../entity/user_profile.py)
Fields: `role: str`, `description: str`, `profile_id: int | None`, `suspended: bool`.
- `create_profile(role, description) -> UserProfile | None` (classmethod) — US-1
- `view_all_profiles() -> list[UserProfile]` (classmethod, **not yet in class diagram**)
- `view_user_profile(profile_id) -> UserProfile | None` (classmethod) — US-2
- `update_user_profile(profile_id, updated_profile) -> bool` (classmethod) — US-3

### `UserAccount` — [entity/user_account.py](../entity/user_account.py)
Fields: `email, password, name, dob, phone_num, profile_id, account_id, suspended`.
- `login(email, password) -> UserAccount | None` (classmethod) — US-11/18/26/39
- `create_account(email, password, name, dob, phone_num, profile_id) -> UserAccount | None` (classmethod) — US-6. Returns None on duplicate email
- `view_user_account(account_id) -> UserAccount | None` (classmethod) — US-7
- `view_all_user_accounts() -> list[UserAccount]` (classmethod, **not yet in class diagram**)
- `update_user_account(account_id, updated_account) -> bool` (classmethod) — US-8

### `FundraisingActivity` — [entity/fundraising_activity.py](../entity/fundraising_activity.py)
Fields: `title, description, target_amount, category, start_date, end_date, status, activity_id, owner_account_id`.
- `save_fundraising_activity() -> bool` (instance method) — US-13
- `view_fundraising_activity_details(activity_id) -> FundraisingActivity | None` (classmethod) — US-21
- `view_all_fundraising_activities() -> list[FundraisingActivity]` (classmethod, **not yet in class diagram**)
- `view_fundraiser_activity(activity_id) -> FundraisingActivity | None` (classmethod) — US-14
- `view_activities_by_owner(owner_account_id) -> list[FundraisingActivity]` (classmethod, **not yet in class diagram**)
- `update_fundraiser_activity(activity_id, updated_fundraiser) -> bool` (classmethod) — US-15
- `submit_search_criteria(search_criteria) -> list[FundraisingActivity]` (classmethod, LIKE on title/description/category) — US-20

### `FavouriteList` — [entity/favourite_list.py](../entity/favourite_list.py) (NEW Sprint 2)
Fields: `account_id: int`, `activity_id: int`. Composite PK (account_id, activity_id) with ON DELETE CASCADE.
- `save_fundraising_activity(account_id, activity_id) -> bool` (classmethod) — US-22. Returns False on duplicate or FK violation
- `view_favourite_list(account_id) -> list[FavouriteList]` (classmethod) — US-24
- `remove_favourite(account_id, activity_id) -> bool` (classmethod, **not yet in class diagram** — foreshadows US-23)

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
| `SearchFundraiserActivityController` | `submit_search_criteria(search_criteria)` | `FundraisingActivity.submit_search_criteria` |
| `SaveFundraiserActivityController` | `save_fundraising_activity(account_id, activity_id)` | `FavouriteList.save_fundraising_activity` |
| `ViewFavouriteListController` | `view_favourite_list(account_id)` | `FavouriteList.view_favourite_list` |

Pragmatic methods not yet on any class diagram (logged in [todo.md](todo.md) for diagram catchup):
- `view_all_profiles`, `view_all_fundraising_activities`, `view_all_user_accounts`, `view_activities_by_owner`, `remove_favourite`

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

---

## 7. Persistence ([persistence/](../persistence/))

### [persistence/schema.sql](../persistence/schema.sql)

| Table | Columns | Notes |
|---|---|---|
| `user_profile` | `profile_id` (PK, AUTOINC), `role`, `description`, `suspended` | |
| `user_account` | `account_id` (PK, AUTOINC), `email` (UNIQUE NOT NULL), `password`, `name`, `dob`, `phone_num`, `profile_id` (FK), `suspended` | **Sprint 2 migration:** `account_id` added; `email` demoted from PK to UNIQUE |
| `fundraising_activity` | `activity_id` (PK, AUTOINC), `title`, `description`, `target_amount`, `category`, `start_date`, `end_date`, `status`, `owner_account_id` (FK) | **Sprint 2 migration:** `owner_email` → `owner_account_id` |
| `favourite_list` | `account_id` (FK), `activity_id` (FK), composite PK | **NEW Sprint 2.** `ON DELETE CASCADE` on both FKs |

### [persistence/db.py](../persistence/db.py)
- `get_connection() -> sqlite3.Connection` — row factory `Row`, foreign keys ON
- `init_db() -> None` — runs `schema.sql`

---

## 8. Application entry ([app.py](../app.py))

Streamlit entry. `layout="wide"`. Sidebar shows sign-in status and a radio for the 16 pages, prefixed by actor (`[Admin]`, `[Fundraiser]`, `[Donee]`, plus `.info (debug)`). No role-based gating yet — see [todo.md](todo.md).

---

## 9. Tests ([tests/](../tests/))

43 tests, all green.

| File | What it covers |
|---|---|
| [tests/conftest.py](../tests/conftest.py) | `fresh_db` autouse fixture — fresh schema before every test |
| [tests/test_user_profile.py](../tests/test_user_profile.py) | create / view / view-all / update / update-missing-id |
| [tests/test_user_account.py](../tests/test_user_account.py) | create / duplicate / login / view / view-all / update / update-missing-id |
| [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) | save / view-details / view-all / view-fundraiser-activity / view-by-owner / update / search |
| [tests/test_favourite_list.py](../tests/test_favourite_list.py) | save / duplicate / view-empty / remove |
| [tests/test_controllers.py](../tests/test_controllers.py) | Sprint 1 controller delegation contracts |
| [tests/test_sprint2_controllers.py](../tests/test_sprint2_controllers.py) | All 9 Sprint 2 controllers — pure-delegation pin |

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

See [todo.md](todo.md) for the full list. Highlights still deferred after Sprint 2:

- Password hashing (any sprint, hardening)
- Role-based menu / route guards
- US-4 / US-5, US-9 / US-10 (admin suspend & search)
- US-16 / US-17 (fundraiser suspend & search FSA)
- US-23 / US-25 (donee delete-favourite & search-favourites — `remove_favourite` already coded as helper)
- US-28..US-33 (analytics / history)
- US-34..US-38 (platform manager category management) — categories still hardcoded
- US-41..US-43 (reports)
