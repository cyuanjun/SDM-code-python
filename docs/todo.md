# Project TODO

Revamp-branch reset (2026-05-14). The previous catalogue of diagram typos, naming deviations, and per-sprint divergence notes was wiped when this branch was created — every entry described the old diagrams. New entries should reference the reworked diagrams as they land.

## Architecture items (carry over from main)

These are diagram-independent and survived the wipe.

- **Plain-text passwords** — when `UserAccount` is rebuilt, password hashing (bcrypt/argon2) is still needed before any real demo. Scope to a hardening sprint, not story-by-story.
- **No RBAC / no menu gating in `app.py`** — every page reachable by anyone, even unauthenticated. Tracked as a "High" item in [issues.md](issues.md).
- **Ownership not enforced at the entity layer** for fundraiser writes (update / suspend their own FRAs). Tracked as a "Medium" item in [issues.md](issues.md). The new diagrams may or may not specify this — confirm when implementing.
- **US-32 / US-33 (donee donation history)** still blocked on a `Donation` entity + a "donate" use case that the previous diagrams didn't include. Check whether the reworked diagrams cover this.

## Revamp-branch checkpoints

- [ ] Confirm reworked diagrams in place under [diagrams/](../diagrams/) and identify which sprints they cover.
- [ ] Re-derive [persistence/schema.sql](../persistence/schema.sql) from the new entity diagrams.
- [ ] Re-derive [data/seed.py](../data/seed.py) once the schema is settled.
- [ ] Sprint 1: write entity tests → entity → controller → boundary → wire into `app.py`.
- [ ] Sprint 2..4: same loop.
- [ ] Re-establish CI green on the rebuild.
- [ ] Re-write [docs/implementation.md](implementation.md) once Sprint 1 lands so the file/class reference matches the new code.
- [ ] Decide whether to keep the `.info (debug)` page idea on the rebuild — it was useful for inspection but is not on any diagram.
