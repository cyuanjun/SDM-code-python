# Implementation Reference — Sprint 1

A complete index of what is implemented in the codebase as of Sprint 1. Cross-references every file, class, method, and the user story it serves. For deferred work and known shortcuts, see [todo.md](todo.md). For architecture rules, see [../CLAUDE.md](../CLAUDE.md).

---

## 1. Stack & tooling

| Concern | Choice |
|---|---|
| Language | Python 3 |
| UI | Streamlit |
| Persistence | SQLite via stdlib `sqlite3` (single file `app.db`) |
| Tests | pytest |
| Seed data | Faker |
| CI | GitHub Actions |

## 2. Directory layout

```
SDM-code/
├── app.py                     # Streamlit entry + sidebar router (wide layout)
├── boundary/                  # 7 Boundary classes (incl. InfoPage debug utility)
├── controller/                # 6 Controller classes
├── entity/                    # 3 Entity classes
├── persistence/               # db.py + schema.sql
├── data/seed.py               # 100/100/100 record generator
├── tests/                     # 17 pytest tests
├── docs/                      # implementation.md + todo.md
├── .github/workflows/ci.yml   # pytest on push/PR
├── requirements.txt
├── README.md
├── CLAUDE.md                  # durable conventions for Claude/team
└── .gitignore
```

## 3. Sprint 1 coverage — 12 user stories

| US | Story | Boundary | Controller | Entity method |
|---|---|---|---|---|
| US-1  | Admin: create user profile | `CreateProfilePage` | `CreateProfileController` | `UserProfile.create_profile` |
| US-6  | Admin: create user account | `CreateAccountPage` | `CreateAccountController` + `ViewProfilesController` | `UserAccount.create_account`, `UserProfile.view_all_profiles` |
| US-11 | Admin: log in | `LoginPage` | `LoginController` | `UserAccount.login` |
| US-12 | Admin: log out | `LogoutPage` | — (self-clear in Boundary per diagram) | — |
| US-13 | Fundraiser: create fundraising activity | `CreateFundraisingActivityPage` | `CreateFundraisingActivityController` | `FundraisingActivity.save_fundraising_activity` |
| US-18 | Fundraiser: log in | `LoginPage` (shared) | `LoginController` | `UserAccount.login` |
| US-19 | Fundraiser: log out | `LogoutPage` (shared) | — | — |
| US-21 | Donee: view fundraising activity | `ViewFundraisingActivityPage` | `ViewFundraisingActivityController` | `FundraisingActivity.view_fundraising_activity_details` |
| US-26 | Donee: log in | `LoginPage` (shared) | `LoginController` | `UserAccount.login` |
| US-27 | Donee: log out | `LogoutPage` (shared) | — | — |
| US-39 | Platform Manager: log in | `LoginPage` (shared) | `LoginController` | `UserAccount.login` |
| US-40 | Platform Manager: log out | `LogoutPage` (shared) | — | — |

12 stories, 6 unique flows, because the 4 login stories share one diagram and the 4 logout stories share one diagram.

---

## 4. Boundary layer ([boundary/](../boundary/))

All input/format validation lives here. None of these classes import from `entity/` directly — they go through Controllers.

### `LoginPage` — [boundary/login_page.py](../boundary/login_page.py)
Covers US-11, US-18, US-26, US-39. Streamlit form with email + password. Validates non-empty + `@` in email. Calls `LoginController().login(...)`. Stores returned `UserAccount` in `st.session_state["user"]` on success.
- `render() -> None`
- `display_success() -> None`
- `display_error() -> None`

### `LogoutPage` — [boundary/logout_page.py](../boundary/logout_page.py)
Covers US-12, US-19, US-27, US-40. Self-contained per diagram: clears session state and reruns. No Controller/Entity.
- `render() -> None`
- `logout() -> None`

### `CreateProfilePage` — [boundary/create_profile_page.py](../boundary/create_profile_page.py)
Covers US-1. Free-text inputs for `role` (`String` per diagram) and `description`. Validates non-empty.
- `render() -> None`
- `display_success() / display_error() -> None`

### `CreateAccountPage` — [boundary/create_account_page.py](../boundary/create_account_page.py)
Covers US-6. Inputs: email, password, name, dob, phone, profile (dropdown sourced from `ViewProfilesController().view_all_profiles()`). Validates email format, password length ≥ 6, phone digits-only. Refuses to render if no profiles exist yet.
- `render() -> None`
- `display_success() / display_error() -> None`

### `CreateFundraisingActivityPage` — [boundary/create_fundraising_activity_page.py](../boundary/create_fundraising_activity_page.py)
Covers US-13. Inputs: title, description, target amount, category (temporary hardcoded list — see [todo.md](todo.md)), start/end date. Boundary owns validation per diagram.
- `render() -> None`
- `validate_fundraising_activity(...) -> bool`
- `display_fundraising_activity_confirmation() -> None`
- `display_fundraising_activity_validation_error() -> None`

### `ViewFundraisingActivityPage` — [boundary/view_fundraising_activity_page.py](../boundary/view_fundraising_activity_page.py)
Covers US-21. Two-step flow: (1) shows a sortable table of all activities (sourced from `ViewFundraisingActivityController().view_all_fundraising_activities()`) with click-to-select; (2) on row click, calls `select_fundraising_activity(activity_id)` (mirroring the diagram's `selectFundraisingActivity` message) and displays full details with a back button.
- `render() -> None`
- `select_fundraising_activity(activity_id: str) -> None`
- `display_fundraising_activity_details(activity) -> None`

### `InfoPage` — [boundary/info_page.py](../boundary/info_page.py)
**Debug utility, not in any diagram.** Reads and writes SQLite directly. Shows row counts, tabbed dataframes per table, and the live schema. Each table tab supports row-click → "Delete row" (with friendly FK-violation handling). Hide before final demo.

---

## 5. Controller layer ([controller/](../controller/))

Pure delegators. Every method is a one-liner that calls one Entity method.

| Controller | Method | Delegates to |
|---|---|---|
| `LoginController` | `login(email, password)` | `UserAccount.login` |
| `CreateProfileController` | `create_profile(role, description)` | `UserProfile.create_profile` |
| `CreateAccountController` | `create_account(email, password, name, dob, phone_num, profile_id)` | `UserAccount.create_account` |
| `CreateFundraisingActivityController` | `create_fundraising_activity(title, description, target_amount, category, start_date, end_date, owner_email)` | `FundraisingActivity.save_fundraising_activity` (after constructing the entity) |
| `ViewFundraisingActivityController` | `view_fundraising_activity_details(activity_id)` | `FundraisingActivity.view_fundraising_activity_details` |
| `ViewFundraisingActivityController` | `view_all_fundraising_activities()` | `FundraisingActivity.view_all_fundraising_activities` |
| `ViewProfilesController` | `view_all_profiles()` | `UserProfile.view_all_profiles` |

Two of these are **pragmatic additions not on any Sprint 1 class diagram** and need to land on the diagram before final marking (logged in [todo.md](todo.md)):
- `ViewProfilesController.view_all_profiles()` powers the profile dropdown on `CreateAccountPage`. Will fit alongside US-2 / US-5 in Sprint 2.
- `ViewFundraisingActivityController.view_all_fundraising_activities()` powers the clickable table on `ViewFundraisingActivityPage`. Will fit alongside US-20 in Sprint 3.

---

## 6. Entity layer ([entity/](../entity/))

Each Entity owns its own SQL via `persistence.db.get_connection()`. All data access is through the Entity's public methods.

### `UserProfile` — [entity/user_profile.py](../entity/user_profile.py)
Fields: `role: str`, `description: str`, `profile_id: int | None`, `suspended: bool`.
- `create_profile(role, description) -> UserProfile | None`  (classmethod)
- `view_all_profiles() -> list[UserProfile]` (classmethod, **not yet in class diagram**)

### `UserAccount` — [entity/user_account.py](../entity/user_account.py)
Fields: `email, password, name, dob, phone_num, profile_id, suspended`.
- `login(email, password) -> UserAccount | None`  (classmethod, returns None on bad creds OR if account is suspended)
- `create_account(email, password, name, dob, phone_num, profile_id) -> UserAccount | None`  (classmethod, returns None if email already exists — this is the business-rule validation that bubbles up to the Boundary's `display_error()`)

### `FundraisingActivity` — [entity/fundraising_activity.py](../entity/fundraising_activity.py)
Fields: `title, description, target_amount, category, start_date, end_date, status, activity_id, owner_email`.
- `save_fundraising_activity() -> bool`  (instance method; sets `self.activity_id` on success)
- `view_fundraising_activity_details(activity_id) -> FundraisingActivity | None`  (classmethod)
- `view_all_fundraising_activities() -> list[FundraisingActivity]` (classmethod, **not yet in class diagram**)

---

## 7. Persistence ([persistence/](../persistence/))

### [persistence/schema.sql](../persistence/schema.sql)
Three tables, one per Entity. Field names mirror the UML attribute lists in snake_case.

| Table | Notable columns |
|---|---|
| `user_profile` | `profile_id` (PK, AUTOINCREMENT), `role`, `description`, `suspended` |
| `user_account` | `email` (PK), `password`, `name`, `dob`, `phone_num`, `profile_id` (FK → user_profile), `suspended` |
| `fundraising_activity` | `activity_id` (PK, AUTOINCREMENT), `title`, `description`, `target_amount`, `category`, `start_date`, `end_date`, `status`, `owner_email` (FK → user_account) |

### [persistence/db.py](../persistence/db.py)
- `get_connection() -> sqlite3.Connection` — row factory set to `Row`, foreign keys ON
- `init_db() -> None` — runs `schema.sql`
- Run as `python -m persistence.db` to initialise an empty DB at `app.db`

---

## 8. Application entry ([app.py](../app.py))

Streamlit entry. Uses `layout="wide"` so tables and the debug inspector can use full window width. On startup calls `init_db()`. Sidebar shows sign-in status and a radio for the 7 pages. Pages registered:

```python
PAGES = {
    "Log in":                       LoginPage,
    "Log out":                      LogoutPage,
    "Create user profile":          CreateProfilePage,
    "Create user account":          CreateAccountPage,
    "Create fundraising activity":  CreateFundraisingActivityPage,
    "View fundraising activity":    ViewFundraisingActivityPage,
    ".info (debug)":                InfoPage,
}
```

No role-based menu gating yet — see [todo.md](todo.md) "Open design questions".

---

## 9. Tests ([tests/](../tests/))

17 tests, all green.

| File | What it covers |
|---|---|
| [tests/conftest.py](../tests/conftest.py) | `fresh_db` autouse fixture: monkeypatches `DB_PATH` to a tmp file and re-initialises schema before every test |
| [tests/test_user_profile.py](../tests/test_user_profile.py) | `create_profile` persistence; `view_all_profiles` returns all profiles + empty list when no records |
| [tests/test_user_account.py](../tests/test_user_account.py) | `create_account` happy path; duplicate-email rejection; `login` correct/incorrect creds |
| [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) | `save_fundraising_activity` persists + sets ID; `view_fundraising_activity_details` round-trip + missing-ID returns None; `view_all_fundraising_activities` returns every record + empty list when none |
| [tests/test_controllers.py](../tests/test_controllers.py) | Each Controller's delegation contract; pins controllers as pure delegators (incl. `view_all_profiles` and `view_all_fundraising_activities`) |

Run with `pytest` (or `.venv/bin/pytest`).

---

## 10. Seed data ([data/seed.py](../data/seed.py))

Idempotent (drops & recreates `app.db`). Populates:
- 100 user profiles (random role + Faker sentence description)
- 100 user accounts (Faker name/email/dob/phone, password `password123`, random profile assignment)
- 100 fundraising activities (Faker text, random category/status/dates/amounts)

Run with `python -m data.seed`.

---

## 11. CI ([.github/workflows/ci.yml](../.github/workflows/ci.yml))

Triggers: push or PR to `main` / `master`. Steps: checkout → setup Python 3.11 with pip cache → `pip install -r requirements.txt` → `pytest -v`.

This satisfies the project's CI/CD evidence requirement once the repo is pushed to GitHub.

---

## 12. Conventions enforced

See [../CLAUDE.md](../CLAUDE.md) for the full list. Quick recap:

1. All input/format validation in Boundary
2. Business-rule validation (uniqueness, existence) bubbles up from Entity → displayed by Boundary
3. No `get_*` / `retrieve_*` method names; entity public methods named after user actions
4. Controllers are pure delegators
5. Class suffixes: `Page`, `Controller`, none for Entities
6. Method signatures match diagrams character-for-character
7. Boundary never imports from `entity/` directly

---

## 13. What is **not** implemented (intentional)

See [todo.md](todo.md) for the full list. Highlights:

- Password hashing — Sprint 2
- Role-based menu / route guards — Sprint 2
- US-2..US-5 (admin view/update/suspend/search profile)
- US-7..US-10 (admin view/update/suspend/search account)
- US-14..US-17 (fundraiser FSA management)
- US-22..US-25 (donee favourites)
- US-28..US-33 (analytics/history)
- US-34..US-38 (platform manager category management) — categories currently hardcoded as a temporary placeholder
- US-41..US-43 (reports)
