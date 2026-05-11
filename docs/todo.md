# Project TODO

Running list of deferred work and known temporary shortcuts. Update as sprints progress.

## Temporary placeholders (replace later)

- **Seed `RECORD_COUNT = 10`** in [data/seed.py](../data/seed.py). Project spec calls for ~100 records per table for the marking demo. Bump `RECORD_COUNT` to `100` and re-run `python -m data.seed` before recording.
- **Hardcoded `"active"` status** in [controller/create_fundraising_activity_controller.py](../controller/create_fundraising_activity_controller.py).
  Acceptable for Sprint 1; revisit when status transitions (suspend, complete) are designed.
- **Plain-text passwords** in [entity/user_account.py](../entity/user_account.py).
  Sprint 2 hardening — add hashing (bcrypt/argon2) before any real demo.
- **Sprint 4 reports use a hardcoded `platform_manager_id`.** [entity/report.py](../entity/report.py) populates `Report.platformManagerId` with the first PM in the table because there is no PM login flow (RBAC deferred). Replace with `st.session_state["user"].id` once PM login is implemented.

## Deferred user stories

- **Sprint 3 (closed 2026-05-05):** US-4 / US-5 (delete & search profile), US-9 / US-10 (suspend & search account), US-16 / US-17 (suspend & search fundraiser FSA), US-23 (delete from favourites), US-25 (search favourites), US-30 / US-31 (search & view completed fundraiser activities). 10 stories.
- **Sprint 4 (in progress, scoped 2026-05-11):** US-28 / US-29 (FRA view & save counts), **US-34..US-38 (platform manager category management)**, US-41..US-43 (reports). 10 stories.
- **Still deferred (Sprint 4+ or hardening):** US-32 / US-33 (donee donation history) — confirmed 2026-05-11 still blocked on a missing donate use case + `Donation` entity. See [docs/issues.md](issues.md). US-39 / US-40 — no diagrams supplied; status unknown.
- **Hardening (any sprint):** password hashing, RBAC, ownership checks on fundraiser writes.

## Debug-only artifacts (remove before final demo)

- [boundary/info_page.py](../boundary/info_page.py) — `.info (debug)` page in the sidebar. Reads DB directly, bypassing B-C-E. For development inspection only; hide or delete before the recorded demo.

## Diagram updates needed before final marking

- **`UserProfile.view_all_profiles()` is implemented but not in any class diagram.** Added so [boundary/create_account_page.py](../boundary/create_account_page.py) can show a profile dropdown instead of a raw profile-ID input. Belongs on the UserProfile entity in the class diagram, and on a `ViewProfilesController` controller class. Folded into Sprint 2's view/update profile work.
- **`FundraisingActivity.view_all_fundraising_activities()` is implemented but not in the US-21 class diagram.** Added so the Donee can pick from a list before triggering `selectFundraisingActivity(activityID)`. Add this method to the `FundraisingActivity` entity and the `ViewFundraisingActivityController` controller in the updated class diagram.
- **`UserAccount.view_all_user_accounts()` and `view_user_account_controller.view_all_user_accounts()`** — added in Sprint 2 to power the admin's account list. Not in the US-7 diagram. Add to class diagram.
- **`FundraisingActivity.view_activities_by_owner()` and `view_fundraiser_activity_controller.view_activities_by_owner()`** — added in Sprint 2 to scope the fundraiser's list view to their own activities. Not in the US-14/15 diagrams. Add to class diagram.
- **`FavouriteList.remove_favourite()`** — added in Sprint 2 as a helper for the View Favourites page. **Resolved by Sprint 3 US-23:** renamed to `delete_favourite(activity_id, account_id)` and parameter order swapped to match the US-23 diagram exactly. No diagram update needed beyond confirming the Sprint 2 placeholder is gone.
- **Schema migration: `account_id` introduced on `user_account`, `owner_email` renamed to `owner_account_id` on `fundraising_activity`.** Reflect this in the persistent / data design diagrams before final marking.

### Sprint 3 (added 2026-05-05)

- **`FundraisingActivity.submitSearchCriteria` signature gains two parameters.** US-17, US-20, US-30 class diagrams all show a one-arg `submitSearchCriteria(searchCriteria: String): List<FundraisingActivity>` on the same Entity, but the three use cases need different filters (donee/all, fundraiser/own, fundraiser/own-completed). Implementation uses `submit_search_criteria(search_criteria: String, owner_account_id: String, status: String): List<FundraisingActivity>`. Update the class diagrams in all three stories (and their respective controllers) to add the `ownerAccountId` and `status` parameters before final submission.
- **`UserProfile.deleteUserProfile(profileId)` FK semantics not specified on the US-4 diagram.** Implementation returns `False` when the profile is referenced by any `user_account` row (FK violation), matching the safe-delete pattern used in `info_page.py`. Add a note to the US-4 sequence/class diagram (or the user story acceptance criteria) clarifying that deletion is refused when accounts depend on the profile.

### Sprint 4 (added 2026-05-11)

- **`FundraisingActivityCategory.view_all_categories()`** — added to power the dropdown in [boundary/create_fundraising_activity_page.py](../boundary/create_fundraising_activity_page.py) once `DEFAULT_CATEGORIES` is removed. Not in any US-34/35 diagram; same pattern as the existing `view_all_*` helpers logged above (Exception A in [CLAUDE.md](../CLAUDE.md)). Add to the class diagram on the `FundraisingActivityCategory` entity.
- **`FundraisingActivity.increment_view_count(activity_id)` and `increment_save_count(activity_id, delta)`** — needed to wire US-28 / US-29. The diagrams only show *reading* `viewCount` and `saveCount`; no story specifies *who* increments them or when. Implementation bumps `viewCount` when the donee opens the activity-details view, and bumps `saveCount` on `save_favourite` / decrements on `delete_favourite`. Add both methods + the increment semantics to the US-28 / US-29 sequence diagrams before final marking.
- **PM count display lives on the existing donee `ViewFundraisingActivityPage`** — per the US-28 / US-29 class diagram. The two `displayFundraisingActivity{View,Save}Count()` calls are rendered only when the logged-in user owns the activity. Consider whether the diagram should instead put these on a fundraiser-only page (`ViewFundraiserActivityPage` already exists in Sprint 2) — flagged as a possible diagram correction but code follows the literal diagram for now.
- **Platform Manager actor introduced without a login flow.** A `platform_manager` table exists and is seeded, but `app.py` does not log Platform Managers in. PM pages are accessible like other admin pages (consistent with the deferred-RBAC stance in [docs/issues.md](issues.md)). Report `platformManagerId` is sourced from the first seeded PM row. Diagram impact: none until RBAC is added.

## Sprint 3 diagram typos (fix in the source diagrams before marking)

Code follows the corrected version in each case.

- **US-4 class diagram:** Boundary method spelled `displaySucess(): void`. Should be `displaySuccess(): void` (matches the US-4 sequence diagram).
- **US-5 sequence:** Lifelines are labelled `RemoveUserProfilePage` and `RemoveUserProfileController`. Should be `SearchUserProfilePage` / `SearchUserProfileController` to match the US-5 class diagram and the user story title.
- **US-10 class diagram (three errors):**
  - Boundary method `displayMatchingUserProfile(userAccount: List<UserAccount>): void` — method name should be `displayMatchingUserAccount` (matches the sequence).
  - Controller method `submitSearchCriteria(searchCriteria: String): List<UserProfile>` — return type should be `List<UserAccount>`.
  - Entity method `submitSearchCriteria(searchCriteria: String): List<UserProfile>` — return type should be `List<UserAccount>`.
- **US-17 sequence:** End call is `displayMatchingUserAccount(activityList: List<FundraisingActivity>)`. Method name should be `displayMatchingFundraisingActivity` to match the US-17 class diagram.
- **US-30 sequence:** End call is `displayMatchingFavourite(activityList: List<FavouriteList>)`. Should be `displayMatchingCompletedActivity(activityList: List<FundraisingActivity>)` to match the US-30 class diagram.
- **US-31 sequence:** Lifelines are labelled `SearchCompletedActivityPage` and `SearchCompletedActivityController`. Should be `ViewCompletedActivityPage` / `ViewCompletedActivityController` to match the US-31 class diagram and the user story (view, not search).
- **US-32 sequence (story deferred to Sprint 4 — see [docs/issues.md](issues.md), but log the typo for completeness):** End call is `displayMatchingFavourite(activityList: List<FavouriteList>)`. Should be `displayMatchingCompletedActivity(activityList: List<FundraisingActivity>)` to match the US-32 class diagram.

## Sprint 4 diagram typos (fix in the source diagrams before marking)

Code follows the corrected version in each case.

- **US-29 title box** says "US-28" (copy-paste from US-28).
- **US-29 class diagram:** Controller method is named `viewFundraisingActivityViewCount(activityId: Integer): Integer`. Should be `viewFundraisingActivitySaveCount(activityId: Integer): Integer` to match the controller-class name `ViewFundraisingActivitySaveCountController` and the boundary's `displayFundraisingActivitySaveCount`. Same fix on the Entity's method.
- **US-35 title box** says "US-34" (copy-paste from US-34).
- **US-35 Boundary class diagram:** lists `displayCreateCategoryPage(): void`. Should be `displayViewCategoryPage(): void` to match the use case ("view category", not "create"). Affects the sequence diagram's lifeline self-call too.
- **US-36 Boundary class diagram:** lists `displayCreateCategoryPage(): void`. Should be `displayUpdateCategoryPage(): void` (copy-paste from US-34). The US-36 sequence diagram correctly shows `displayUpdateFRACategoryPage()`.
- **US-37 class diagram (typo):** method `submitSeachCriteria` is missing the 'r'. Should be `submitSearchCriteria` to match every other search story (Sprint 2 US-20, Sprint 3 US-10/17/30, etc.).
- **US-37 Boundary:** `displaySuccess(): void` is listed as a method on `SearchFundraisingActivityCategoryPage`. Search pages don't display success — should be `displayMatchingFRACategory(FRACategoryList: List<FundraisingActivityCategory>): void` (which the sequence diagram does show).
- **US-38 sequence:** controller-to-entity arrow is labelled `suspendFRAcategory(categoryId: Integer)` with lowercase 'c'. Should be `suspendFRACategory` to match the class diagram.

## Sprint 4 naming deviations (diagram-as-contract exception, log here)

The Sprint 4 diagrams introduce a `FundraisingActivityCategory` entity whose method names mix camel case with the `FRA` acronym (`ViewFRACategory`, `updateFRACategory`, `suspendFRACategory`). To stay consistent with existing entities (which use full words — `view_user_account`, `update_user_profile`, `suspend_user_account`, `suspend_fundraising_activity`), the implementation uses:

- `view_fundraising_activity_category` instead of `view_fra_category` / `ViewFRACategory`
- `update_fundraiser_activity_category` instead of `update_fra_category` / `updateFRACategory`
- `suspend_fundraising_activity_category` instead of `suspend_fra_category` / `suspendFRACategory`
- `submit_search_criteria` (already in use on `FundraisingActivity`) instead of `submitSeachCriteria`

Confirmed 2026-05-11. Update the US-34..US-38 class + sequence diagrams to use the full-word forms before final marking.

## Sprint 2 diagram typos (fix in the source diagrams before marking)

- **US-7 sequence:** actor's first arrow points to `ViewUserProfilePage` and entity is labelled `UserProfile`. Should be `ViewUserAccountPage` / `UserAccount` (matches the class diagram and the implemented code).
- **US-15 sequence:** controller and entity labels are `UpdateUserProfileController` / `UserProfile`. Should be `UpdateFundraiserActivityController` / `FundraisingActivity` (matches the class diagram).
- **US-22 class diagram:** entity box header says `FundraisingActivity` but the fields (`accountId`, `activityId`) and the sequence diagram are clearly `FavouriteList`. Header should read `FavouriteList`.
- **US-14 class diagram:** boundary method signature is `displayFundraisingActivity(userAccount: UserAccount): void`. Parameter type should be `FundraisingActivity` not `UserAccount`.
- **US-20 title text:** says "As a fundraiser, I want to update my fundraising activity..." but the actor and methods describe the donee search story. Replace title with the US-20 story from the user-stories table.

## Open design questions

- Role-based menu gating in `app.py` — all 26 pages are visible to everyone. Pages are prefixed by actor `[Admin]/[Fundraiser]/[Donee]` for legibility but there is no enforcement; an anonymous visitor can reach any admin page. Tracked as a "High" item in [issues.md](issues.md) ("Admin pages have no authentication / RBAC gate"). Originally pencilled in for Sprint 3; deferred to a hardening sprint to avoid a partial fix.
- Ownership not enforced at the entity layer for `update_fundraiser_activity` (Sprint 2 US-15) and `suspend_fundraising_activity` (Sprint 3 US-16). Tracked as a "Medium" item in [issues.md](issues.md). Fix requires a signature change on both methods plus diagram updates; queued for the same hardening sprint.
- Diagram fix: relabel actor on US-18 / US-19 Sprint 1 sequence diagrams from "Platform manager" to "Fundraiser".
