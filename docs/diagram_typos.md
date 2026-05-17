# Diagram typos

Consolidated list of every divergence between the source UML diagrams and the implemented code. In every case the code follows the **corrected** version; the diagram itself needs to be updated before final marking.

When a typo gets fixed in the source diagram, strike it through and add a `**resolved YYYY-MM-DD**` note rather than deleting it — keeps a record of what was fixed.

For *Exception A* additions (off-diagram methods added to power UX), *bootstrap deviations* (default role accounts + demo donation seeds), and *open architectural items* (plain-text passwords, email uniqueness), see [docs/todo.md](todo.md).

---

## Sprint 1

Diagrams: [diagrams/sprint-1_diagrams/](../diagrams/sprint-1_diagrams/).

- ~~**[US-01.jpg](../diagrams/sprint-1_diagrams/US-01.jpg) `UserProfile.suspended: String`**~~ — **resolved 2026-05-14**. Re-exported diagram now types `suspended: Boolean`, matching every other `suspended` attribute in the project.
- ~~**[US-11.jpg](../diagrams/sprint-1_diagrams/US-11.jpg) `UserAccount.profileId: Integer`**~~ — **resolved 2026-05-14**. Re-exported diagram now types `profileId: String`, matching US-6 / US-18 / US-26 / US-39.
- ~~**No `displayError` / `displayValidationError` on any boundary class diagram.**~~ **Deferred by lecturer 2026-05-16.** Diagram convention is that error display is implicit; the diagrams will continue to show only `displaySuccess(...)`. Code behaviour unchanged. Tracked under "Lecturer decisions" in [todo.md](todo.md).
- ~~**[US-13.jpg](../diagrams/sprint-1_diagrams/US-13.jpg) `createFundraisingActivity` is missing `ownerAccountId: String`.**~~ **Resolved 2026-05-16.** Re-exported diagram now signs the method `createFundraisingActivity(title, description, targetAmount, FRACatId, startDate, endDate, ownerAccountId: String): FundraisingActivity` on both the class diagram and sequence diagram, matching the 7-param implementation. Boundary still supplies `ownerAccountId` from `st.session_state["user"].account_id`.
- ~~**[US-13.jpg](../diagrams/sprint-1_diagrams/US-13.jpg) `category: String` is a free-text field, bypassing the curated FundraisingActivityCategory list.**~~ **Resolved 2026-05-18.** The 2026-05-18 diagram replaces the entity attribute `category: String` with `FRACatId: String` (FK to `FundraisingActivityCategory`) and updates `createFundraisingActivity` / `updateMyFundraisingActivity` parameter lists accordingly. The change cascades through every FRA class diagram (US-14, US-15, US-17, US-20, US-21, US-30, US-31). Schema adds `fra_cat_id TEXT NOT NULL REFERENCES fundraising_activity_category(fra_cat_id)`. Create/update boundaries now render the category as a `st.selectbox` populated by `FundraisingActivityCategory.view_all_categories()` (active categories only — a legitimate FK dropdown, not a String enum). Search methods (US-17, US-20, US-30, donation history, favourite search) JOIN to `fundraising_activity_category` and match `category_name` so existing UX continues to work. Tests' shared `conftest.py` seeds a default `cat_001` "Test" category so FK-dependent tests don't each have to bootstrap one.
- ~~**Login failure return type not on diagrams ([US-11.jpg](../diagrams/sprint-1_diagrams/US-11.jpg), [US-18.jpg](../diagrams/sprint-1_diagrams/US-18.jpg), [US-26.jpg](../diagrams/sprint-1_diagrams/US-26.jpg), [US-39.jpg](../diagrams/sprint-1_diagrams/US-39.jpg)).**~~ **Deferred by lecturer 2026-05-16.** Login diagrams keep typing `login(email, password): UserAccount` with no failure branch; implementation's `None`-on-no-match is accepted as an implicit convention. Code behaviour unchanged. Tracked under "Lecturer decisions" in [todo.md](todo.md).

## Sprint 2

Diagrams: [diagrams/sprint-2_diagrams/](../diagrams/sprint-2_diagrams/).

- ~~**[US-14.jpg](../diagrams/sprint-2_diagrams/US-14.jpg) boundary method:** `displayMyFundraisingActivity(fundraisingActivity: FundraiserActivity): void`. `FundraiserActivity` is not an entity. Should be `FundraisingActivity` to match the Sprint 1 US-13 entity.~~ **Resolved 2026-05-16.** Re-exported diagram now types the boundary method (class + sequence) `displayMyFundraisingActivity(fundraisingActivity: FundraisingActivity): void`.
- ~~**[US-15.jpg](../diagrams/sprint-2_diagrams/US-15.jpg) class diagram is missing `ownerAccountId` on the update method.**~~ **Resolved 2026-05-16.** Re-exported diagram now signs the method (class + sequence) `updateFundraisingActivity(ownerAccountId: String, FRAId: String, updatedActivity: FundraisingActivity): Boolean` consistently — 3 params, correct entity type. Code renamed to match: entity method [`update_fundraising_activity`](../entity/fundraising_activity.py) (previously `update_fundraiser_activity`); controller delegator updated to the same name. **Further refined 2026-05-17:** method renamed `updateFundraisingActivity` → `updateMyFundraisingActivity` (controller + entity) and parameter `updatedActivity` / `updatedFundraiser` → `updatedMyFRA` for consistency with the per-US class names `UpdateMyFundraisingActivityPage` / `UpdateMyFundraisingActivityController` and to mark this as an owner-scoped operation. Code now uses `update_my_fundraising_activity` / `updated_my_fra`.
- ~~**[US-20.jpg](../diagrams/sprint-2_diagrams/US-20.jpg) boundary class name:** `ViewFundraisingActivities` (no `Page` suffix). Project rule mandates the `Page` suffix on every Boundary class — implementation uses `ViewFundraisingActivitiesPage`.~~ **Resolved 2026-05-16.** Re-exported diagram now names the boundary `ViewFundraisingActivitiesPage`.
- ~~**[US-24.jpg](../diagrams/sprint-2_diagrams/US-24.jpg) return type:** `viewFavourite(accountId: String): Favourite` — returns a single Favourite, but the user story is "view all my favourites" which implies many.~~ **Resolved 2026-05-16.** Re-exported diagram names the boundary `ViewFavouriteListPage`, the controller `ViewFavouriteListController`, and the method `viewFavouriteList(accountId: String): List<Favourite>`. Code renamed to match: [boundary/view_favourite_list_page.py](../boundary/view_favourite_list_page.py), [controller/view_favourite_list_controller.py](../controller/view_favourite_list_controller.py), `Favourite.view_favourite_list`.

## Sprint 3

Diagrams: [diagrams/sprint-3_diagrams/](../diagrams/sprint-3_diagrams/).

- ~~**[US-09.jpg](../diagrams/sprint-3_diagrams/US-09.jpg) `UserAccount.profileId: Integer`.**~~ **Resolved 2026-05-16.** Re-exported diagram types `profileId: String`.
- ~~**[US-09.jpg](../diagrams/sprint-3_diagrams/US-09.jpg) boundary class mismatch:** class diagram lists `ViewUserAccountPage`, sequence diagram shows `SuspendUserAccountPage`.~~ **Resolved 2026-05-16.** Both class + sequence now use `ViewUserAccountPage`, matching the reuse pattern.
- ~~**[US-16.jpg](../diagrams/sprint-3_diagrams/US-16.jpg) boundary class:** lists `ViewFundraisingActivityPage` (the donee's view, US-21). Should be `ViewMyFundraisingActivityPage`.~~ **Resolved 2026-05-16.** Diagram now names the boundary `ViewMyFundraisingActivityPage`.
- ~~**[US-16.jpg](../diagrams/sprint-3_diagrams/US-16.jpg) entity attribute typo:** `suspended: Bool`.~~ **Resolved 2026-05-16.** Diagram now types `suspended: Boolean`.
- ~~**[US-25.jpg](../diagrams/sprint-3_diagrams/US-25.jpg) signature mismatch:** class shows `searchFavourite(viewMode: String, searchCriteria: String, accountId: String)`; sequence shows `searchFavourite(searchCriteria: String, accountId: String)`.~~ **Resolved 2026-05-17.** Re-exported diagram drops `viewMode`; both class + sequence now sign `searchFavourite(accountId: String, searchCriteria: String): List<Favourite>` (owner first, 2 params). Code's `Favourite.search_favourite` + `SearchFavouriteController.search_favourite` param order flipped to match.
- ~~**[US-25.jpg](../diagrams/sprint-3_diagrams/US-25.jpg) boundary class:** named `ViewFundraisingActivitiesPage` — collides with the Sprint 2 US-20 boundary.~~ **Resolved 2026-05-16 / further 2026-05-17.** Re-exported diagram now names the boundary `ViewFavouriteListPage` (shared with US-23 + US-24); code's per-US `SearchFavouritePage` retired and the US-25 search method merged into `boundary/view_favourite_list_page.py` (mirrors US-14/17 and US-30/31 patterns).
- ~~**[US-30.jpg](../diagrams/sprint-3_diagrams/US-30.jpg) boundary class collision:** class + sequence diagrams name the boundary `ViewMyFundraisingActivitiesPage`~~ **Resolved 2026-05-16 / further 2026-05-17 / final 2026-05-18.** The 2026-05-18 diagram explicitly places US-30 on `ViewMyFundraisingActivitiesPage` (shared with US-17 and US-31) — same as the original 2026-05-16 collision said, except now intentional. Code follows: the interim `ViewMyCompletedFundraisingActivitiesPage` (created 2026-05-17) retired; US-17 + US-30 + US-31 all live on `boundary/view_my_fundraising_activities_page.py` with an `[All]` / `[Completed]` tab toggle (matches the sketch design).
- ~~**[US-30.jpg](../diagrams/sprint-3_diagrams/US-30.jpg) `searchMyCompletedFRA` parameter order:**~~ **Resolved 2026-05-16.** Diagram now signs the method `searchMyCompletedFRA(ownerAccountId, searchCriteria)` (owner first), matching every other owner-scoped method.
- ~~**[US-31.jpg](../diagrams/sprint-3_diagrams/US-31.jpg) per-id detail vs list semantics**~~ **Resolved 2026-05-17 / boundary moved 2026-05-18.** 2026-05-17 reframed the method to list semantics (`viewMyCompletedFundraisingActivities(owner): List<FundraisingActivity>`). 2026-05-18 moves the boundary from `ViewMyCompletedFundraisingActivitiesPage` to `ViewMyFundraisingActivitiesPage` (shared with US-17 + US-30). Code follows.
- ~~**[US-23.jpg](../diagrams/sprint-3_diagrams/US-23.jpg) boundary class (round 2)**~~ **Resolved 2026-05-18.** The 2026-05-18 export moves US-23's boundary from `ViewFavouriteListPage` to `ViewFundraisingActivityPage` — the donee removes-from-favourites on the activity detail page (symmetric with US-22 Save on the same page; parallel to US-15 Update + US-16 Suspend on `ViewMyFundraisingActivityPage`). Code follows: `[Remove from favourites]` button now lives on the activity detail page, conditionally shown when the activity is already favourited. `ViewFavouriteListPage` and the consolidated `MyFavouritesPage` no longer render per-row Remove buttons.
- ~~**[US-33.jpg](../diagrams/sprint-3_diagrams/US-33.jpg) per-id detail vs list semantics**~~ **Resolved 2026-05-18.** The 2026-05-18 diagram reframes US-33 from per-id detail (`viewMyDonationHistory(accountId, donationId): Donation`) to list semantics (`viewMyDonationHistories(accountId): List<Donation>`); boundary `ViewMyDonationHistoryPage` (singular) → `ViewMyDonationHistoriesPage` (plural, shared with US-32). Same shape as the US-31 reframe. Code follows: old per-id method + controller + boundary deleted; new list method + controller; the Exception A `Donation.view_my_donations` is retired (was the picker; now replaced by the diagram-defined list method).
- ~~**[US-36.jpg](../diagrams/sprint-4_diagrams/US-36.jpg) signature flatten**~~ **Resolved 2026-05-18.** The 2026-05-18 diagram changes `updateFundraisingActivityCategory(FRACatId, updatedFRACategory: FundraisingActivityCategory)` → `updateFundraisingActivityCategory(FRACatId, categoryName, description)` — direct field params instead of a wrapping entity object. `suspended` is no longer settable via this method (US-38 handles suspend/unsuspend separately). Code follows.
- ~~**[US-32.jpg](../diagrams/sprint-3_diagrams/US-32.jpg) controller class name + sequence/class diagram inconsistency**~~ **Resolved 2026-05-16 / further 2026-05-18.** 2026-05-16 export aligned class + sequence at `SearchMyDonationHistoryController`. The 2026-05-18 export pluralises to `SearchMyDonationHistoriesController` (matching the boundary `ViewMyDonationHistoriesPage`); code aligned — `SearchDonationHistoryController` retired in favour of `SearchMyDonationHistoriesController`. The previously-deferred "no My in code" divergence is now resolved.
- ~~**[US-32.jpg](../diagrams/sprint-3_diagrams/US-32.jpg) `accountId: Integer`.**~~ **Resolved 2026-05-16.** Diagram now types `accountId: String`.
- ~~**[US-23.jpg](../diagrams/sprint-3_diagrams/US-23.jpg) boundary class name:** Diagram shows `ViewFavouritePage` (singular) for the remove-favourite action; should be `ViewFavouriteListPage` to match the renamed US-24 boundary (same screen).~~ **Resolved 2026-05-17.** Re-exported diagram now names the boundary `ViewFavouriteListPage` (class + sequence consistent); also fixes the user-story wording from "suspend" → "remove" and "favourite list" → "favourites list". Code already used `ViewFavouriteListPage` — no code change.

## Sprint 4

Diagrams: [diagrams/sprint-4_diagrams/](../diagrams/sprint-4_diagrams/).

- ~~**[US-28.jpg](../diagrams/sprint-4_diagrams/US-28.jpg) / [US-29.jpg](../diagrams/sprint-4_diagrams/US-29.jpg) boundary class:** lists `ViewFundraisingActivityPage` (the donee's page from US-21) — but the actor is **Fundraiser** viewing their own counts.~~ **Resolved 2026-05-16.** Re-exported diagrams now name the boundary `ViewMyFundraisingActivityPage` on both class + sequence, matching the Fundraiser actor.
- ~~**[US-41.jpg](../diagrams/sprint-4_diagrams/US-41.jpg) / [US-42.jpg](../diagrams/sprint-4_diagrams/US-42.jpg) / [US-43.jpg](../diagrams/sprint-4_diagrams/US-43.jpg) `generate*Report` signatures are missing `platformManagerId`.**~~ **Resolved 2026-05-16.** All three methods now sign as `(startDate: Date, endDate: Date, platformManagerId: String): Report` on both class + sequence diagrams, matching the code's parameter order.
- ~~**[US-41.jpg](../diagrams/sprint-4_diagrams/US-41.jpg) / [US-42.jpg](../diagrams/sprint-4_diagrams/US-42.jpg) / [US-43.jpg](../diagrams/sprint-4_diagrams/US-43.jpg) `Report.generatedAt: Date`.**~~ **Resolved 2026-05-16.** Re-exported diagrams now type `generatedAt: datetime`, matching the code's `datetime.datetime` value.
- **[US-41.jpg](../diagrams/sprint-4_diagrams/US-41.jpg) / [US-42.jpg](../diagrams/sprint-4_diagrams/US-42.jpg) / [US-43.jpg](../diagrams/sprint-4_diagrams/US-43.jpg) shared boundary class name.** All three diagrams name the boundary class `GenerateReportPage`, but each describes a different use case. Implementation uses ONE `GenerateReportPage` with an internal radio selector for daily / weekly / monthly, routing to the three diagram-defined controllers. **Deferred 2026-05-16** — accepted as a deliberate consolidation; splitting into per-story boundaries would add three files for the same UI without behavioural change.

## UX consolidation (no individual diagram is wrong — the *set* deviates)

Added 2026-05-15 after the design sketch consolidating per-US pages into resource-focused screens. Every diagram-defined per-US Boundary class **still exists** as a tested artifact, but the sidebar wires the seven combined pages below instead. Each combined page calls the same Controllers and Entities the per-US Boundaries do.

The diagrams themselves don't need to change — the per-US classes are still real, still tested, and still 1:1 with their stories. The deviation is purely in *which* Boundary classes get wired into the sidebar. Either add a "UX wireframe" diagram showing the seven combined pages alongside the existing class diagrams, or document the consolidation as a deliberate refactor of the UI surface.

| Combined page (sidebar entry) | Per-US Boundary classes it replaces in the sidebar |
|---|---|
| `ManageUserProfilePage` | `CreateProfilePage`, `ViewUserProfilePage`, `UpdateUserProfilePage`, `ViewUserProfilesPage` (and the suspend button on `ViewUserProfilePage`) |
| `ManageUserAccountPage` | `CreateAccountPage`, `ViewUserAccountPage`, `UpdateUserAccountPage`, `ViewUserAccountsPage` (and the suspend button on `ViewUserAccountPage`) |
| `ManageMyFundraisingActivityPage` | `CreateFundraisingActivityPage`, `ViewMyFundraisingActivityPage`, `UpdateMyFundraisingActivityPage`, `ViewMyFundraisingActivitiesPage`, `ViewMyCompletedFundraisingActivitiesPage` (All/Completed tabs) |
| `BrowseFundraisingActivityPage` | `ViewFundraisingActivityPage` (donee detail + US-22 save button), `ViewFundraisingActivitiesPage` (US-20 search) |
| `MyFavouritesPage` | `ViewFavouriteListPage` (US-24 list + US-25 search). US-23 Remove lives on `ViewFundraisingActivityPage` per the 2026-05-18 diagram. |
| `MyDonationsPage` | `ViewMyDonationHistoryPage`, `ViewMyDonationHistoriesPage` |
| `ManageFundraisingActivityCategoryPage` | `CreateFundraisingActivityCategoryPage`, `ViewFundraisingActivityCategoryPage`, `UpdateFundraisingActivityCategoryPage`, `ViewFundraisingActivityCategoriesPage` (suspend button on view detail) |

The 8th sidebar entry (`GenerateReportPage`) was already shared across US-41/42/43 on the diagrams; nothing changes there.

## Unsuspend toggle (Exception A, UX)

Added 2026-05-15. The diagrams define `suspend*` methods on `UserProfile` (US-4), `UserAccount` (US-9), `FundraisingActivity` (US-16), and `FundraisingActivityCategory` (US-38) — but no corresponding **unsuspend** methods. Once suspended, the only way to clear the flag through the diagram-defined surface was via the update form (toggling the `suspended` checkbox), which is awkward.

To support a toggle button in the consolidated `Manage*` pages, four `unsuspend_*` Exception A methods were added (and four pure-delegator controllers):

| Entity | Suspend (diagram-defined) | Unsuspend (Exception A) |
|---|---|---|
| `UserProfile` | `suspend_user_profile(profile_id)` (US-4) | `unsuspend_user_profile(profile_id)` |
| `UserAccount` | `suspend_user_account(account_id)` (US-9) | `unsuspend_user_account(account_id)` |
| `FundraisingActivity` | `suspend_my_fundraising_activity(owner, fra_id)` (US-16) | `unsuspend_my_fundraising_activity(owner, fra_id)` |
| `FundraisingActivityCategory` | `suspend_fundraising_activity_category(fra_cat_id)` (US-38) | `unsuspend_fundraising_activity_category(fra_cat_id)` |

Each unsuspend method mirrors its suspend twin's signature, ownership scoping, and return type. Add them to the relevant class + sequence diagrams before final marking, or define a new "unsuspend" use case per actor.
