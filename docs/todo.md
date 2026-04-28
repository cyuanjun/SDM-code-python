# Project TODO

Running list of deferred work and known temporary shortcuts. Update as sprints progress.

## Temporary placeholders (replace later)

- **Seed `RECORD_COUNT = 10`** in [data/seed.py](../data/seed.py). Project spec calls for ~100 records per table for the marking demo. Bump `RECORD_COUNT` to `100` and re-run `python -m data.seed` before recording.
- **Hardcoded fundraising-activity categories** in [boundary/create_fundraising_activity_page.py](../boundary/create_fundraising_activity_page.py) (`DEFAULT_CATEGORIES`).
  These are temporary. The proper "create category" use case (US-34) will be added in a later sprint by the Platform Manager role, with categories stored in the DB and looked up here. Once US-34 is implemented, replace `DEFAULT_CATEGORIES` with a query against the categories table.
- **Hardcoded `"active"` status** in [controller/create_fundraising_activity_controller.py](../controller/create_fundraising_activity_controller.py).
  Acceptable for Sprint 1; revisit when status transitions (suspend, complete) are designed.
- **Plain-text passwords** in [entity/user_account.py](../entity/user_account.py).
  Sprint 2 hardening — add hashing (bcrypt/argon2) before any real demo.

## Deferred user stories

- **Sprint 3 (proposed):** US-4 / US-5 (suspend & search profile), US-9 / US-10 (suspend & search account), US-16 / US-17 (suspend & search fundraiser FSA), US-23 (delete from favourites), US-25 (search favourites), US-28 / US-29 (FSA view & favourite counts)
- **Sprint 4 (proposed):** US-30..US-33 (history / donations), **US-34..US-38 (platform manager category management)**, US-41..US-43 (reports)
- **Hardening (any sprint):** password hashing

## Debug-only artifacts (remove before final demo)

- [boundary/info_page.py](../boundary/info_page.py) — `.info (debug)` page in the sidebar. Reads DB directly, bypassing B-C-E. For development inspection only; hide or delete before the recorded demo.

## Diagram updates needed before final marking

- **`UserProfile.view_all_profiles()` is implemented but not in any class diagram.** Added so [boundary/create_account_page.py](../boundary/create_account_page.py) can show a profile dropdown instead of a raw profile-ID input. Belongs on the UserProfile entity in the class diagram, and on a `ViewProfilesController` controller class. Folded into Sprint 2's view/update profile work.
- **`FundraisingActivity.view_all_fundraising_activities()` is implemented but not in the US-21 class diagram.** Added so the Donee can pick from a list before triggering `selectFundraisingActivity(activityID)`. Add this method to the `FundraisingActivity` entity and the `ViewFundraisingActivityController` controller in the updated class diagram.
- **`UserAccount.view_all_user_accounts()` and `view_user_account_controller.view_all_user_accounts()`** — added in Sprint 2 to power the admin's account list. Not in the US-7 diagram. Add to class diagram.
- **`FundraisingActivity.view_activities_by_owner()` and `view_fundraiser_activity_controller.view_activities_by_owner()`** — added in Sprint 2 to scope the fundraiser's list view to their own activities. Not in the US-14/15 diagrams. Add to class diagram.
- **`FavouriteList.remove_favourite()`** — added in Sprint 2 as a helper for the View Favourites page. Foreshadows US-23 (delete from favourites); add to class diagram when US-23 is formalized.
- **Schema migration: `account_id` introduced on `user_account`, `owner_email` renamed to `owner_account_id` on `fundraising_activity`.** Reflect this in the persistent / data design diagrams before final marking.

## Sprint 2 diagram typos (fix in the source diagrams before marking)

- **US-7 sequence:** actor's first arrow points to `ViewUserProfilePage` and entity is labelled `UserProfile`. Should be `ViewUserAccountPage` / `UserAccount` (matches the class diagram and the implemented code).
- **US-15 sequence:** controller and entity labels are `UpdateUserProfileController` / `UserProfile`. Should be `UpdateFundraiserActivityController` / `FundraisingActivity` (matches the class diagram).
- **US-22 class diagram:** entity box header says `FundraisingActivity` but the fields (`accountId`, `activityId`) and the sequence diagram are clearly `FavouriteList`. Header should read `FavouriteList`.
- **US-14 class diagram:** boundary method signature is `displayFundraisingActivity(userAccount: UserAccount): void`. Parameter type should be `FundraisingActivity` not `UserAccount`.
- **US-20 title text:** says "As a fundraiser, I want to update my fundraising activity..." but the actor and methods describe the donee search story. Replace title with the US-20 story from the user-stories table.

## Open design questions

- Role-based menu gating in `app.py` — currently all 16 pages are visible to everyone. Pages are prefixed by actor `[Admin]/[Fundraiser]/[Donee]` for legibility but no enforcement. Decide when to add proper RBAC (target: Sprint 3).
- Diagram fix: relabel actor on US-18 / US-19 Sprint 1 sequence diagrams from "Platform manager" to "Fundraiser".
