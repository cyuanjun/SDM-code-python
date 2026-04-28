# SDM Online Fundraising System

CSIT314 group project — an online fundraising system matching fundraisers with donees. Built with Python + Streamlit + SQLite, following a B-C-E (Boundary-Controller-Entity) OOP architecture.

- [CLAUDE.md](CLAUDE.md) — architecture conventions and the diagram-as-contract rule
- [docs/implementation.md](docs/implementation.md) — full reference of every file, class, and method
- [docs/todo.md](docs/todo.md) — temporary placeholders, deferred work, and diagram updates owed before final marking

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m persistence.db          # creates app.db with empty tables
python -m data.seed               # populates ~10 records per table (bump RECORD_COUNT to 100 in data/seed.py for the marking demo)

streamlit run app.py              # launches the UI on http://localhost:8501
```

## Run tests

```bash
pytest
```

43 tests, all green. CI runs the same suite via [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Project layout

| Path | Layer | Purpose |
|---|---|---|
| `app.py` | — | Streamlit entry + session-based router (wide layout) |
| `boundary/` | Boundary | Streamlit page modules — one per use case (+ `info_page.py` debug utility) |
| `controller/` | Controller | Pure delegators between Boundary and Entity |
| `entity/` | Entity | Business objects + persistence |
| `persistence/` | — | SQLite connection helper + schema |
| `data/seed.py` | — | Test data generator (Faker) |
| `tests/` | — | pytest tests (TDD) |
| `docs/` | — | implementation reference + todo list |
| `.github/workflows/ci.yml` | — | CI: runs pytest on push/PR |

## Coverage so far

**Sprint 1** (12 stories): create profile/account, login/logout for all four actors, create fundraising activity, view fundraising activity (donee).

**Sprint 2** (9 stories): admin view/update profile (US-2/3) and account (US-7/8); fundraiser view/update their own FSAs (US-14/15); donee search FSAs (US-20), save to favourites (US-22), view favourites (US-24).

Total: **21 of 43 user stories** implemented across 16 Streamlit pages and 43 passing tests.

## Debug utilities

The sidebar includes a `.info (debug)` page that shows row counts, full table dumps, the live schema, and supports row-click delete with friendly FK-violation handling. Bypasses the B-C-E layers because it is not a use case. **Hide before the final live demo** — see [docs/todo.md](docs/todo.md).
