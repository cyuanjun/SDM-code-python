# Project TODO

Running list of **deferred work, temporary shortcuts, and architectural deviations** to fix before final marking.

Pure **diagram typos** (signatures, attribute types, boundary class names) live in [docs/diagram_typos.md](diagram_typos.md). This file tracks things that require code or scope changes, not just diagram edits.

## Debug-only artifacts (hide or remove before final demo)

- **[boundary/non_diagram/info_page.py](../boundary/non_diagram/info_page.py)** — `.info (debug)` sidebar page. Reads every table directly via `persistence/db.get_connection()`, bypassing the B-C-E layers. Shows row counts at the top, raw table dumps in tabs, and the live schema. Not a use case; for dev inspection only. Remove or hide before any recorded demo.

## Bootstrap deviations (data/seed.py)

These exist because the diagrams don't define an entry point for some required data. Each is idempotent on app startup. Either formalise the seed as a "first-time setup" use case on the diagrams, or accept it as a demo-only convention.

- **One default account per role** — `a001@a.com` (admin), `fr001@a.com` (fundraiser), `d001@a.com` (donee), `pm001@a.com` (platform manager), all with password `123`. Solves the chicken-and-egg admin-creates-the-first-admin problem implied by US-1 / US-6's "User admin" actor, and gives every role a logged-in-able starting point for the demo.
- **Demo donations (Sprint 3)** — three sample donations tied to the seeded donee + a "Demo hospital fund" activity owned by the seeded fundraiser. US-32 / US-33 introduce a `Donation` entity but no Sprint 1–3 diagram defines a "donate" use case, so the table would otherwise be empty. **Approved by lecturer (2026-05-15)** as an acceptable bootstrap convention — no further diagram work required.

## Exception A — off-diagram entity methods to power UX

Per CLAUDE.md "Exception A — Pragmatic Entity extensions for UX": each entry is an off-diagram method added to an Entity (plus a matching pure-delegator controller) to power a list/dropdown the Boundary needs. Each must land on the relevant class diagram before final marking.

- **`UserProfile.view_all_profiles()` + `ViewProfilesController`** — added in US-6 (2026-05-14) to populate the profile dropdown on `CreateAccountPage`. The `createAccount(..., profileId: String)` signature implies the admin picks an existing profile; without a list method the admin would have to type `prof_NNN` manually.
- **`FundraisingActivity.view_all_fundraising_activities()`** — added in US-21 (2026-05-14) so `ViewFundraisingActivityPage` can show a list before the donee triggers `viewFundraisingActivity(activityId)`. Method lives on the existing `ViewFundraisingActivityController` (Exception A allows extending an existing controller). Add to the US-21 class diagram on both the entity and the controller.
- **`UserAccount.view_all_user_accounts()`** — added in US-7 (2026-05-14) so `ViewUserAccountPage` / `UpdateUserAccountPage` can show a list before the admin picks an account by id. Method lives on the existing `ViewUserAccountController`. Add to the US-7 / US-8 class diagrams.
- **`FundraisingActivity.view_my_fundraising_activities(owner_account_id)`** — added in US-14 (2026-05-14) so `ViewMyFundraisingActivityPage` / `UpdateMyFundraisingActivityPage` can scope the picker to the logged-in fundraiser's own activities. Without this the fundraiser would have to know their own FRAIds verbatim. Method lives on `ViewMyFundraisingActivityController`. Add to the US-14 / US-15 class diagrams.
- **`Donation.view_my_donations(account_id)`** — added in US-33 (2026-05-15) so `ViewMyDonationHistoryPage` can show a picker before the donee triggers `viewMyDonationHistory(donationId)`. Method lives on `ViewMyDonationHistoryController`. Add to the US-33 class diagram.
- **`FundraisingActivity.increment_view_count(fra_id)` + `increment_save_count(fra_id, delta)`** — needed in Sprint 4 (US-28 / US-29). The diagrams only define **read** methods for the count columns, never write. Implementation fires `+1` view from US-21 (donee opens an activity), `+1` save from US-22 (favourite), `−1` save from US-23 (remove favourite). Add the increment methods + their semantics to the US-28 / US-29 sequence diagrams (or define a new use case that owns them).
- **Four `unsuspend_*` methods** (and four pure-delegator `Unsuspend*Controller` classes) — added 2026-05-15 so the consolidated `Manage*` pages can offer a single suspend/unsuspend toggle. Mirrors `suspend_user_profile` (US-4), `suspend_user_account` (US-9), `suspend_my_fundraising_activity` (US-16), `suspend_fundraising_activity_category` (US-38). Add each unsuspend method to its parent's class diagram, or define an unsuspend use case per actor.

## Lecturer decisions (no further diagram or code work required)

Things the lecturer has explicitly accepted as-is. The diagram does not need to change and the code stays as it is.

- **Demo donations seed (2026-05-15).** Three sample donations seeded against the default donee + fundraiser so US-32 / US-33 have data to display at demo time. Approved as an acceptable bootstrap convention. Lives in [data/seed.py](../data/seed.py); also listed under "Bootstrap deviations" above for completeness.
- **Email uniqueness on `UserAccount` (2026-05-15).** Lecturer instructed adding a `UNIQUE` constraint at the schema level. Implemented — see "Resolved" below.
- **No `displayError` on Sprint 1 boundary classes (2026-05-16).** Boundary diagrams only show `displaySuccess(...)`. Error display is treated as an implicit convention; diagrams will not be updated. Code keeps the inline `st.error(...)` calls.
- **Login failure return type on US-11 / US-18 / US-26 / US-39 (2026-05-16).** The four login diagrams keep typing `login(email, password): UserAccount` with no explicit failure branch. The implementation's `None`-on-no-match is accepted as an implicit convention; diagrams will not be updated.

## Deferred typos (accepted code-vs-diagram divergences)

Sprint 3 + Sprint 4 items where the diagram and code disagree but the team has chosen to accept the divergence rather than fix either side. Each entry has an inline `Deferred 2026-05-16` note in [diagram_typos.md](diagram_typos.md); this section is the consolidated index.

- **[US-23.jpg](../diagrams/sprint-3_diagrams/US-23.jpg) boundary class name.** Diagram: `ViewFavouritePage` (singular). Code: `ViewFavouriteListPage` (shared with US-24). Same screen, different names.
- **[US-25.jpg](../diagrams/sprint-3_diagrams/US-25.jpg) `viewMode` param.** Class diagram has 3-param `searchFavourite(viewMode, searchCriteria, accountId)`; sequence diagram has 2 params. Code uses the 2-param sequence version.
- **[US-25.jpg](../diagrams/sprint-3_diagrams/US-25.jpg) boundary class name.** Diagram: `ViewFavouritesPage`. Code: `SearchFavouritePage` (matches the user story "search my favourites list").
- ~~**[US-30.jpg](../diagrams/sprint-3_diagrams/US-30.jpg) / [US-31.jpg](../diagrams/sprint-3_diagrams/US-31.jpg) shared boundary class.**~~ **Resolved 2026-05-17.** Re-exported diagrams name the shared boundary `ViewMyCompletedFundraisingActivitiesPage`; code now consolidates US-30 + US-31 into a single file `boundary/view_my_completed_fundraising_activities_page.py` (mirrors the US-14/17 pattern).
- **[US-32.jpg](../diagrams/sprint-3_diagrams/US-32.jpg) "My" naming.** Diagram uses `SearchMyDonationHistoryController` and `searchMyDonationHistory` everywhere. Code drops "My" — `SearchDonationHistoryController` and `Donation.search_donation_history`. Function is identical; just a name preference.
- **[US-41.jpg](../diagrams/sprint-4_diagrams/US-41.jpg) / [US-42.jpg](../diagrams/sprint-4_diagrams/US-42.jpg) / [US-43.jpg](../diagrams/sprint-4_diagrams/US-43.jpg) shared `GenerateReportPage`.** All three Sprint 4 report diagrams share the same boundary class name (unusual — every other US has its own). Code consolidates into ONE [boundary/generate_report_page.py](../boundary/generate_report_page.py) with an internal radio selector that routes daily/weekly/monthly to the three diagram-defined controllers. Accepted as a deliberate consolidation.

## Open architectural items

Stack / policy concerns, not diagram-bound. Will re-surface as the rebuild touches each area.

- **Plain-text passwords.** Sprint 1's `UserAccount` stores the password as a plain string per the diagram. Hashing (bcrypt / argon2) belongs in a hardening sprint.

## Resolved

- ~~**No RBAC / menu gating in `app.py`.**~~ **Resolved 2026-05-15.** Sidebar now filters pages by the logged-in user's role (looked up via `ViewUserProfileController.view_user_profile`). Not signed in → only `Log In` + `.info (debug)`. Each role only sees its own actor's pages. `.info (debug)` stays visible for development; remove or hide along with the debug page before final demo.
- ~~**Email is not unique on `UserAccount`.**~~ **Resolved 2026-05-15** (lecturer instruction). `user_account.email` now has a `UNIQUE` constraint at the schema level. `UserAccount.create_account` returns `Optional[UserAccount]` — `None` on conflict; `UserAccount.update_user_account` returns `False` on conflict. Boundary surfaces "email already in use" errors. US-6 diagram still types the signature as `createAccount(...) -> UserAccount` with no failure branch — that diagram fix is now part of the existing "create / login failure branch" entry in [diagram_typos.md](diagram_typos.md).
