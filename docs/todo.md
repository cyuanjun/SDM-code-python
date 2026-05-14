# Project TODO

Running list of deferred work, temporary shortcuts, and diagram typos to fix before final marking. Update as sprints progress.

## Sprint 1 diagram typos (fix in the source diagrams before marking)

Code follows the corrected (consensus) version in each case. Logged 2026-05-14 when the reworked Sprint 1 diagrams were read.

- **[US-11.jpg](../diagrams/sprint-1_diagrams/US-11.jpg) class diagram:** `UserAccount.profileId: Integer`. Every other diagram that includes `UserAccount` ([US-6](../diagrams/sprint-1_diagrams/US-06.jpg), [US-18](../diagrams/sprint-1_diagrams/US-18.jpg), [US-26](../diagrams/sprint-1_diagrams/US-26.jpg), [US-39](../diagrams/sprint-1_diagrams/US-39.jpg)) shows `profileId: String`. Should be `String`.
- **[US-01.jpg](../diagrams/sprint-1_diagrams/US-01.jpg) class diagram:** `UserProfile.suspended: String`. Every `suspended` attribute on `UserAccount` is `Boolean`, and a string-typed suspension flag has no semantics. Should be `Boolean`.
- **No `displayError` / `displayValidationError` on any boundary class diagram.** Every Sprint 1 boundary shows only `displaySuccess(...)`. Validation must live in the Boundary per the project rule, so an error-display method is implicit. Add `displayError(): void` (or equivalent) to every Sprint 1 boundary class diagram before final marking, or document the convention that error display is implicit.

## Open architectural items (carry over from main, re-log here as they apply)

These survived the revamp wipe because they're stack/policy concerns, not diagram-bound. Will re-surface as the rebuild touches each area.

- **Plain-text passwords.** Sprint 1's `UserAccount` will store the password as a plain string per the diagram. Hashing (bcrypt / argon2) belongs in a hardening sprint, not story-by-story.
- **No RBAC / menu gating in `app.py`.** Once boundaries are wired back in, anyone can reach any page until gating lands. See [issues.md](issues.md) once re-populated.
- **Ownership not enforced** at the entity layer for fundraiser writes. Re-check when US-15 / US-16 (or whichever stories the new sprints assign) arrive.
