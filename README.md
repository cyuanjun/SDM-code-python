# SDM Online Fundraising System — revamp branch

CSIT314 group project. Built from scratch against reworked UML diagrams. B-C-E architecture, OOP backend, diagram-as-contract — see [CLAUDE.md](CLAUDE.md).

- [CLAUDE.md](CLAUDE.md) — architecture conventions
- [docs/diagram_typos.md](docs/diagram_typos.md) — every divergence between source diagrams and code (to fix in diagrams before final marking)
- [docs/todo.md](docs/todo.md) — bootstrap deviations, Exception A entries, architectural items
- [diagrams/](diagrams/) — reworked UML diagrams, organised by sprint

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m persistence.db          # initialises app.db with all current tables
streamlit run app.py              # launches the UI on http://localhost:8501
```

App startup also runs [data/seed.py](data/seed.py) which idempotently creates default accounts + demo data:

| Role | Email | Password |
|---|---|---|
| Admin | `admin@example.com` | `admin` |
| Platform Manager | `pm@example.com` | `pm` |
| Donee (demo) | `demo-donee@example.com` | `demo` |

A demo fundraiser is also seeded along with three sample donations so US-32 / US-33 have data to display. Logged in [docs/todo.md](docs/todo.md) as a bootstrap convention to either keep or replace with an initial-setup use case before final marking.

## Run tests

```bash
pytest
```

340 passing. Tests are written test-first; per [CLAUDE.md](CLAUDE.md) "TDD expectations" every entity method ships with both a happy-path and a negative test (missing rows, FK violations, invalid input, empty results, cross-tenant access). Controller delegation tests are paired the same way. CI runs via [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Project layout

| Path | Layer | Purpose |
|---|---|---|
| `app.py` | — | Streamlit entry + session-based router |
| `boundary/` | Boundary | One Streamlit page module per use case |
| `controller/` | Controller | Pure delegators between Boundary and Entity |
| `entity/` | Entity | Business objects + persistence |
| `persistence/` | — | SQLite connection helper + schema + shared ID helpers |
| `data/seed.py` | — | Idempotent seed: admin, PM, demo donee + activity + donations |
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

All 43 user stories implemented. 340 tests passing.
