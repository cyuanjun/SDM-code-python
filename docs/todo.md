# Project TODO

Running list of deferred work and known temporary shortcuts. Update as sprints progress.

## Temporary placeholders (replace later)

- **Hardcoded fundraising-activity categories** in [boundary/create_fundraising_activity_page.py](../boundary/create_fundraising_activity_page.py) (`DEFAULT_CATEGORIES`).
  These are temporary. The proper "create category" use case (US-34) will be added in a later sprint by the Platform Manager role, with categories stored in the DB and looked up here. Once US-34 is implemented, replace `DEFAULT_CATEGORIES` with a query against the categories table.
- **Hardcoded `"active"` status** in [controller/create_fundraising_activity_controller.py](../controller/create_fundraising_activity_controller.py).
  Acceptable for Sprint 1; revisit when status transitions (suspend, complete) are designed.
- **Plain-text passwords** in [entity/user_account.py](../entity/user_account.py).
  Sprint 2 hardening — add hashing (bcrypt/argon2) before any real demo.

## Deferred user stories

- **Sprint 2:** US-2..US-5, US-7..US-10 (admin view/update/suspend/search), password hashing
- **Sprint 3:** US-14..US-17 (fundraiser FSA management), US-22..US-25 (donee favourites)
- **Sprint 4:** US-28..US-33 (analytics / history), **US-34..US-38 (platform manager category management)**, US-39..US-43 (reports)

## Debug-only artifacts (remove before final demo)

- [boundary/info_page.py](../boundary/info_page.py) — `.info (debug)` page in the sidebar. Reads DB directly, bypassing B-C-E. For development inspection only; hide or delete before the recorded demo.

## Diagram updates needed before final marking

- **`UserProfile.view_all_profiles()` is implemented but not in any class diagram.** Added so [boundary/create_account_page.py](../boundary/create_account_page.py) can show a profile dropdown instead of a raw profile-ID input. Belongs on the UserProfile entity in the class diagram, and likely a `ViewProfilesController` controller class. Will naturally fit alongside US-2 (view profile) and US-5 (search profiles) in Sprint 2.
- **`FundraisingActivity.view_all_fundraising_activities()` is implemented but not in the US-21 class diagram.** Added so the Donee can pick from a list before triggering `selectFundraisingActivity(activityID)`. Add this method to the `FundraisingActivity` entity and the `ViewFundraisingActivityController` controller in the updated class diagram. Will fit naturally with US-20 (donee search FSAs) when that lands in Sprint 3.

## Open design questions

- Role-based menu gating in `app.py` — currently all 6 pages are visible to everyone. Decide when to add proper RBAC (target: Sprint 2 alongside admin stories).
- Diagram fix: relabel actor on US-18 / US-19 sequence diagrams from "Platform manager" to "Fundraiser".
