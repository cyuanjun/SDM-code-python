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
python -m data.seed               # populates ~100 records per table

streamlit run app.py              # launches the UI on http://localhost:8501
```

## Run tests

```bash
pytest
```

17 tests, all green. CI runs the same suite via [.github/workflows/ci.yml](.github/workflows/ci.yml).

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

## Sprint 1 coverage (current)

- US-1 Create user profile
- US-6 Create user account (profile chosen via dropdown)
- US-11/18/26/39 Login (User Admin / Fundraiser / Donee / Platform Manager)
- US-12/19/27/40 Logout
- US-13 Create fundraising activity
- US-21 View fundraising activity details (clickable list → details view)

## Debug utilities

The sidebar includes a `.info (debug)` page that shows row counts, full table dumps, the live schema, and supports row-click delete with friendly FK-violation handling. Bypasses the B-C-E layers because it is not a use case. **Hide before the final live demo** — see [docs/todo.md](docs/todo.md).
