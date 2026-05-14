# Project TODO

Running list of deferred work, temporary shortcuts, and diagram typos to fix before final marking. Update as sprints progress.

## Sprint 1 diagram typos (fix in the source diagrams before marking)

Code follows the corrected (consensus) version in each case. Logged 2026-05-14 when the reworked Sprint 1 diagrams were read.

- ~~**US-11.jpg `UserAccount.profileId: Integer`**~~ — **resolved 2026-05-14**: corrected diagram drops in with `profileId: String`.
- ~~**US-01.jpg `UserProfile.suspended: String`**~~ — **resolved 2026-05-14**: corrected diagram drops in with `suspended: Boolean`.
- **No `displayError` / `displayValidationError` on any boundary class diagram.** Every Sprint 1 boundary shows only `displaySuccess(...)`. Validation must live in the Boundary per the project rule, so an error-display method is implicit. Add `displayError(): void` (or equivalent) to every Sprint 1 boundary class diagram before final marking, or document the convention that error display is implicit.

## Diagram updates needed before final marking (Exception A)

Per CLAUDE.md "Exception A — Pragmatic Entity extensions for UX": each entry below is an off-diagram method added to an Entity (plus a matching pure-delegator controller) to power a list/dropdown the Boundary needs. Each must land on the relevant class diagram before final marking.

- **`UserProfile.view_all_profiles()` + `ViewProfilesController`** — added in US-6 (2026-05-14) to populate the profile dropdown on `CreateAccountPage`. The `createAccount(..., profileId: String)` signature implies the admin picks an existing profile; without a list method the admin would have to type `prof_NNN` manually.

## Open architectural items (carry over from main, re-log here as they apply)

These survived the revamp wipe because they're stack/policy concerns, not diagram-bound. Will re-surface as the rebuild touches each area.

- **Plain-text passwords.** Sprint 1's `UserAccount` stores the password as a plain string per the diagram. Hashing (bcrypt / argon2) belongs in a hardening sprint, not story-by-story.
- **Email is not unique on `UserAccount`.** The US-6 diagram doesn't declare email as a unique attribute, so `createAccount` allows duplicates. When US-11 / US-18 / US-26 / US-39 (login) land, login will match the first row with matching email + password — a real concern if duplicates ever exist. Either add a uniqueness check in the diagram or document the first-match login semantics.
- **No RBAC / menu gating in `app.py`.** Once more boundaries are wired in, anyone can reach any page until gating lands.
- **Ownership not enforced** at the entity layer for fundraiser writes. Re-check when US-15 / US-16 (or whichever stories the new sprints assign) arrive.
