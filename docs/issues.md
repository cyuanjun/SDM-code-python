# Project Issues

Active design gaps and blockers. Each entry states the problem, the decision, and what unblocks it. Entries below carried over from `main` at the start of the revamp (2026-05-14); file references will become live again as the rebuild reintroduces those modules.

## Donation tracking missing — US-32 and US-33 status TBD

**Problem.** US-32 (donee searches donation history) and US-33 (donee views donation history) both require knowing which campaigns each donee has donated to. On the previous `main` branch this was deferred because:

- No `donation` table existed in the schema.
- No "donate" use case was shipped in any sprint.
- `favourite_list` tracks *interest*, not contributions, so it could not stand in.

**Decision (carry-over).** On `main`, US-32/US-33 were deferred indefinitely pending a `Donation` entity + a "donate" user story. Reports (US-41–43) generated correctly but reported `0` / `0.00` for donation columns because no donation rows existed.

**Question for the rebuild.** Do the reworked diagrams include a `Donation` entity and a "donate" use case? If yes, US-32 / US-33 can land naturally inside their sprint. If no, the same deferral applies.

**What unblocks them.**
- A `Donation` entity + table (likely fields: `donation_id`, `account_id`, `activity_id`, `amount`, `donated_at`).
- A "donate" user story that produces donation rows.
- Seeding for the donations table so the search/view pages have rows to render.

## Admin pages have no authentication / RBAC gate (High)

**Problem.** On `main`, the sidebar in `app.py` exposed every page to anonymous visitors. Admin Boundary pages performed privileged actions (delete profile, suspend account, search accounts) with no login check and no role check. The project-wide gap remained because partial fixes per-sprint would create inconsistency without solving the problem.

**Decision (carry-over).** Logged as a hardening-sprint item. The diagrams don't specify the gate either way — Boundary-internal logic.

**What unblocks it.** Once the rebuild has admin pages in place:
- (a) Cheap stopgap: `if "user" not in st.session_state: warn + return` on all admin pages uniformly. Blocks anonymous walk-up only.
- (b) Proper RBAC: read `st.session_state["user"].profile_id`, look up the profile's role, gate per page. Likely also gates the sidebar (`PAGES`) by role so unauthorised pages don't appear.

## Ownership not enforced at entity layer for fundraiser writes (Medium)

**Problem.** On `main`, `FundraisingActivity.suspend_fundraising_activity(activity_id)` and `update_fundraiser_activity(activity_id, updated)` mutated rows by `activity_id` only, without verifying the caller owned them. Boundary-level scoping (dropdown filtered to the caller's activities) was the only protection — a forged callback or alternate page bypassed it.

**Decision (carry-over).** Defense-in-depth fix queued for a hardening sprint. The reworked diagrams may or may not specify the check — confirm when reimplementing US-15 / US-16.

**What unblocks it.**
- Add `owner_account_id` (or equivalent) to both entity methods. SQL becomes `WHERE activity_id = ? AND owner_account_id = ?`. Returns `False` when the caller doesn't own the row.
- Update controllers and boundaries to forward the session user's account id.
- Tests asserting cross-tenant suspend/update returns `False`.
