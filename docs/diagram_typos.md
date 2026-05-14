# Diagram typos

Consolidated list of every divergence between the source UML diagrams and the implemented code. In every case the code follows the **corrected** version; the diagram itself needs to be updated before final marking.

When a typo gets fixed in the source diagram, strike it through and add a `**resolved YYYY-MM-DD**` note rather than deleting it — keeps a record of what was fixed.

For *Exception A* additions (off-diagram methods added to power UX) and *architectural deviations* (default admin / PM / donation seeds, view-count increments, RBAC, ownership), see [docs/todo.md](todo.md).

---

## Sprint 1

Diagrams: [diagrams/sprint-1_diagrams/](../diagrams/sprint-1_diagrams/).

- ~~**[US-01.jpg](../diagrams/sprint-1_diagrams/US-01.jpg) `UserProfile.suspended: String`**~~ — **resolved 2026-05-14**. Re-exported diagram now types `suspended: Boolean`, matching every other `suspended` attribute in the project.
- ~~**[US-11.jpg](../diagrams/sprint-1_diagrams/US-11.jpg) `UserAccount.profileId: Integer`**~~ — **resolved 2026-05-14**. Re-exported diagram now types `profileId: String`, matching US-6 / US-18 / US-26 / US-39.
- **No `displayError` / `displayValidationError` on any boundary class diagram.** Every Sprint 1 boundary shows only `displaySuccess(...)`. Validation must live in the Boundary per the project rule, so an error-display method is implicit. Add `displayError(): void` (or equivalent) to every Sprint 1 boundary class diagram, or document the convention that error display is implicit.
- **[US-13.jpg](../diagrams/sprint-1_diagrams/US-13.jpg) `createFundraisingActivity` is missing `ownerAccountId: String`.** The entity declares `ownerAccountId: String` as an attribute, but the method signature doesn't accept it — so the column would never be populated. Implementation adds it as a 7th parameter; the boundary supplies it from `st.session_state["user"].account_id`. Add the parameter to the class + sequence diagrams.
- **Login failure return type not on diagrams ([US-11.jpg](../diagrams/sprint-1_diagrams/US-11.jpg), [US-18.jpg](../diagrams/sprint-1_diagrams/US-18.jpg), [US-26.jpg](../diagrams/sprint-1_diagrams/US-26.jpg), [US-39.jpg](../diagrams/sprint-1_diagrams/US-39.jpg)).** All four login diagrams type `login(email, password): UserAccount` with no failure branch. Implementation returns `None` on no-match so the boundary can show an error. Document the failure branch explicitly on the four login class diagrams.

## Sprint 2

Diagrams: [diagrams/sprint-2_diagrams/](../diagrams/sprint-2_diagrams/).

- **[US-14.jpg](../diagrams/sprint-2_diagrams/US-14.jpg) boundary method:** `displayMyFundraisingActivity(fundraisingActivity: FundraiserActivity): void`. `FundraiserActivity` is not an entity. Should be `FundraisingActivity` to match the Sprint 1 US-13 entity.
- **[US-15.jpg](../diagrams/sprint-2_diagrams/US-15.jpg) class diagram is missing `ownerAccountId` on the update method.** Class shows `updateFundraiserActivity(FRAId: String, updatedActivity: FundraiserActivity): Boolean` (2 params) but the sequence diagram shows `updateFundraiserActivity(ownerAccountId: String, FRAId: String, updatedActivity: FundraiserActivity)` (3 params). Implementation uses the 3-param sequence version so ownership is enforced. Plus the same `FundraiserActivity` → `FundraisingActivity` typo.
- **[US-20.jpg](../diagrams/sprint-2_diagrams/US-20.jpg) boundary class name:** `ViewFundraisingActivities` (no `Page` suffix). Project rule mandates the `Page` suffix on every Boundary class — implementation uses `ViewFundraisingActivitiesPage`.
- **[US-24.jpg](../diagrams/sprint-2_diagrams/US-24.jpg) return type:** `viewFavourite(accountId: String): Favourite` — returns a single Favourite, but the user story is "view all my favourites" which implies many. Should be `viewFavourites(accountId: String): List<Favourite>` (note plural method name too). Implementation uses the list version.

## Sprint 3

Diagrams: [diagrams/sprint-3_diagrams/](../diagrams/sprint-3_diagrams/).

- **[US-09.jpg](../diagrams/sprint-3_diagrams/US-09.jpg) `UserAccount.profileId: Integer`.** Same typo as the (resolved) Sprint 1 US-11 entry — re-introduced here when the diagram was redrawn. Should be `String`.
- **[US-09.jpg](../diagrams/sprint-3_diagrams/US-09.jpg) boundary class mismatch:** class diagram lists `ViewUserAccountPage`, sequence diagram shows `SuspendUserAccountPage`. Implementation reuses the Sprint 2 `ViewUserAccountPage` (same pattern as US-4 reusing `ViewUserProfilePage`): the suspend button is added to the existing view-detail page. Pick one and reconcile.
- **[US-16.jpg](../diagrams/sprint-3_diagrams/US-16.jpg) boundary class:** lists `ViewFundraisingActivityPage` (the donee's view, US-21). Should be `ViewMyFundraisingActivityPage` (fundraiser's own, US-14) since the actor is the fundraiser and the activity is theirs. Implementation extends the US-14 page.
- **[US-16.jpg](../diagrams/sprint-3_diagrams/US-16.jpg) entity attribute typo:** `suspended: Bool` (other entities use `Boolean`). Should be `Boolean` uniformly.
- **[US-25.jpg](../diagrams/sprint-3_diagrams/US-25.jpg) signature mismatch:** class shows `searchFavourite(viewMode: String, searchCriteria: String, accountId: String)`; sequence shows `searchFavourite(searchCriteria: String, accountId: String)`. The `viewMode` parameter is not exercised in the sequence — implementation uses the 2-param sequence version.
- **[US-25.jpg](../diagrams/sprint-3_diagrams/US-25.jpg) boundary class:** named `ViewFundraisingActivitiesPage` — collides with the Sprint 2 US-20 boundary. Implementation uses `SearchFavouritePage` to avoid the collision and match the user story ("search my favourites list").
- **[US-32.jpg](../diagrams/sprint-3_diagrams/US-32.jpg) `accountId: Integer` on the controller + entity.** Should be `String` to match every other account-id surface.

## Sprint 4

Diagrams: [diagrams/sprint-4_diagrams/](../diagrams/sprint-4_diagrams/).

- **[US-28.jpg](../diagrams/sprint-4_diagrams/US-28.jpg) / [US-29.jpg](../diagrams/sprint-4_diagrams/US-29.jpg) boundary class:** lists `ViewFundraisingActivityPage` (the donee's page from US-21) — but the actor is **Fundraiser** viewing their own counts. Implementation extends the donee page with owner-gated count display (renders only when `st.session_state["user"].account_id == activity.owner_account_id`). Either rename the boundary to `ViewMyFundraisingActivityPage` on the class diagram, or document the owner-gate convention.
- **[US-41.jpg](../diagrams/sprint-4_diagrams/US-41.jpg) / [US-42.jpg](../diagrams/sprint-4_diagrams/US-42.jpg) / [US-43.jpg](../diagrams/sprint-4_diagrams/US-43.jpg) `generate*Report` signatures are missing `platformManagerId`.** The entity declares `platformManagerId: String` as an attribute, but the three method signatures take only `(startDate: Date, endDate: Date): Report` — so the column would never be populated. Implementation adds `platform_manager_id` as a 3rd parameter; the boundary supplies it from `st.session_state["user"].account_id`. Add the parameter to the class + sequence diagrams.
- **[US-41.jpg](../diagrams/sprint-4_diagrams/US-41.jpg) / [US-42.jpg](../diagrams/sprint-4_diagrams/US-42.jpg) / [US-43.jpg](../diagrams/sprint-4_diagrams/US-43.jpg) shared boundary class name.** All three diagrams name the boundary class `GenerateReportPage`, but each describes a different use case. Implementation uses ONE `GenerateReportPage` with an internal radio selector for daily / weekly / monthly, routing to the three diagram-defined controllers. Either keep one shared page or rename per-story (`GenerateDailyReportPage`, etc.) — current implementation keeps the shared name.

## UX consolidation (no individual diagram is wrong — the *set* deviates)

Added 2026-05-15 after the design sketch consolidating per-US pages into resource-focused screens. Every diagram-defined per-US Boundary class **still exists** as a tested artifact, but the sidebar wires the seven combined pages below instead. Each combined page calls the same Controllers and Entities the per-US Boundaries do.

The diagrams themselves don't need to change — the per-US classes are still real, still tested, and still 1:1 with their stories. The deviation is purely in *which* Boundary classes get wired into the sidebar. Either add a "UX wireframe" diagram showing the seven combined pages alongside the existing class diagrams, or document the consolidation as a deliberate refactor of the UI surface.

| Combined page (sidebar entry) | Per-US Boundary classes it replaces in the sidebar |
|---|---|
| `ManageUserProfilePage` | `CreateProfilePage`, `ViewUserProfilePage`, `UpdateUserProfilePage`, `ViewUserProfilesPage` (and the suspend button on `ViewUserProfilePage`) |
| `ManageUserAccountPage` | `CreateAccountPage`, `ViewUserAccountPage`, `UpdateUserAccountPage`, `ViewUserAccountsPage` (and the suspend button on `ViewUserAccountPage`) |
| `ManageMyFundraisingActivityPage` | `CreateFundraisingActivityPage`, `ViewMyFundraisingActivityPage`, `UpdateMyFundraisingActivityPage`, `ViewMyFundraisingActivitiesPage`, `SearchMyCompletedActivityPage`, `ViewMyCompletedActivityPage` (All/Completed tabs) |
| `BrowseFundraisingActivityPage` | `ViewFundraisingActivityPage` (donee detail + US-22 save button), `ViewFundraisingActivitiesPage` (US-20 search) |
| `MyFavouritesPage` | `ViewFavouritePage` (with US-23 remove), `SearchFavouritePage` |
| `MyDonationsPage` | `ViewMyDonationHistoryPage`, `ViewMyDonationHistoriesPage` |
| `ManageFundraisingActivityCategoryPage` | `CreateFundraisingActivityCategoryPage`, `ViewFundraisingActivityCategoryPage`, `UpdateFundraisingActivityCategoryPage`, `ViewFundraisingActivityCategoriesPage` (suspend button on view detail) |

The 8th sidebar entry (`GenerateReportPage`) was already shared across US-41/42/43 on the diagrams; nothing changes there.
