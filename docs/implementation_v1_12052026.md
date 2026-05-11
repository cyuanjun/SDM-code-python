# Implementation Snapshot v1 — 2026-05-12

A point-in-time report of the SDM Online Fundraising System after Sprint 4 lands. Cross-references the live docs but is meant to be read standalone for marking / handover.

- **Live references:** [implementation.md](implementation.md) (full code index), [todo.md](todo.md) (deferred work + diagram catchup), [issues.md](issues.md) (open design questions), [differences.md](differences.md) (per-user-story diagram-vs-code diff), [../CLAUDE.md](../CLAUDE.md) (architecture rules).
- **Scope of this snapshot:** Sprints 1–4 complete. 41 of 43 user stories implemented across 34 Streamlit pages, 7 entities, 33 controllers, 110 passing tests.

---

## 1. What has been done

### Sprint 1 (12 stories) — closed
Onboarding + core flows for all four actors.

| US | Story |
|---|---|
| US-1 | Admin: create user profile |
| US-6 | Admin: create user account |
| US-11 | Admin: log in |
| US-12 | Admin: log out |
| US-13 | Fundraiser: create fundraising activity |
| US-18 | Fundraiser: log in |
| US-19 | Fundraiser: log out |
| US-21 | Donee: view fundraising activity |
| US-26 | Donee: log in |
| US-27 | Donee: log out |
| US-39 | Platform Manager: log in |
| US-40 | Platform Manager: log out |

Note: US-39 / US-40 PM login reuses the shared `LoginPage` + `UserAccount.login()`. The supplied diagrams predate Sprint 4's separate `platform_manager` table, so a real PM today logs in via a `UserAccount` row whose profile.role is `platform_manager`.

### Sprint 2 (9 stories) — closed
Admin/fundraiser CRUD + donee discovery.

| US | Story |
|---|---|
| US-2 / US-3 | Admin: view / update user profile |
| US-7 / US-8 | Admin: view / update user account |
| US-14 / US-15 | Fundraiser: view / update own FRA |
| US-20 | Donee: search FRAs |
| US-22 | Donee: save FRA to favourites |
| US-24 | Donee: view favourites |

### Sprint 3 (10 stories) — closed
Admin destructive ops + fundraiser/donee search + completed-activity flows.

| US | Story |
|---|---|
| US-4 / US-5 | Admin: delete / search user profile |
| US-9 / US-10 | Admin: suspend / search user account |
| US-16 / US-17 | Fundraiser: suspend / search own FRA |
| US-23 | Donee: delete a favourite |
| US-25 | Donee: search favourites |
| US-30 / US-31 | Fundraiser: search / view completed FRAs |

### Sprint 4 (10 stories) — closed 2026-05-12
Fundraiser metrics, platform-manager category management, platform-manager reporting.

| US | Story | New code |
|---|---|---|
| US-28 | Fundraiser: view FRA view count | `view_count` column + `view_fundraising_activity_view_count` + owner-only section on `ViewFundraisingActivityPage` |
| US-29 | Fundraiser: view FRA save count | `save_count` column + `view_fundraising_activity_save_count` + owner-only section on `ViewFundraisingActivityPage` |
| US-34 | PM: create FRA category | new entity `FundraisingActivityCategory`, table `fundraising_activity_category` |
| US-35 | PM: view FRA category | `view_fundraising_activity_category` |
| US-36 | PM: update FRA category | `update_fundraising_activity_category` |
| US-37 | PM: search FRA categories | `submit_search_criteria` |
| US-38 | PM: suspend FRA category | `suspend_fundraising_activity_category` |
| US-41 / US-42 / US-43 | PM: daily / weekly / monthly report | new entity `Report` (on-the-fly, no `report` table), new entity + table `platform_manager` |

**Cross-cutting Sprint 4 changes:**
- Replaced hardcoded `DEFAULT_CATEGORIES` in [boundary/create_fundraising_activity_page.py](../boundary/create_fundraising_activity_page.py) and [boundary/update_fundraiser_activity_page.py](../boundary/update_fundraiser_activity_page.py) with a live lookup against `fundraising_activity_category`.
- Wired `FavouriteList.save_fundraising_activity` / `delete_favourite` to bump and decrement `fundraising_activity.save_count`. View count is bumped on the donee's `selectFundraisingActivity` click.
- Sidebar prefixed `[PM]` for the eight new platform-manager pages.

---

## 2. What's missing — and why

### 2.1 User stories not implemented

| US | Story | Status | Reason |
|---|---|---|---|
| US-32 | Donee: search donation history | **Deferred** | Blocked on a missing donate use case + `Donation` entity. The Sprint 3 and Sprint 4 diagram drops both omitted a "donate" story, so there is no way to produce donation rows. Logged in [issues.md](issues.md). |
| US-33 | Donee: view donation history | **Deferred** | Same blocker as US-32. |
| US-39 | Platform Manager: log in | **Diagram-only / unverified** | A Sprint 1 diagram exists, but no Sprint 4 diagram introduces a separate PM login. The current implementation re-uses the shared `LoginPage` for everyone, which technically satisfies US-39 as drawn (Sprint 1) but does not gate by role. See §2.3. |
| US-40 | Platform Manager: log out | **Diagram-only / unverified** | Same as US-39. |

US-32 / US-33 are the only two stories with no implementation at all. The two PM-login stories are arguably "done by reuse" but were never re-drawn for Sprint 4.

### 2.2 Active design gaps (have implementations, but with known shortcuts)

| Item | Severity | Where logged |
|---|---|---|
| Plain-text passwords in [entity/user_account.py](../entity/user_account.py) and [entity/platform_manager.py](../entity/platform_manager.py) | Low (hardening) | [todo.md](todo.md), [issues.md](issues.md) |
| No RBAC / no menu gating in `app.py` — all 34 sidebar pages are visible and reachable by anonymous visitors | **High** | [issues.md](issues.md) |
| Ownership not enforced at the entity layer for `update_fundraiser_activity` (US-15) and `suspend_fundraising_activity` (US-16) — boundary filters today, no defense-in-depth | **Medium** | [issues.md](issues.md) |
| `Report.totalDonationAmount` / `totalDonationCount` always 0 because no donations exist | Knock-on from US-32/33 | [issues.md](issues.md); also surfaced as a caption on every generate-report page |
| Platform Manager has no login flow — `platform_manager` table is seeded but `app.py` doesn't sign PMs in. `Report.platformManagerId` is sourced from the first seeded row | Medium | [issues.md](issues.md) |
| Reports are generated on the fly with no `report` table — `reportId` is 0, `generatedAt` is `datetime.now()` | Open question — see §4 | [issues.md](issues.md) |
| Donee viewing an FRA increments `view_count` even when the viewer is the activity's owner — owner-self-views inflate the metric | Cosmetic | [todo.md](todo.md) Sprint 4 entry |

### 2.3 Why those choices

- **US-32/33 deferred (decided 2026-05-05, reconfirmed 2026-05-11).** Implementing them mid-sprint would require designing a `Donation` entity, a "donate" use case, a `donation` table, Faker seeding, and new sequence/class diagrams — all without a supplied diagram to anchor it. Scope expansion was rejected.
- **RBAC deferred to hardening.** A partial fix (only Sprint 3 / Sprint 4 admin pages) would create inconsistency with Sprint 1/2 admin pages. A clean fix is one connected refactor and was queued accordingly.
- **Platform Manager actor without login (decided 2026-05-11).** Mirrors the existing RBAC stance: actor pages exist and are reachable; full gating is the hardening sprint's job. The `platform_manager` table is real so that the `Report` entity has somewhere to source `platformManagerId` for the on-the-fly flow.
- **Reports on the fly, no `report` table (decided 2026-05-11).** Diagrams show only generate-and-display, no save step or view-past-reports story. Storing reports without a "view past reports" use case would add a schema for no user-visible benefit. Logged as an open question instead.

---

## 3. Differences from the supplied diagrams

Detailed per-user-story breakdown lives in [differences.md](differences.md); the [todo.md](todo.md) "Diagram updates needed before final marking" section is the canonical list. Categories below summarise the kinds of deviation introduced.

### 3.1 Diagram typos the code corrected (must fix in source diagrams before submission)

Code follows the corrected version in every case. Full list in [todo.md](todo.md); highlights per sprint:

- **Sprint 1:** US-1 `displaySucess` → `displaySuccess`. US-13 trailing-comma cosmetic. `Logout()` capitalisation on US-12/19/27/40 sequences.
- **Sprint 2:** US-7 sequence labels swapped (`ViewUserProfilePage` should be `ViewUserAccountPage`). US-14 boundary signature has wrong param type. US-15 lifelines are wrong entity. US-20 title is wrong story. US-22 entity header should be `FavouriteList`, not `FundraisingActivity`.
- **Sprint 3:** US-4 `displaySucess`. US-5 lifelines labelled `RemoveUserProfile*` (should be `SearchUserProfile*`). US-10 three errors: `displayMatchingUserProfile` → `displayMatchingUserAccount`, return type `List<UserProfile>` → `List<UserAccount>` in two places. US-17 / US-30 sequence end-call names. US-31 lifelines (`SearchCompletedActivity*` → `ViewCompletedActivity*`). US-32 end-call name (story deferred but typo logged for completeness).
- **Sprint 4:** US-29 title box says "US-28" (copy-paste); US-29 controller method named `viewFundraisingActivityViewCount` should be `…SaveCount`. US-35 title box says "US-34"; US-35 Boundary lists `displayCreateCategoryPage` (should be `displayViewCategoryPage`). US-36 Boundary same copy-paste error (should be `displayUpdateCategoryPage`). US-37 `submitSeachCriteria` missing the 'r'; US-37 Boundary lists `displaySuccess` instead of `displayMatchingFRACategory`. US-38 sequence has lowercase 'c' in `suspendFRAcategory`.

### 3.2 Implementation deviations from the diagrams (must update diagrams to match code)

These are intentional departures. Each has a logged justification.

- **`FundraisingActivity.submit_search_criteria` widened.** Diagrams for US-17 / US-20 / US-30 (and the deferred US-32) all show a one-arg `submitSearchCriteria(searchCriteria: String): List<FundraisingActivity>` on the same entity. The three live use cases need different filters; implementation took `submit_search_criteria(search_criteria, owner_account_id=None, status=None)`. Diagrams must be updated to add `ownerAccountId` and `status` parameters.
- **`FavouriteList.submit_search_criteria` widened.** US-25 diagram does not show account scoping but without it the method would leak other donees' favourites. Implementation takes an optional `account_id`. Diagram must be updated.
- **`UserProfile.delete_user_profile` FK semantics.** US-4 diagram does not specify behaviour when an account references the profile. Implementation returns `False` (safe delete). Diagram should add this clause.
- **Sprint 4 category-entity naming.** Diagrams use `ViewFRACategory`, `updateFRACategory`, `suspendFRACategory`. Implementation uses the full-word forms (`view_fundraising_activity_category`, `update_fundraising_activity_category`, `suspend_fundraising_activity_category`) to stay consistent with Sprint 1–3 naming (e.g. `suspend_fundraising_activity`, `view_user_profile`). `submitSeachCriteria` also normalised to the project-standard `submit_search_criteria`. Logged under [todo.md](todo.md) "Sprint 4 naming deviations".
- **Sprint 4 schema migration on `fundraising_activity`.** `view_count` and `save_count` columns were added (default 0). Plus the new tables `fundraising_activity_category` and `platform_manager`. Reflect in the persistent / data design diagrams.
- **Earlier schema migration** (already logged): `account_id` added to `user_account`; `owner_email` renamed to `owner_account_id` on `fundraising_activity`.

### 3.3 Pragmatic methods not in any class diagram (CLAUDE.md Exception A)

Sanctioned helpers. Each needs to land in the class diagrams before final marking.

- `UserProfile.view_all_profiles()` — feeds the profile dropdown on `CreateAccountPage`.
- `UserAccount.view_all_user_accounts()` — admin's account list.
- `FundraisingActivity.view_all_fundraising_activities()` — donee's clickable list.
- `FundraisingActivity.view_activities_by_owner(owner_account_id)` — fundraiser's scoped list.
- `FundraisingActivityCategory.view_all_categories()` — feeds the dropdown that replaced `DEFAULT_CATEGORIES`.
- `FundraisingActivity.increment_view_count(activity_id)` and `increment_save_count(activity_id, delta)` — Sprint 4 counter wiring; the diagrams only show *reading* the counters.

### 3.4 PM count display on the donee's page (literal diagram reading)

The US-28 / US-29 class diagrams place `displayFundraisingActivityViewCount` and `displayFundraisingActivitySaveCount` on `ViewFundraisingActivityPage` — the donee-facing page introduced by Sprint 1's US-21. Implementation follows the diagram literally: the page conditionally renders two metric tiles when the logged-in user owns the activity. Open question whether the diagrams should instead put these on a fundraiser-only page (Sprint 2 already has `ViewFundraiserActivityPage`). Logged in [todo.md](todo.md).

---

## 4. Open design questions

Decisions surfaced during Sprint 4 that the team should resolve before final submission. All logged in [issues.md](issues.md).

1. **Report persistence.** Generate-on-the-fly today (`report_id = 0`, `generated_at = datetime.now()`). Two options: (a) keep ephemeral, drop `reportId` from the diagrams; (b) add a `report` table + a "view past reports" story. Sprint 4 chose (a) provisionally.
2. **Donate flow / `Donation` entity.** Required to unblock US-32 / US-33 and to give the Sprint 4 reports non-zero donation totals. Needs a user story, an entity, a table, seed data, and updated US-32 / US-33 diagrams.
3. **Platform Manager login.** Currently no dedicated login. Either fold into existing `UserAccount.login()` by reusing `profile.role`, or add a separate login page that reads from the new `platform_manager` table.
4. **Ownership writes (hardening).** Add `owner_account_id` to `update_fundraiser_activity(...)` and `suspend_fundraising_activity(...)` for defence-in-depth. Diagram impact: US-15 / US-16 gain `ownerAccountId` on entity, controller, and message arrows.
5. **RBAC menu gating in `app.py`.** All 34 pages reachable by anonymous visitors today. Either cheap stopgap (require `session_state["user"]` on every admin/PM page) or proper role-keyed sidebar.
6. **Owner-self-view counts as a view.** Cosmetic; current behaviour inflates the fundraiser's own view metric. Easy fix once the counter-bump path takes an optional account_id.

---

## 5. Verification

```bash
source .venv/bin/activate
pytest                            # 110 passed in ~0.3s
python -m persistence.db          # creates app.db with empty schema (Sprint 4 tables included)
python -m data.seed               # populates 10 profiles, 10 accounts, 10 FRAs, 20 favourites, 5 categories, 5 PMs
streamlit run app.py              # serves the 34-page sidebar on http://localhost:8501
```

CI runs `pytest -v` on every push via [.github/workflows/ci.yml](../.github/workflows/ci.yml) (Python 3.11).

### Smoke-test paths for the marker

- **Sprint 4 US-28/29:** log in as a fundraiser, open `[Donee] View fundraising activity`, click one of your own activities — view count and save count tiles appear under the description.
- **Sprint 4 US-34..38:** `[PM] Create FRA category` → create one; `[PM] View FRA category` → pick it; `[PM] Update FRA category` → edit; `[PM] Search FRA categories` → free-text search; `[PM] Suspend FRA category` → flip status.
- **Sprint 4 US-41..43:** `[PM] Generate daily/weekly/monthly report` → date inputs → click. Metric tiles render; donation totals show 0 with a caption explaining why.
- **Counter wiring:** as a donee, save an activity from `[Donee] Save to favourites`, then visit `[Donee] View fundraising activity` as the activity's *owner* — the save-count metric should reflect the save.

---

## 6. Stat counts (at snapshot time)

| Layer | Count |
|---|---|
| Boundary classes | 34 (incl. `InfoPage` debug utility) |
| Controller classes | 33 |
| Entity classes | 7 (`UserProfile`, `UserAccount`, `FundraisingActivity`, `FavouriteList`, `FundraisingActivityCategory`, `PlatformManager`, `Report`) |
| Tables | 6 (`user_profile`, `user_account`, `fundraising_activity`, `favourite_list`, `fundraising_activity_category`, `platform_manager`) — `Report` has no table |
| User stories — implemented | 41 of 43 |
| User stories — deferred | 2 (US-32, US-33) |
| pytest tests | 110, all green |
| Sidebar pages | 34 (`[Admin]` 10, `[Fundraiser]` 7, `[Donee]` 6, `[PM]` 8, shared 2, debug 1) |

---

## 7. What to do next (suggested order)

1. **Diagram catchup pass** — apply the full [todo.md](todo.md) "Diagram updates needed before final marking" list to the source diagrams. Without this, the marker will see deviations not justified by an updated diagram.
2. **Decide on report persistence** (§4 item 1) — one-line decision unblocks a small diagram tweak.
3. **Decide on donate flow** (§4 item 2) — needed to unblock US-32/33 and make Sprint 4 reports meaningful.
4. **Hardening sprint** — RBAC, ownership checks, password hashing. Single connected change; do it last.
5. **Bump `RECORD_COUNT` to 100** in [data/seed.py](../data/seed.py) and re-run `python -m data.seed` before recording the marking demo.
6. **Hide `InfoPage`** before the final live demo (logged in [todo.md](todo.md) "Debug-only artifacts").
