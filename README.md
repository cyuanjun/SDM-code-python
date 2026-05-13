# SDM Online Fundraising System — revamp branch

CSIT314 group project. This branch is rebuilding the system from scratch against reworked UML diagrams. Architecture conventions (B-C-E, OOP backend, diagram-as-contract) carry over from main; see [CLAUDE.md](CLAUDE.md).

- [CLAUDE.md](CLAUDE.md) — architecture conventions and the diagram-as-contract rule
- [docs/todo.md](docs/todo.md) — revamp checkpoints and architecture items carried over
- [docs/issues.md](docs/issues.md) — active design gaps (RBAC, ownership-check, donation tracking)
- [diagrams/](diagrams/) — UML diagrams (drop the reworked versions here)

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m persistence.db          # initialises app.db (currently no tables — schema rebuilds story by story)

streamlit run app.py              # launches the placeholder UI on http://localhost:8501
```

A seed script will land once at least one entity exists.

## Run tests

```bash
pytest
```

Only a placeholder smoke test on this branch ([tests/test_smoke.py](tests/test_smoke.py)) so pytest collects at least one item and CI stays green. Real tests get written test-first as each entity is rebuilt. CI still runs via [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Project layout

| Path | Layer | Purpose |
|---|---|---|
| `app.py` | — | Streamlit entry + session-based router (currently a placeholder) |
| `boundary/` | Boundary | Streamlit page modules — empty, refills as stories land |
| `controller/` | Controller | Pure delegators between Boundary and Entity — empty |
| `entity/` | Entity | Business objects + persistence — empty |
| `persistence/` | — | SQLite connection helper (`db.py`) + schema (currently empty) |
| `data/` | — | Faker seed — TBD |
| `tests/` | — | pytest tests + `conftest.py` fixture (preserved) |
| `docs/` | — | todo list, active issues |
| `diagrams/` | — | source UML diagrams (reworked versions to be dropped in) |
| `.github/workflows/ci.yml` | — | CI: runs pytest on push/PR |

## Coverage so far

Nothing implemented yet on this branch. Sprint 1 stories will be the first to land.
