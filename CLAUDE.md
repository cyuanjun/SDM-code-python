# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is the durable contract between the team and Claude Code for the CSIT314 SDM group project. Read it first every session.

## Common commands

```bash
# First-time setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the app (init_db + idempotent seeds run automatically on startup)
streamlit run app.py              # serves on http://localhost:8501

# Database
python -m persistence.db          # creates app.db with empty tables (no seed)
python -m data.seed               # idempotent — init_db + seed all 4 role accounts + demo donations
rm app.db && python -m data.seed  # nuke and reseed from scratch

# Tests
pytest                            # full suite
pytest -v                         # verbose (matches CI)
pytest tests/test_user_account.py                          # single file
pytest tests/test_user_account.py::test_login_succeeds     # single test
pytest -k favourite               # by name substring
```

There is no linter or formatter configured — do not introduce one without asking.

## Project context

CSIT314 (Software Development Methodologies) group project, UOW SIM S2 2026. Building an online fundraising system (GoFundMe-style) that matches fundraisers with donees. Four actors — User Admin, Fundraiser, Donee, Platform Manager — across 43 user stories split into 4 sprints. Marking criteria require a B-C-E (Boundary-Controller-Entity) architecture, an OOP backend, TDD, CI/CD, and tight consistency between UML diagrams and code.

## Stack (locked in)

- **Python 3** for everything
- **Streamlit** for UI — each Boundary class is a Streamlit page module
- **SQLite** via stdlib `sqlite3` for persistence — single `app.db` file
- **pytest** for tests (incl. `streamlit.testing.v1.AppTest` for boundary smoke tests)
- **GitHub Actions** for CI ([.github/workflows/ci.yml](.github/workflows/ci.yml) pins Python 3.11 — keep `requirements.txt` compatible)

Do not propose Django/Flask/FastAPI/Node/SQLAlchemy/etc. unless the user explicitly reopens the stack discussion.

## Diagram-as-contract rule

When the user shares Sprint N sequence/class diagrams, **treat the class names, method names, parameter lists, and return types as binding**. Implement them character-for-character (modulo Python `snake_case`). Do not rename, merge, split, or "clean up" diagram methods without explicit approval. If a diagram conflicts with this file, ask the user which to update.

The source-of-truth diagrams live under [diagrams/](diagrams/), organised by sprint (`sprint-1_diagrams/` … `sprint-4_diagrams/`), one `US-NN.jpg` per story.

For detail on a specific user story (diagram surface, code paths, tests, assumptions, deferred items), read **[docs/implementation_2026-05-18.md](docs/implementation_2026-05-18.md)** — one section per US.

For the diagram-by-diagram surface (Boundary / Controller / Entity + methods + args) paired with the matching `Code →` Python identifier, ordered US-1 → US-43, read **[docs/audit.md](docs/audit.md)** — this is the "does the code match the diagrams" cross-check; zero open drifts as of 2026-05-18.

Every divergence between a diagram and the code is split across two more docs:

- [docs/diagram_typos.md](docs/diagram_typos.md) — pure typos / signature issues in the source diagrams where the code follows the *corrected* version. Grouped by sprint.
- [docs/todo.md](docs/todo.md) — Exception A entries (off-diagram methods added for UX), bootstrap deviations (data/seed.py), Lecturer decisions (4), Deferred typos index (6), Open architectural items (1), and a Resolved section.

Read both before assuming a method name or signature is wrong in the code — it may already be tracked as a known diagram fix.

## Architecture conventions

These rules apply to every sprint and override defaults:

1. **All input/format validation lives in the Boundary** (Streamlit page). Empty fields, format checks, date sanity, positive amounts — checked before any controller is called.
2. **Business-rule validation (uniqueness, existence) lives in the Entity.** The Entity reports failure (e.g. returns `None` or `False`); the Boundary calls `display_error()` based on that signal.
3. **No `get_*` or `retrieve_*` method names anywhere.** Entity public methods are named after the user-facing action: `login`, `create_account`, `create_profile`, `view_fundraising_activity`, `save_fundraising_activity`. SQL `SELECT`s are an internal implementation detail of the Entity.
4. **Controllers are pure delegators.** They take Boundary input, call one Entity method, return the result. No branching, no transformation, no logging. If a controller needs logic, raise it with the user before adding.
5. **Class-name suffixes are fixed:** Boundary classes end in `Page` (or `LogoutPage`), Controller classes end in `Controller`, Entity classes have no suffix.
6. **Method signatures match the diagrams character-for-character** (modulo snake_case). Same arity, same return type. If you need new parameters, the diagram must change first.
7. **Boundary never imports Entity for behaviour.** All Entity *access* (read / write / search) goes through a Controller. The one carve-out: a Boundary may import an Entity dataclass purely to *construct* an instance to pass into a controller (e.g. `UpdateUserProfileController().update_user_profile(profile_id, UserProfile(role=..., description=..., suspended=...))`) because the diagram-defined update signatures take an entity object as a parameter. This is a constructor import, not a behaviour call.

## Documented exceptions

Three narrow exceptions to the strict rules above.

### Exception A — Pragmatic Entity extensions for UX

If a Boundary page legitimately needs to display a list of records, look up by a non-id field, or perform an action the diagram doesn't define (e.g. unsuspend), you may add a method to the Entity (and a matching pure delegator on a Controller). Conditions:

- The new method follows the naming rule (`view_*`, `unsuspend_*`, `increment_*`, etc. — never `get_*` / `retrieve_*`).
- The Controller stays a pure delegator.
- An entry is added to the "Exception A — off-diagram entity methods to power UX" section of [docs/todo.md](docs/todo.md), naming the new method and which boundary needs it.
- The class diagram is updated to reflect the new method **before** final submission (or a new use case is defined).

Current Exception A methods (live in [docs/todo.md](docs/todo.md)): `UserProfile.view_all_profiles` + `unsuspend_user_profile`, `UserAccount.view_all_user_accounts` + `unsuspend_user_account`, `FundraisingActivity.view_all_fundraising_activities` + `view_my_fundraising_activities` + `increment_view_count` + `increment_save_count` + `unsuspend_my_fundraising_activity`, `FundraisingActivityCategory.view_all_categories` + `unsuspend_fundraising_activity_category`. (`Donation.view_my_donations` was retired 2026-05-18 when US-33 reframed to list semantics.)

### Exception B — Debug-only utilities

A page intended purely for development inspection (currently [boundary/non_diagram/info_page.py](boundary/non_diagram/info_page.py)) may bypass the B-C-E layers and read/write the database directly. Conditions:

- The page docstring states clearly that it is a debug utility, not part of the design.
- The page is logged under **"Debug-only artifacts"** in [docs/todo.md](docs/todo.md).
- The page is hidden or removed before the final recorded demo.

Do not extend this exception to features that look "small" — only true dev/inspection tools qualify.

### Exception C — UX consolidation (combined Boundary pages)

The reworked diagrams define 27 per-US Boundary classes (`CreateProfilePage`, `ViewUserProfilePage`, `UpdateUserProfilePage`, `ViewUserProfilesPage`, etc.) which would produce a 27-entry sidebar. The sidebar instead wires seven **combined `Manage*` / `Browse*` / `My*` pages** that compose search + list + detail + inline create + update + suspend/unsuspend into one screen per resource type.

- Every per-US Boundary class **still exists** as a tested artifact — the diagrams stay 1:1 with source files. They're just not sidebar entries.
- The combined pages call the same Controllers and Entities the per-US Boundaries do; no new business logic.
- Logged under "UX consolidation" in [docs/diagram_typos.md](docs/diagram_typos.md) with the full mapping from combined page → per-US classes it replaces.

When adding a new story whose diagram fits an existing combined page, extend the combined page rather than wiring the new per-US class into the sidebar.

## Directory layout

```
SDM-code/
├── app.py                 # Streamlit entry; PAGES + PAGES_BY_ROLE; role-gated routing
├── boundary/              # <<Boundary>> pages — 27 per-US diagram-derived classes
│   └── non_diagram/       # 7 UX-consolidated Manage/Browse/My pages + 1 debug page (not on any diagram)
├── controller/            # <<Controller>> classes — pure delegators, one method per use case
│   └── non_diagram/       # 5 Exception A controllers (4 unsuspend + view_profiles, not on any diagram)
├── entity/                # <<Entity>> classes — UserProfile, UserAccount, FundraisingActivity, Favourite, Donation, FundraisingActivityCategory, Report
├── persistence/
│   ├── db.py              # get_connection() + init_db() — sqlite3 plumbing
│   ├── ids.py             # format_id(prefix, n) / next_id(conn, table, col, prefix) — TEXT-PK helpers
│   └── schema.sql         # CREATE TABLE statements, one per Entity
├── data/seed.py           # Idempotent bootstrap: one account per role + 3 demo donations
├── tests/                 # pytest tests + conftest.py (autouse tmp_path DB fixture)
│   └── non_diagram/       # smoke tests for the 8 non-diagram boundaries + delegation tests for the 5 non-diagram controllers
├── docs/
│   ├── implementation_2026-05-18.md  # Per-US implementation reference (diagram surface, code paths, tests, assumptions, deferred items) — primary per-story doc
│   ├── audit.md           # Diagram-by-diagram Boundary / Controller / Entity surface + matching `Code →` identifier, US-1 → US-43; zero open drifts
│   ├── test_cases.md      # Diagram-derived test cases (per-US table, 103 IDs, happy + negative path per US)
│   ├── diagram_typos.md   # Per-sprint catalogue of every diagram divergence (resolved + outstanding + deferred)
│   └── todo.md            # Bootstrap deviations, Exception A entries, Lecturer decisions, Deferred typos index, Open architectural items, Resolved
├── diagrams/              # Source UML diagrams, sprint-1_diagrams/ … sprint-4_diagrams/
└── .github/workflows/     # CI (Python 3.11)
```

## Key implementation patterns

These are the non-obvious wiring choices a future session would otherwise have to reverse-engineer:

- **Routing.** `app.py` holds a flat `PAGES` dict (sidebar label → Boundary class) and a `PAGES_BY_ROLE` dict (role → allow-list of labels). `main()` calls `_current_role()` (looks up the session user's profile via `ViewUserProfileController`), filters PAGES by `PAGES_BY_ROLE[role]`, renders the sidebar radio, and calls `page_cls().render()`. The `.info (debug)` page is visible to every role and to logged-out users.
- **Session.** Cross-page state (the logged-in user) lives in `st.session_state["user"]` as a `UserAccount` instance. Login writes it; logout clears it; pages read it directly. **Always call `st.rerun()` after mutating session state** so the sidebar caption (which renders before page logic) picks up the new value on the next pass. The signed-in caption shows `Signed in as <name> (<role>) <email>` via the same `ViewUserProfileController` lookup that drives role gating.
- **DB access.** `persistence/db.py` exposes `get_connection()` (returns a `sqlite3.Connection` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`) and `init_db()` (executes `schema.sql`). Entities open their own connections per operation — there is no ORM and no shared session.
- **Prefixed string IDs.** Every PK column is `TEXT` storing `prefix_NNN` strings (`prof_001`, `acc_001`, `fra_001`, `cat_001`, `rep_001`, `don_001`) — matches what the diagrams say. FK columns are TEXT too, holding the same prefixed form. SQLite doesn't auto-increment TEXT PKs, so `persistence/ids.py.next_id(conn, table, id_column, prefix)` mints the next id on each INSERT (SELECT MAX existing → parse suffix → increment → format with 3-digit zero-pad). Entity methods take and return the prefixed strings unchanged — there's no parse/format dance in the SQL bindings any more.
- **Test isolation.** [tests/conftest.py](tests/conftest.py) defines an `autouse` fixture that monkey-patches `persistence.db.DB_PATH` to a `tmp_path` file and re-initialises the schema before every test. Never write tests that assume `app.db`; just call entity methods and the fixture handles the rest.
- **Seed data.** `data/seed.py` is **idempotent** — every function checks for existence before inserting. On every `streamlit run app.py`, four default accounts are seeded (`a001@a.com` / admin, `fr001@a.com` / fundraiser, `d001@a.com` / donee, `pm001@a.com` / platform manager — all with password `123`), plus a demo activity owned by the fundraiser and three sample donations from the donee. No Faker, no `RECORD_COUNT`. To start fresh: `rm app.db && streamlit run app.py`.

## TDD expectations

- Every new Entity gets `tests/test_<entity>.py` written **before** the entity body is implemented.
- Every new Controller gets one delegation test (controller forwards to entity, returns entity's result).
- Boundary pages get smoke tests only (`render()` doesn't raise via `streamlit.testing.v1.AppTest`) — Streamlit UIs are hard to unit-test, that's expected.
- **Every entity method gets at least one negative test alongside its happy-path test.** Cover the failure paths the diagram or schema implies — `None` / `False` returns for missing rows, uniqueness violations, FK violations, invalid input, empty results, cross-tenant access where ownership applies. A test file with only happy-path cases is incomplete.
- **Every controller delegation test is mirrored by a negative-path delegation test** — when the entity returns `None` / `False` / `[]`, the controller must forward that unchanged.
- Run `pytest` locally and in CI on every push.

## Sprint workflow

When handed new sprint diagrams:

1. List affected use cases (US-N).
2. Identify which Boundary / Controller / Entity files are new vs. modified.
3. Write/update entity tests first (happy + negative).
4. Implement entity (with persistence).
5. Implement controller (pure delegator) + delegation test (happy + negative mirror).
6. Implement the per-US boundary page.
7. Wire into the appropriate combined `Manage*` / `Browse*` / `My*` page (Exception C) — not directly into the sidebar.
8. Update `persistence/schema.sql` if new fields/tables.
9. Update `data/seed.py` if new tables need demo data.
10. Update `PAGES_BY_ROLE` in `app.py` if the new story belongs to a role that doesn't have its combined page yet.

## Anti-patterns to refuse

- Business logic inside a Controller method
- Validation outside the Boundary
- Method names containing `get_` or `retrieve_`
- Boundary importing from `entity/` directly
- Renaming a diagram method to fit Pythonic taste
- Adding password hashing or any other feature not in the active sprint's diagrams (RBAC is the one exception — already in place via `PAGES_BY_ROLE`)

## Coverage and what's deferred

All **43 user stories** are implemented on this branch (`revamp-final-diagrams`). **389 tests pass.** **Zero open diagram drifts** — see [docs/audit.md](docs/audit.md) for the diagram-by-diagram Boundary / Controller / Entity surface + matching `Code →` Python identifier.

The seed bulks up to **100 accounts / 100 categories / 100 activities / 100 donations** on startup (idempotent — `seed_bulk_all()` in [data/seed.py](data/seed.py)). Profiles stay schema-locked at 1 per role. Account split: 1 admin / 25 fundraisers / 70 donees / 4 PMs. The four default-credentials accounts (a001/fr001/d001/pm001) are still the first row in each role.

| Sprint | Stories | Status |
|---|---|---|
| Sprint 1 | US-1, 6, 11, 12, 13, 18, 19, 21, 26, 27, 39, 40 | ✓ |
| Sprint 2 | US-2, 3, 7, 8, 14, 15, 20, 22, 24 | ✓ |
| Sprint 3 | US-4, 5, 9, 10, 16, 17, 23, 25, 30, 31, 32, 33 | ✓ |
| Sprint 4 | US-28, 29, 34, 35, 36, 37, 38, 41, 42, 43 | ✓ |

### Still open (in [docs/todo.md](docs/todo.md) "Open architectural items")

- **Plain-text passwords.** Sprint 1's `UserAccount` stores the password as plain text per the diagram. Hashing (bcrypt/argon2) belongs in a hardening sprint.

### Resolved in this revamp

- **RBAC / menu gating** — closed by `PAGES_BY_ROLE` in `app.py`.
- **Ownership enforcement at the entity layer** — closed because the reworked US-14/15/16/17/30/31 diagrams pass `owner_account_id` as a parameter; entity-side `WHERE owner_account_id = ?` clauses refuse cross-owner writes.
- **Donation history (US-32 / US-33)** — closed by the new `Donation` entity in Sprint 3 + a `seed_demo_donations` bootstrap (lecturer-approved 2026-05-15 as a bootstrap convention).
- **Default-admin / PM / fundraiser / donee accounts** — closed by per-role idempotent seed functions in `data/seed.py`.
- **Email uniqueness on `UserAccount`** — closed 2026-05-15 (lecturer instruction). `user_account.email` has `UNIQUE` at the schema level; `create_account` returns `None` on conflict, `update_user_account` returns `False`. Boundary surfaces an "email already in use" message.
