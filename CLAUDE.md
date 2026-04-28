# CLAUDE.md — SDM Project Conventions

This file is the durable contract between the team and Claude Code for the CSIT314 SDM group project. Read it first every session.

## Project context

CSIT314 (Software Development Methodologies) group project, UOW SIM S2 2026. Building an online fundraising system (GoFundMe-style) that matches fundraisers with donees. Four actors — User Admin, Fundraiser, Donee, Platform Manager — across 43 user stories split into ~4 sprints. Marking criteria require a B-C-E (Boundary-Controller-Entity) architecture, an OOP backend, TDD, CI/CD, and tight consistency between UML diagrams and code.

## Stack (locked in)

- **Python 3** for everything
- **Streamlit** for UI — each Boundary class is a Streamlit page module
- **SQLite** via stdlib `sqlite3` for persistence — single `app.db` file
- **pytest** for tests
- **Faker** for seed data
- **GitHub Actions** for CI

Do not propose Django/Flask/FastAPI/Node/SQLAlchemy/etc. unless the user explicitly reopens the stack discussion.

## Diagram-as-contract rule

When the user shares Sprint N sequence/class diagrams, **treat the class names, method names, parameter lists, and return types as binding**. Implement them character-for-character (modulo Python `snake_case`). Do not rename, merge, split, or "clean up" diagram methods without explicit approval. If a diagram conflicts with this file, ask the user which to update.

## Architecture conventions

These rules apply to every sprint and override defaults:

1. **All input/format validation lives in the Boundary** (Streamlit page). Empty fields, format checks, date sanity, positive amounts — checked before any controller is called.
2. **Business-rule validation (uniqueness, existence) lives in the Entity.** The Entity reports failure (e.g. returns `None` or `False`); the Boundary calls `display_error()` based on that signal.
3. **No `get_*` or `retrieve_*` method names anywhere.** Entity public methods are named after the user-facing action: `login`, `create_account`, `create_profile`, `view_fundraising_activity_details`, `save_fundraising_activity`. SQL `SELECT`s are an internal implementation detail of the Entity.
4. **Controllers are pure delegators.** They take Boundary input, call one Entity method, return the result. No branching, no transformation, no logging. If a controller needs logic, raise it with the user before adding.
5. **Class-name suffixes are fixed:** Boundary classes end in `Page` (or `LogoutPage`), Controller classes end in `Controller`, Entity classes have no suffix.
6. **Method signatures match the diagrams character-for-character** (modulo snake_case). Same arity, same return type. If you need new parameters, the diagram must change first.
7. **Boundary never imports Entity directly.** All Entity access goes through a Controller.

## Documented exceptions

Two narrow exceptions to the strict rules above. Each must be logged in [docs/todo.md](docs/todo.md) when used so the team knows what to fix before final marking.

### Exception A — Pragmatic Entity extensions for UX

If a Boundary page legitimately needs to display a list of records (e.g. a profile dropdown, a clickable table of activities) but no Sprint diagram defines a corresponding entity method, you may add a `view_all_<entities>()` classmethod to the Entity (and a matching pure delegator on a Controller). Conditions:

- The new method follows the naming rule (`view_*`, never `get_*` / `retrieve_*`).
- The Controller stays a pure delegator.
- An entry is added to the **"Diagram updates needed before final marking"** section of [docs/todo.md](docs/todo.md), naming the new method and the future user story it will fit under.
- The class diagram is updated to reflect the new method **before** final submission.

Existing examples (all logged in [docs/todo.md](docs/todo.md) for diagram catchup):
- `UserProfile.view_all_profiles()` — profile dropdown on `CreateAccountPage`
- `FundraisingActivity.view_all_fundraising_activities()` — clickable table on `ViewFundraisingActivityPage`
- `UserAccount.view_all_user_accounts()` — admin's account list on `ViewUserAccountPage`
- `FundraisingActivity.view_activities_by_owner()` — fundraiser's scoped list on `ViewFundraiserActivityPage` / `UpdateFundraiserActivityPage`
- `FavouriteList.remove_favourite()` — helper anticipating US-23

### Exception B — Debug-only utilities

A page intended purely for development inspection (currently `boundary/info_page.py`) may bypass the B-C-E layers and read/write the database directly. Conditions:

- The page docstring states clearly that it is a debug utility, not part of the design.
- The page is logged under **"Debug-only artifacts"** in [docs/todo.md](docs/todo.md).
- The page is hidden or removed before the final recorded demo.

Do not extend this exception to features that look "small" — only true dev/inspection tools qualify.

## Directory layout

```
SDM-code/
├── app.py                 # Streamlit entry; routes via st.session_state
├── boundary/              # <<Boundary>> classes — one file per page
├── controller/            # <<Controller>> classes — one file per use case
├── entity/                # <<Entity>> classes — own their persistence
├── persistence/           # db.py + schema.sql
├── data/seed.py           # Faker-based test data generator (RECORD_COUNT, default 10; bump to 100 for the marking demo)
├── tests/                 # pytest tests
└── .github/workflows/     # CI
```

## TDD expectations

- Every new Entity gets `tests/test_<entity>.py` written **before** the entity body is implemented.
- Every new Controller gets one delegation test (controller forwards to entity, returns entity's result).
- Boundary pages get smoke tests only (`render()` doesn't raise) — Streamlit UIs are hard to unit-test, that's expected.
- Run `pytest` locally and in CI on every push.

## Sprint workflow

When handed new sprint diagrams:

1. List affected use cases (US-N).
2. Identify which Boundary / Controller / Entity files are new vs. modified.
3. Write/update entity tests first.
4. Implement entity (with persistence).
5. Implement controller (pure delegator).
6. Implement boundary page.
7. Wire the page into `app.py`'s router.
8. Update `persistence/schema.sql` if new fields/tables.
9. Update `data/seed.py` if new tables need seeding.

## Anti-patterns to refuse

- Business logic inside a Controller method
- Validation outside the Boundary
- Method names containing `get_` or `retrieve_`
- Boundary importing from `entity/` directly
- Renaming a diagram method to fit Pythonic taste
- Adding password hashing, RBAC, or other features not in the active sprint's diagrams

## Out-of-scope features (deferred, intentionally)

- Password hashing — add in Sprint 2 hardening
- Full role-based access control — single-role check in `app.py` is enough for now
- Suspend/update/search admin flows (US-2..US-5, US-7..US-10) — Sprint 2
- FSA management, favourites, history, reports (US-14..US-43) — Sprints 3/4
