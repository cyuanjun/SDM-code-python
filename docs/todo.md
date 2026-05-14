# Project TODO

Running list of **deferred work, temporary shortcuts, and architectural deviations** to fix before final marking.

Pure **diagram typos** (signatures, attribute types, boundary class names) live in [docs/diagram_typos.md](diagram_typos.md). This file tracks things that require code or scope changes, not just diagram edits.

## Debug-only artifacts (hide or remove before final demo)

- **[boundary/info_page.py](../boundary/info_page.py)** — `.info (debug)` sidebar page. Reads every table directly via `persistence/db.get_connection()`, bypassing the B-C-E layers. Shows row counts at the top, raw table dumps in tabs, and the live schema. Not a use case; for dev inspection only. Remove or hide before any recorded demo.

## Bootstrap deviations (data/seed.py)

These exist because the diagrams don't define an entry point for some required data. Each is idempotent on app startup. Either formalise the seed as a "first-time setup" use case on the diagrams, or accept it as a demo-only convention.

- **Default admin account** — `admin@example.com` / `admin`. Solves the chicken-and-egg admin-creates-the-first-admin problem implied by US-1 / US-6's "User admin" actor.
- **Default platform manager account (Sprint 4)** — `pm@example.com` / `pm`. PM-only Sprint 4 stories (US-34..38, US-41..43) need a logged-in `platform_manager`; no diagram defines how the first PM exists.
- **Demo donations (Sprint 3)** — three sample donations tied to a seeded donee + a seeded fundraiser activity. US-32 / US-33 introduce a `Donation` entity but no Sprint 1–3 diagram defines a "donate" use case, so the table would otherwise be empty.

## Exception A — off-diagram entity methods to power UX

Per CLAUDE.md "Exception A — Pragmatic Entity extensions for UX": each entry is an off-diagram method added to an Entity (plus a matching pure-delegator controller) to power a list/dropdown the Boundary needs. Each must land on the relevant class diagram before final marking.

- **`UserProfile.view_all_profiles()` + `ViewProfilesController`** — added in US-6 (2026-05-14) to populate the profile dropdown on `CreateAccountPage`. The `createAccount(..., profileId: String)` signature implies the admin picks an existing profile; without a list method the admin would have to type `prof_NNN` manually.
- **`FundraisingActivity.view_all_fundraising_activities()`** — added in US-21 (2026-05-14) so `ViewFundraisingActivityPage` can show a list before the donee triggers `viewFundraisingActivity(activityId)`. Method lives on the existing `ViewFundraisingActivityController` (Exception A allows extending an existing controller). Add to the US-21 class diagram on both the entity and the controller.
- **`UserAccount.view_all_user_accounts()`** — added in US-7 (2026-05-14) so `ViewUserAccountPage` / `UpdateUserAccountPage` can show a list before the admin picks an account by id. Method lives on the existing `ViewUserAccountController`. Add to the US-7 / US-8 class diagrams.
- **`FundraisingActivity.view_my_fundraising_activities(owner_account_id)`** — added in US-14 (2026-05-14) so `ViewMyFundraisingActivityPage` / `UpdateMyFundraisingActivityPage` can scope the picker to the logged-in fundraiser's own activities. Without this the fundraiser would have to know their own FRAIds verbatim. Method lives on `ViewMyFundraisingActivityController`. Add to the US-14 / US-15 class diagrams.
- **`Donation.view_my_donations(account_id)`** — added in US-33 (2026-05-15) so `ViewMyDonationHistoryPage` can show a picker before the donee triggers `viewMyDonationHistory(donationId)`. Method lives on `ViewMyDonationHistoryController`. Add to the US-33 class diagram.
- **`FundraisingActivity.increment_view_count(fra_id)` + `increment_save_count(fra_id, delta)`** — needed in Sprint 4 (US-28 / US-29). The diagrams only define **read** methods for the count columns, never write. Implementation fires `+1` view from US-21 (donee opens an activity), `+1` save from US-22 (favourite), `−1` save from US-23 (remove favourite). Add the increment methods + their semantics to the US-28 / US-29 sequence diagrams (or define a new use case that owns them).

## Open architectural items

Stack / policy concerns, not diagram-bound. Will re-surface as the rebuild touches each area.

- **Plain-text passwords.** Sprint 1's `UserAccount` stores the password as a plain string per the diagram. Hashing (bcrypt / argon2) belongs in a hardening sprint.
- **Email is not unique on `UserAccount`.** The US-6 diagram doesn't declare email as a unique attribute, so `createAccount` allows duplicates. Login matches the first row with matching email + password — a real concern if duplicates ever exist. Either add a uniqueness check in the diagram or document the first-match login semantics.
- **No RBAC / menu gating in `app.py`.** Anyone can reach any page until gating lands. Sidebar entries are prefixed `[Admin]/[Fundraiser]/[Donee]/[PM]` for legibility only, not enforcement.
