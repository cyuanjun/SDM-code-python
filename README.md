# SDM Online Fundraising System — revamp-final-diagrams branch

CSIT314 group project. Built from scratch against reworked UML diagrams. B-C-E architecture, OOP backend, diagram-as-contract — see [CLAUDE.md](CLAUDE.md).

- [CLAUDE.md](CLAUDE.md) — architecture conventions
- [docs/implementation_2026-05-18.md](docs/implementation_2026-05-18.md) — per-US implementation reference (diagram surface, code paths, tests, assumptions, deferred items)
- [docs/audit.md](docs/audit.md) — diagram-by-diagram Boundary / Controller / Entity surface paired with the matching `Code →` Python identifier, ordered US-1 → US-43 (zero open drifts)
- [docs/test_cases.md](docs/test_cases.md) — diagram-derived test cases (per-US table, 103 IDs, every happy + negative path)
- [docs/diagram_typos.md](docs/diagram_typos.md) — every divergence between source diagrams and code
- [docs/todo.md](docs/todo.md) — bootstrap deviations, Exception A entries, lecturer decisions, deferred typos, open architectural items
- [diagrams/](diagrams/) — reworked UML diagrams, organised by sprint

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

streamlit run app.py              # launches the UI on http://localhost:8501
                                  # init_db + seeds run automatically on startup
```

### Database commands

```bash
python -m persistence.db          # create app.db with empty tables (no seed)
python -m data.seed               # idempotent — init_db + seed all 4 role accounts + demo donations
rm app.db && python -m data.seed  # nuke and reseed from scratch
```

App startup also runs [data/seed.py](data/seed.py) — anything the seed produces is also produced by `streamlit run app.py`. The standalone `python -m data.seed` is useful when you want to refresh the DB without launching the UI.

### Default accounts seeded

| Role | Email | Password |
|---|---|---|
| Admin | `a001@a.com` | `123` |
| Fundraiser | `fr001@a.com` | `123` |
| Donee | `d001@a.com` | `123` |
| Platform Manager | `pm001@a.com` | `123` |

Three sample donations are also seeded against a demo activity owned by the default fundraiser so US-32 / US-33 have data to display. Lecturer-approved (2026-05-15) as an acceptable bootstrap convention — logged in [docs/todo.md](docs/todo.md) under "Lecturer decisions".

On top of the four default credentials, `seed_bulk_all()` runs on startup and tops up to **100 of each scalable table**: accounts / categories / activities / donations / favourites / reports — so the admin/PM browse + search pages have realistic data to scroll. Account split (after TC actors are added): 2 admins (`a001` + `tc-admin`) / 25 fundraisers (`fr001`..`fr024` + `tc-fr`) / 69 donees (`d001`..`d068` + `tc-d`) / 4 PMs (`pm001`..`pm003` + `tc-pm`). Favourites are 100 distinct (donee × activity) pairs; reports cycle daily / weekly / monthly across the PMs. Idempotent — re-running `streamlit run app.py` or `python -m data.seed` does nothing once the targets are met.

**TC scenario rows** — `seed_tc_scenario()` runs after the bulk top-ups, adding a curated set of `TC - <>`-prefixed rows that back every test case in [docs/test_cases.md](docs/test_cases.md). The scenario is fully self-contained under its own actor accounts:

| Account | Email | Password | Owns |
|---|---|---|---|
| TC - Admin | `tc-admin@a.com` | `123` | (no data — admin actor for management TCs) |
| TC - Fundraiser | `tc-fr@a.com` | `123` | the 3 TC activities |
| TC - Donee | `tc-d@a.com` | `123` | the 2 TC donations + 1 TC favourite |
| TC - Platform Manager | `tc-pm@a.com` | `123` | the 1 TC monthly report |

Plus 3 categories (`TC - Health`, `TC - Education`, `TC - Sports` (suspended)) and 3 activities owned by TC - Fundraiser (`TC - Active hospital fund`, `TC - Completed school fund` (past end_date → stored `completed=1`), `TC - Suspended sports fund` (suspended=1)). Single coherent scenario shared across all 106 TCs — one set tests everything. `seed_tc_scenario()` runs **after** the bulk top-ups (which reserve the trailing slots), so the TC rows occupy the highest IDs in every table — `acc_097..100`, `cat_098..100`, `fra_098..100`, `don_099..100`, `fav_100`, `rep_100`. Final totals per scalable table stay at 100. Role distribution becomes 2 admin / 25 fundraisers / 69 donees / 4 PMs (one donee slot shifted to admin to make room for TC - Admin while keeping the account total at 100).

## Run tests

```bash
pytest
```

412 passing. Tests are written test-first; per [CLAUDE.md](CLAUDE.md) "TDD expectations" every entity method ships with both a happy-path and a negative test (missing rows, FK violations, invalid input, empty results, cross-tenant access). Controller delegation tests are paired the same way. CI runs via [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Project layout

| Path | Layer | Purpose |
|---|---|---|
| `app.py` | — | Streamlit entry + session-based router |
| `boundary/` | Boundary | One Streamlit page module per use case |
| `controller/` | Controller | Pure delegators between Boundary and Entity |
| `entity/` | Entity | Business objects + persistence |
| `persistence/` | — | SQLite connection helper + schema + shared ID helpers |
| `data/seed.py` | — | Idempotent seed: one account per role (admin / fundraiser / donee / PM) + a demo activity + three sample donations |
| `tests/` | — | pytest tests + `conftest.py` fixture |
| `docs/` | — | architectural notes (typos catalogue, todo, etc.) |
| `diagrams/` | — | source UML diagrams (per sprint) |
| `.github/workflows/ci.yml` | — | CI: runs pytest on push/PR |

## Coverage so far

| Sprint | Stories | Status |
|---|---|---|
| Sprint 1 | US-1, 6, 11, 12, 13, 18, 19, 21, 26, 27, 39, 40 | ✓ Complete |
| Sprint 2 | US-2, 3, 7, 8, 14, 15, 20, 22, 24 | ✓ Complete |
| Sprint 3 | US-4, 5, 9, 10, 16, 17, 23, 25, 30, 31, 32, 33 | ✓ Complete |
| Sprint 4 | US-28, 29, 34, 35, 36, 37, 38, 41, 42, 43 | ✓ Complete |

All 43 user stories implemented. 410 tests passing. Zero outstanding diagram typos — every divergence is either resolved (live diagrams updated), lecturer-deferred, or logged as an accepted code-vs-diagram divergence. See [docs/audit.md](docs/audit.md) for the diagram-by-diagram surface and `Code →` mapping, plus [docs/diagram_typos.md](docs/diagram_typos.md) and the "Lecturer decisions" / "Deferred typos" sections of [docs/todo.md](docs/todo.md).

The sidebar is consolidated into 10 entries via per-actor `Manage*` / `Browse*` / `My*` pages (Exception C in [CLAUDE.md](CLAUDE.md)). Role-based gating filters pages by the logged-in user's role.
