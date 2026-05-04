# Project Issues

Active design gaps and blockers surfaced during sprint planning. Each entry states the problem, the decision, and what unblocks it. When an issue is resolved, move it to the bottom under "Resolved" with the resolution date.

## Donation tracking missing — US-32 and US-33 deferred to Sprint 4

**Problem.** US-32 (donee searches donation history) and US-33 (donee views donation history) both require knowing which campaigns each donee has donated to. The system currently stores no such record:

- No `donation` table in [persistence/schema.sql](../persistence/schema.sql).
- No "donate" use case shipped in Sprint 1 or Sprint 2.
- `favourite_list` tracks *interest*, not contributions, so it cannot stand in.

The Sprint 3 diagrams for US-32/US-33 assume donation data exists but no Sprint 1–3 user story creates it.

**Decision (2026-05-05).** Defer US-32 and US-33 to Sprint 4 alongside the actual donate flow. Sprint 3 ships the remaining 10 stories (US-4, US-5, US-9, US-10, US-16, US-17, US-23, US-25, US-30, US-31).

**What unblocks them.**
- A `Donation` entity + table (likely fields: `donation_id`, `account_id`, `activity_id`, `amount`, `donated_at`).
- A "donate" user story (or a documented Sprint 4 story) that produces donation rows.
- Faker seeding for the donations table so the search/view pages have rows to render.
- Updated US-32 / US-33 sequence + class diagrams once the entity exists.

## Admin pages have no authentication / RBAC gate (High)

**Problem.** None of the admin Boundary pages check that a user is logged in or has an admin profile before performing privileged actions. The sidebar in [app.py](../app.py) exposes every page to anonymous visitors. Concretely:

- [boundary/delete_user_profile_page.py](../boundary/delete_user_profile_page.py) — anonymous delete
- [boundary/suspend_user_account_page.py](../boundary/suspend_user_account_page.py) — anonymous suspend
- [boundary/search_user_account_page.py](../boundary/search_user_account_page.py) — leaks email/name to anonymous viewers
- [boundary/search_user_profile_page.py](../boundary/search_user_profile_page.py) — leaks role/description
- All Sprint 1/2 admin pages have the same gap (`view_user_account_page.py`, `update_user_profile_page.py`, `create_account_page.py`, etc.)

The 6 fundraiser/donee Sprint 3 pages already check `if "user" not in st.session_state` because they need `account_id` from session for data scoping. The admin pages don't perform the same check because admin actions don't depend on a session value, only on a role — and role enforcement is the deferred RBAC work.

**Decision (2026-05-05).** Logged here rather than patched mid-Sprint-3 because:

- RBAC is already an explicit out-of-scope item — see [CLAUDE.md](../CLAUDE.md) "Out-of-scope features": *"Full role-based access control — single-role check in `app.py` is enough for now"*.
- It's a pre-existing project-wide gap, not a Sprint 3 regression.
- A partial fix (only the four Sprint 3 admin pages) creates inconsistency with Sprint 1/2 admin pages without solving the problem.

**What unblocks it.** A future hardening sprint that does one of:

- (a) Cheap stopgap: add `if "user" not in st.session_state: warn + return` to *all* admin pages uniformly. Half a line per page; no role check; blocks anonymous walk-up only. Anyone with any account still has full admin access — useful as a stopgap, not as RBAC.
- (b) Proper RBAC: read `st.session_state["user"].profile_id`, look up the profile's role, gate per page. Likely also gates the sidebar (`PAGES`) by role so unauthorized pages don't appear.
- Diagram impact: none for (a). For (b), the `profile.role` field is already on the diagram; the gate is Boundary-internal logic the diagrams don't specify either way.

## Ownership not enforced at entity layer for fundraiser writes (Medium)

**Problem.** [entity/fundraising_activity.py](../entity/fundraising_activity.py) has two methods that mutate a fundraiser's activity by `activity_id` only, without verifying the caller owns it:

- `suspend_fundraising_activity(activity_id)` — Sprint 3 US-16
- `update_fundraiser_activity(activity_id, updated)` — Sprint 2 US-15

Today the relevant boundaries scope the dropdown to `view_activities_by_owner(session_user.account_id)`, so a normal user can only pick their own. But:

- Defense-in-depth: any future caller (URL param, another page, automated workflow) bypasses that boundary filter.
- A forged or stale Streamlit callback could submit an activity ID outside the dropdown's current contents.

The entity should refuse cross-tenant writes, not trust the caller.

**Decision (2026-05-05).** Logged rather than fixed mid-Sprint-3 because the fix requires a signature change on both methods plus their controllers and boundaries — which is the same diagram-as-contract deviation we already accumulated for `submit_search_criteria`. Kept out of Sprint 3 to avoid expanding the diagram-update backlog further; queue it for the same hardening sprint as the RBAC item above.

**What unblocks it.** A targeted fix:

- Add `owner_account_id` to both entity methods. SQL becomes `WHERE activity_id = ? AND owner_account_id = ?`. Returns `False` (no row affected) when the caller doesn't own the row.
- Update controllers and boundaries to forward `st.session_state["user"].account_id`.
- Add tests asserting cross-tenant suspend/update returns `False` and leaves the row unchanged.
- Diagram impact: US-15 and US-16 class + sequence diagrams gain `ownerAccountId: String` on the entity, controller, and message arrows. Log under [todo.md](todo.md) "Diagram updates needed before final marking".
