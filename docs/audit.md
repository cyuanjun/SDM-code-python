# Audit — diagram surface (US-1 → US-43)

Transcription of the Boundary / Controller / Entity surface for every user story, taken directly from the source diagrams in [diagrams/sprint-N_diagrams/](../diagrams/). Ordered numerically US-1 → US-43 (not by sprint).

Each layer lists what the **diagram** says, then the matching `Code →` identifier + file path showing what's actually implemented (in `snake_case`). Where a `Code →` line shows a different class or method name than the diagram, that's a drift — collected at the bottom of this file.

*Last refreshed: 2026-05-18, after the US-15 unpack-fields refactor, US-22/US-23 success-message persistence fix, US-28/US-29 boundary-placement rewire, US-28/US-29 diagram re-export (`category: String` → `FRACatId: String`), US-31 diagram re-export (`myCompletedFRAList: List<FundraisingActivity>` wrapper restored), US-37 boundary method rename (`display_matching_fra_category` → `display_matching_fundraising_activity_category`), the final diagram sweep (six `Search*sController` → singular form + US-23 `displaySuccess()` → `displayRemoveSuccess()`), plus the post-audit code-side additions: `UNIQUE(phone_num)` on UserAccount (parallel to email), `FundraisingActivity.completed` flipped from derived-only `@property` to derive+store (column re-added, refreshed at app startup), generic `init_db()` schema-reconcile auto-migration covering every table, bulk seed extended to 100 favourites + 100 reports (now 100 rows in all 6 scalable tables), and `seed_tc_scenario()` adding a fully self-contained `TC - <>`-prefixed scenario (4 TC actor accounts — tc-admin/tc-fr/tc-d/tc-pm — backing 3 categories / 3 activities / 2 donations / 1 favourite / 1 report) that backs every TC in [test_cases.md](test_cases.md); each `seed_bulk_*` now reserves the trailing TC slots so TC rows occupy the highest IDs in every table (`acc_097..100`, `cat_098..100`, `fra_098..100`, `don_099..100`, `fav_100`, `rep_100`) with totals still at 100 (role split rebalanced to 2 admin / 25 fr / 69 d / 4 pm to fit TC - Admin in); `seed_bulk_favourites` rewritten to walk past pre-existing pairs. **Zero open drifts.** Diagram-vs-code identifier audit re-run after each commit: 107 / 107 verified, 412 tests pass.*

Conventions:
- Class names are taken verbatim from the diagrams (so `category` vs `FRACatId` reflects the diagram as drawn).
- Methods are `methodName(arg: Type, …): ReturnType`. Logout pages don't have a Controller / Entity.
- Entity attribute lists are recorded once per entity and referenced as *(attrs as US-N)* on subsequent appearances.
- `FundraisingActivity.completed: Boolean` is **derive+store**: the value is computed as `(end_date < today)` at INSERT/UPDATE time and persisted to the schema column, then `FundraisingActivity.refresh_completed_flags()` runs on app startup to flip rows whose `end_date` passed since the last write. US-30/31 filter `WHERE completed = 1` against the stored column. Diagram-literal — the attribute is a real boolean column, value just happens to be computed by the entity rather than user-supplied.
- Diagram drifts and consolidations noted inline where applicable; full prose lives in [diagram_typos.md](diagram_typos.md) and [todo.md](todo.md).

---

## US-1 — Create user profile *(User admin)*
- **Boundary:** `CreateProfilePage`
  - `displaySuccess(profile: UserProfile): void`
  - Code → `CreateProfilePage.display_success(profile)` in [boundary/create_profile_page.py](../boundary/create_profile_page.py)
- **Controller:** `CreateProfileController`
  - `createProfile(role: String, description: String): UserProfile`
  - Code → `CreateProfileController.create_profile(role, description)` in [controller/create_profile_controller.py](../controller/create_profile_controller.py)
- **Entity:** `UserProfile` *(profileId: String, role: String, description: String, suspended: Boolean)*
  - `createProfile(role: String, description: String): UserProfile`
  - Code → `UserProfile.create_profile(role, description)` in [entity/user_profile.py](../entity/user_profile.py)

## US-2 — View user profile *(User admin)*
- **Boundary:** `ViewUserProfilePage`
  - `displayUserProfile(profile: UserProfile): void`
  - Code → `ViewUserProfilePage.display_user_profile(profile)` in [boundary/view_user_profile_page.py](../boundary/view_user_profile_page.py)
- **Controller:** `ViewUserProfileController`
  - `viewUserProfile(profileId: String): UserProfile`
  - Code → `ViewUserProfileController.view_user_profile(profile_id)` in [controller/view_user_profile_controller.py](../controller/view_user_profile_controller.py)
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `viewUserProfile(profileId: String): UserProfile`
  - Code → `UserProfile.view_user_profile(profile_id)` in [entity/user_profile.py](../entity/user_profile.py)

## US-3 — Update user profile *(User admin)*
- **Boundary:** `UpdateUserProfilePage`
  - `displaySuccess(): void`
  - Code → `UpdateUserProfilePage.display_success()` in [boundary/update_user_profile_page.py](../boundary/update_user_profile_page.py)
- **Controller:** `UpdateUserProfileController`
  - `updateUserProfile(profileId: String, role: String, description: String): Boolean`
  - Code → `UpdateUserProfileController.update_user_profile(profile_id, role, description)` in [controller/update_user_profile_controller.py](../controller/update_user_profile_controller.py)
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `updateUserProfile(profileId: String, role: String, description: String): Boolean`
  - Code → `UserProfile.update_user_profile(profile_id, role, description)` in [entity/user_profile.py](../entity/user_profile.py)

## US-4 — Suspend user profile *(User admin)*
- **Boundary:** `ViewUserProfilePage`
  - `displaySuccess(): void`
  - Code → `ViewUserProfilePage.display_success()` in [boundary/view_user_profile_page.py](../boundary/view_user_profile_page.py)
- **Controller:** `SuspendUserProfileController`
  - `suspendUserProfile(profileId: String): Boolean`
  - Code → `SuspendUserProfileController.suspend_user_profile(profile_id)` in [controller/suspend_user_profile_controller.py](../controller/suspend_user_profile_controller.py)
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `suspendUserProfile(profileId: String): Boolean`
  - Code → `UserProfile.suspend_user_profile(profile_id)` in [entity/user_profile.py](../entity/user_profile.py)

## US-5 — Search user profile *(User admin)*
- **Boundary:** `ViewUserProfilesPage`
  - `displayMatchingUserProfile(profileList: List<UserProfile>): void`
  - Code → `ViewUserProfilesPage.display_matching_user_profile(profiles)` in [boundary/view_user_profiles_page.py](../boundary/view_user_profiles_page.py)
- **Controller:** `SearchUserProfileController`
  - `searchUserProfile(searchCriteria: String): List<UserProfile>`
  - Code → `SearchUserProfileController.search_user_profile(search_criteria)` in [controller/search_user_profile_controller.py](../controller/search_user_profile_controller.py)
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `searchUserProfile(searchCriteria: String): List<UserProfile>`
  - Code → `UserProfile.search_user_profile(search_criteria)` in [entity/user_profile.py](../entity/user_profile.py)

## US-6 — Create user account *(User admin)*
- **Boundary:** `CreateAccountPage`
  - `displaySuccess(account: UserAccount): void`
  - Code → `CreateAccountPage.display_success(account)` in [boundary/create_account_page.py](../boundary/create_account_page.py)
- **Controller:** `CreateAccountController`
  - `createAccount(email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): UserAccount`
  - Code → `CreateAccountController.create_account(email, password, name, dob, phone_num, profile_id)` in [controller/create_account_controller.py](../controller/create_account_controller.py)
- **Entity:** `UserAccount` *(accountId: String, email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String, suspended: Boolean)*
  - `createAccount(email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): UserAccount`
  - Code → `UserAccount.create_account(email, password, name, dob, phone_num, profile_id)` in [entity/user_account.py](../entity/user_account.py)

## US-7 — View user account *(User admin)*
- **Boundary:** `ViewUserAccountPage`
  - `displayUserAccount(account: UserAccount): void`
  - Code → `ViewUserAccountPage.display_user_account(account)` in [boundary/view_user_account_page.py](../boundary/view_user_account_page.py)
- **Controller:** `ViewUserAccountController`
  - `viewUserAccount(accountId: String): UserAccount`
  - Code → `ViewUserAccountController.view_user_account(account_id)` in [controller/view_user_account_controller.py](../controller/view_user_account_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `viewUserAccount(accountId: String): UserAccount`
  - Code → `UserAccount.view_user_account(account_id)` in [entity/user_account.py](../entity/user_account.py)

## US-8 — Update user account *(User admin)*
- **Boundary:** `UpdateUserAccountPage`
  - `displaySuccess(): void`
  - Code → `UpdateUserAccountPage.display_success()` in [boundary/update_user_account_page.py](../boundary/update_user_account_page.py)
- **Controller:** `UpdateUserAccountController`
  - `updateUserAccount(accountId: String, email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): Boolean`
  - Code → `UpdateUserAccountController.update_user_account(account_id, email, password, name, dob, phone_num, profile_id)` in [controller/update_user_account_controller.py](../controller/update_user_account_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `updateUserAccount(accountId: String, email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): Boolean`
  - Code → `UserAccount.update_user_account(account_id, email, password, name, dob, phone_num, profile_id)` in [entity/user_account.py](../entity/user_account.py)

## US-9 — Suspend user account *(User admin)*
- **Boundary:** `ViewUserAccountPage`
  - `displaySuccess(): void`
  - Code → `ViewUserAccountPage.display_success()` in [boundary/view_user_account_page.py](../boundary/view_user_account_page.py)
- **Controller:** `SuspendUserAccountController`
  - `suspendUserAccount(accountId: String): Boolean`
  - Code → `SuspendUserAccountController.suspend_user_account(account_id)` in [controller/suspend_user_account_controller.py](../controller/suspend_user_account_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `suspendUserAccount(accountId: String): Boolean`
  - Code → `UserAccount.suspend_user_account(account_id)` in [entity/user_account.py](../entity/user_account.py)

## US-10 — Search user account *(User admin)*
- **Boundary:** `ViewUserAccountsPage`
  - `displayMatchingUserAccount(accountList: List<UserAccount>): void`
  - Code → `ViewUserAccountsPage.display_matching_user_account(accounts)` in [boundary/view_user_accounts_page.py](../boundary/view_user_accounts_page.py)
- **Controller:** `SearchUserAccountController`
  - `searchUserAccount(searchCriteria: String): List<UserAccount>`
  - Code → `SearchUserAccountController.search_user_account(search_criteria)` in [controller/search_user_account_controller.py](../controller/search_user_account_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `searchUserAccount(searchCriteria: String): List<UserAccount>`
  - Code → `UserAccount.search_user_account(search_criteria)` in [entity/user_account.py](../entity/user_account.py)

## US-11 — Log in *(User admin)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
  - Code → `LoginPage.display_success()` in [boundary/login_page.py](../boundary/login_page.py)
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
  - Code → `LoginController.login(email, password)` in [controller/login_controller.py](../controller/login_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`
  - Code → `UserAccount.login(email, password)` in [entity/user_account.py](../entity/user_account.py)

## US-12 — Log out *(User admin)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
  - Code → `LogoutPage.logout()` in [boundary/logout_page.py](../boundary/logout_page.py)
- **Controller:** *(none — boundary self-call)*
- **Entity:** *(none)*

## US-13 — Create fundraising activity *(Fundraiser)*
- **Boundary:** `CreateFundraisingActivityPage`
  - `displaySuccess(fundraisingActivity: FundraisingActivity): void`
  - Code → `CreateFundraisingActivityPage.display_success(activity)` in [boundary/create_fundraising_activity_page.py](../boundary/create_fundraising_activity_page.py)
- **Controller:** `CreateFundraisingActivityController`
  - `createFundraisingActivity(title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date, ownerAccountId: String): FundraisingActivity`
  - Code → `CreateFundraisingActivityController.create_fundraising_activity(title, description, target_amount, fra_cat_id, start_date, end_date, owner_account_id)` in [controller/create_fundraising_activity_controller.py](../controller/create_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(FRAId: String, title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date, completed: Boolean, suspended: Boolean, ownerAccountId: String, viewCount: Integer, saveCount: Integer)*
  - `createFundraisingActivity(title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date, ownerAccountId: String): FundraisingActivity`
  - Code → `FundraisingActivity.create_fundraising_activity(title, description, target_amount, fra_cat_id, start_date, end_date, owner_account_id)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-14 — View my fundraising activity *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displayMyFundraisingActivity(fundraisingActivity: FundraisingActivity): void`
  - Code → `ViewMyFundraisingActivityPage.display_my_fundraising_activity(activity)` in [boundary/view_my_fundraising_activity_page.py](../boundary/view_my_fundraising_activity_page.py)
- **Controller:** `ViewMyFundraisingActivityController`
  - `viewMyFundraisingActivity(ownerAccountId: String, FRAId: String): FundraisingActivity`
  - Code → `ViewMyFundraisingActivityController.view_my_fundraising_activity(owner_account_id, fra_id)` in [controller/view_my_fundraising_activity_controller.py](../controller/view_my_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewMyFundraisingActivity(ownerAccountId: String, FRAId: String): FundraisingActivity`
  - Code → `FundraisingActivity.view_my_fundraising_activity(owner_account_id, fra_id)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-15 — Update my fundraising activity *(Fundraiser)*
- **Boundary:** `UpdateMyFundraisingActivityPage`
  - `displaySuccess(): void`
  - Code → `UpdateMyFundraisingActivityPage.display_success()` in [boundary/update_my_fundraising_activity_page.py](../boundary/update_my_fundraising_activity_page.py)
- **Controller:** `UpdateMyFundraisingActivityController`
  - `updateMyFundraisingActivity(ownerAccountId: String, FRAId: String, title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date): Boolean`
  - Code → `UpdateMyFundraisingActivityController.update_my_fundraising_activity(owner_account_id, fra_id, title, description, target_amount, fra_cat_id, start_date, end_date)` in [controller/update_my_fundraising_activity_controller.py](../controller/update_my_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `updateMyFundraisingActivity(ownerAccountId: String, FRAId: String, title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date): Boolean`
  - Code → `FundraisingActivity.update_my_fundraising_activity(owner_account_id, fra_id, title, description, target_amount, fra_cat_id, start_date, end_date)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-16 — Suspend my fundraising activity *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displaySuccess(): void`
  - Code → `ViewMyFundraisingActivityPage.display_success()` in [boundary/view_my_fundraising_activity_page.py](../boundary/view_my_fundraising_activity_page.py)
- **Controller:** `SuspendMyFundraisingActivityController`
  - `suspendMyFundraisingActivity(ownerAccountId: String, FRAId: String): Boolean`
  - Code → `SuspendMyFundraisingActivityController.suspend_my_fundraising_activity(owner_account_id, fra_id)` in [controller/suspend_my_fundraising_activity_controller.py](../controller/suspend_my_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `suspendMyFundraisingActivity(ownerAccountId: String, FRAId: String): Boolean`
  - Code → `FundraisingActivity.suspend_my_fundraising_activity(owner_account_id, fra_id)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-17 — Search my fundraising activities *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivitiesPage`
  - `displayMatchingMyFundraisingActivity(myFRAList: List<FundraisingActivity>): void`
  - Code → `ViewMyFundraisingActivitiesPage.display_matching_my_fundraising_activity(activities)` in [boundary/view_my_fundraising_activities_page.py](../boundary/view_my_fundraising_activities_page.py)
- **Controller:** `SearchMyFundraisingActivityController`
  - `searchMyFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
  - Code → `SearchMyFundraisingActivityController.search_my_fundraising_activity(owner_account_id, search_criteria)` in [controller/search_my_fundraising_activity_controller.py](../controller/search_my_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `searchMyFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
  - Code → `FundraisingActivity.search_my_fundraising_activity(owner_account_id, search_criteria)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-18 — Log in *(Fundraiser)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
  - Code → `LoginPage.display_success()` in [boundary/login_page.py](../boundary/login_page.py)
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
  - Code → `LoginController.login(email, password)` in [controller/login_controller.py](../controller/login_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`
  - Code → `UserAccount.login(email, password)` in [entity/user_account.py](../entity/user_account.py)

## US-19 — Log out *(Fundraiser)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
  - Code → `LogoutPage.logout()` in [boundary/logout_page.py](../boundary/logout_page.py)
- **Controller:** *(none)*
- **Entity:** *(none)*

## US-20 — Search fundraising activities *(Donee)*
- **Boundary:** `ViewFundraisingActivitiesPage`
  - `displayMatchingFundraisingActivities(FRAList: List<FundraisingActivity>): void`
  - Code → `ViewFundraisingActivitiesPage.display_matching_fundraising_activities(activities)` in [boundary/view_fundraising_activities_page.py](../boundary/view_fundraising_activities_page.py)
- **Controller:** `SearchFundraisingActivityController`
  - `searchFundraisingActivity(searchCriteria: String): List<FundraisingActivity>`
  - Code → `SearchFundraisingActivityController.search_fundraising_activity(search_criteria)` in [controller/search_fundraising_activity_controller.py](../controller/search_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `searchFundraisingActivity(searchCriteria: String): List<FundraisingActivity>`
  - Code → `FundraisingActivity.search_fundraising_activity(search_criteria)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-21 — View fundraising activity *(Donee)*
- **Boundary:** `ViewFundraisingActivityPage`
  - `displayFundraisingActivity(fundraisingActivity: FundraisingActivity): void`
  - Code → `ViewFundraisingActivityPage.display_fundraising_activity(activity)` in [boundary/view_fundraising_activity_page.py](../boundary/view_fundraising_activity_page.py)
- **Controller:** `ViewFundraisingActivityController`
  - `viewFundraisingActivity(activityId: String): FundraisingActivity`
  - Code → `ViewFundraisingActivityController.view_fundraising_activity(activity_id)` in [controller/view_fundraising_activity_controller.py](../controller/view_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewFundraisingActivity(activityId: String): FundraisingActivity`
  - Code → `FundraisingActivity.view_fundraising_activity(activity_id)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-22 — Save fundraising activity to favourites *(Donee)*
- **Boundary:** `ViewFundraisingActivityPage`
  - `displaySuccess(): void`
  - Code → `ViewFundraisingActivityPage.display_success()` in [boundary/view_fundraising_activity_page.py](../boundary/view_fundraising_activity_page.py)
- **Controller:** `SaveFundraisingActivityController`
  - `saveFundraisingActivity(accountId: String, FRAId: String): Boolean`
  - Code → `SaveFundraisingActivityController.save_fundraising_activity(account_id, fra_id)` in [controller/save_fundraising_activity_controller.py](../controller/save_fundraising_activity_controller.py)
- **Entity:** `Favourite` *(accountId: String, FRAId: String)*
  - `saveFundraisingActivity(accountId: String, FRAId: String): Boolean`
  - Code → `Favourite.save_fundraising_activity(account_id, fra_id)` in [entity/favourite.py](../entity/favourite.py)

## US-23 — Remove from favourite list *(Donee)*
- **Boundary:** `ViewFundraisingActivityPage`
  - `displayRemoveSuccess(): void`
  - Code → `ViewFundraisingActivityPage.display_remove_success()` in [boundary/view_fundraising_activity_page.py](../boundary/view_fundraising_activity_page.py)
- **Controller:** `RemoveFavouriteController`
  - `removeFavourite(FRAId: String, accountId: String): Boolean`
  - Code → `RemoveFavouriteController.remove_favourite(fra_id, account_id)` in [controller/remove_favourite_controller.py](../controller/remove_favourite_controller.py)
- **Entity:** `Favourite` *(attrs as US-22)*
  - `removeFavourite(FRAId: String, accountId: String): Boolean`
  - Code → `Favourite.remove_favourite(fra_id, account_id)` in [entity/favourite.py](../entity/favourite.py)

## US-24 — View favourite list *(Donee)*
- **Boundary:** `ViewFavouriteListPage`
  - `displayFavouriteList(favouriteList: List<Favourite>): void`
  - Code → `ViewFavouriteListPage.display_favourite_list(favourites)` in [boundary/view_favourite_list_page.py](../boundary/view_favourite_list_page.py)
- **Controller:** `ViewFavouriteListController`
  - `viewFavouriteList(accountId: String): List<Favourite>`
  - Code → `ViewFavouriteListController.view_favourite_list(account_id)` in [controller/view_favourite_list_controller.py](../controller/view_favourite_list_controller.py)
- **Entity:** `Favourite` *(attrs as US-22)*
  - `viewFavouriteList(accountId: String): List<Favourite>`
  - Code → `Favourite.view_favourite_list(account_id)` in [entity/favourite.py](../entity/favourite.py)

## US-25 — Search my favourites list *(Donee)*
- **Boundary:** `ViewFavouriteListPage`
  - `displayMatchingFavourites(favouriteList: List<Favourite>): void`
  - Code → `ViewFavouriteListPage.display_matching_favourites(favourites)` in [boundary/view_favourite_list_page.py](../boundary/view_favourite_list_page.py)
- **Controller:** `SearchFavouriteController`
  - `searchFavourite(accountId: String, searchCriteria: String): List<Favourite>`
  - Code → `SearchFavouriteController.search_favourite(account_id, search_criteria)` in [controller/search_favourite_controller.py](../controller/search_favourite_controller.py)
- **Entity:** `Favourite` *(attrs as US-22)*
  - `searchFavourite(accountId: String, searchCriteria: String): List<Favourite>`
  - Code → `Favourite.search_favourite(account_id, search_criteria)` in [entity/favourite.py](../entity/favourite.py)

## US-26 — Log in *(Donee)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
  - Code → `LoginPage.display_success()` in [boundary/login_page.py](../boundary/login_page.py)
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
  - Code → `LoginController.login(email, password)` in [controller/login_controller.py](../controller/login_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`
  - Code → `UserAccount.login(email, password)` in [entity/user_account.py](../entity/user_account.py)

## US-27 — Log out *(Donee)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
  - Code → `LogoutPage.logout()` in [boundary/logout_page.py](../boundary/logout_page.py)
- **Controller:** *(none)*
- **Entity:** *(none)*

## US-28 — View fundraising activity view count *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displayFundraisingActivityViewCount(viewCount: Integer): void`
  - Code → `ViewMyFundraisingActivityPage.display_fundraising_activity_view_count(view_count)` in [boundary/view_my_fundraising_activity_page.py](../boundary/view_my_fundraising_activity_page.py)
- **Controller:** `ViewFundraisingActivityViewCountController`
  - `viewFundraisingActivityViewCount(FRAId: String): Integer`
  - Code → `ViewFundraisingActivityViewCountController.view_fundraising_activity_view_count(fra_id)` in [controller/view_fundraising_activity_view_count_controller.py](../controller/view_fundraising_activity_view_count_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewFundraisingActivityViewCount(FRAId: String): Integer`
  - Code → `FundraisingActivity.view_fundraising_activity_view_count(fra_id)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-29 — View fundraising activity save count *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displayFundraisingActivitySaveCount(saveCount: Integer): void`
  - Code → `ViewMyFundraisingActivityPage.display_fundraising_activity_save_count(save_count)` in [boundary/view_my_fundraising_activity_page.py](../boundary/view_my_fundraising_activity_page.py)
- **Controller:** `ViewFundraisingActivitySaveCountController`
  - `viewFundraisingActivitySaveCount(FRAId: String): Integer`
  - Code → `ViewFundraisingActivitySaveCountController.view_fundraising_activity_save_count(fra_id)` in [controller/view_fundraising_activity_save_count_controller.py](../controller/view_fundraising_activity_save_count_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewFundraisingActivitySaveCount(FRAId: String): Integer`
  - Code → `FundraisingActivity.view_fundraising_activity_save_count(fra_id)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py)

## US-30 — Search my completed fundraising activities *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivitiesPage`
  - `displayMatchingMyCompletedFundraisingActivity(myCompletedFRAList: List<FundraisingActivity>): void`
  - Code → `ViewMyFundraisingActivitiesPage.display_matching_my_completed_fundraising_activity(activities)` in [boundary/view_my_fundraising_activities_page.py](../boundary/view_my_fundraising_activities_page.py)
- **Controller:** `SearchMyCompletedFundraisingActivityController`
  - `searchMyCompletedFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
  - Code → `SearchMyCompletedFundraisingActivityController.search_my_completed_fundraising_activity(owner_account_id, search_criteria)` in [controller/search_my_completed_fundraising_activity_controller.py](../controller/search_my_completed_fundraising_activity_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `searchMyCompletedFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
  - Code → `FundraisingActivity.search_my_completed_fundraising_activity(owner_account_id, search_criteria)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py) — filter is `WHERE a.end_date < ?` (today), not a stored `completed` flag (post-2026-05-18 refactor)

## US-31 — View my completed fundraising activities *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivitiesPage`
  - `displayMyCompletedFundraisingActivities(myCompletedFRAList: FundraisingActivity): void`
  - Code → `ViewMyFundraisingActivitiesPage.display_my_completed_fundraising_activities(activities)` in [boundary/view_my_fundraising_activities_page.py](../boundary/view_my_fundraising_activities_page.py)
- **Controller:** `ViewMyCompletedFundraisingActivitiesController`
  - `viewMyCompletedFundraisingActivities(ownerAccountId: String): List<FundraisingActivity>`
  - Code → `ViewMyCompletedFundraisingActivitiesController.view_my_completed_fundraising_activities(owner_account_id)` in [controller/view_my_completed_fundraising_activities_controller.py](../controller/view_my_completed_fundraising_activities_controller.py)
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewMyCompletedFundraisingActivities(ownerAccountId: String): List<FundraisingActivity>`
  - Code → `FundraisingActivity.view_my_completed_fundraising_activities(owner_account_id)` in [entity/fundraising_activity.py](../entity/fundraising_activity.py) — filter is `WHERE end_date < ?` (today), not a stored `completed` flag (post-2026-05-18 refactor)

## US-32 — Search my donation history *(Donee)*
- **Boundary:** `ViewMyDonationHistoriesPage`
  - `displayMatchingMyDonationHistories(donationList: List<Donation>): void`
  - Code → `ViewMyDonationHistoriesPage.display_matching_my_donation_histories(donations)` in [boundary/view_my_donation_histories_page.py](../boundary/view_my_donation_histories_page.py)
- **Controller:** `SearchMyDonationHistoriesController`
  - `searchMyDonationHistory(accountId: String, searchCriteria: String): List<Donation>`
  - Code → `SearchMyDonationHistoriesController.search_my_donation_history(account_id, search_criteria)` in [controller/search_my_donation_histories_controller.py](../controller/search_my_donation_histories_controller.py)
- **Entity:** `Donation` *(donationId: String, accountId: String, FRAId: String, amount: Decimal, donationDate: Date)*
  - `searchMyDonationHistory(accountId: String, searchCriteria: String): List<Donation>`
  - Code → `Donation.search_my_donation_history(account_id, search_criteria)` in [entity/donation.py](../entity/donation.py)

## US-33 — View my donation histories *(Donee)*
- **Boundary:** `ViewMyDonationHistoriesPage`
  - `displayMyDonationHistories(donationList: List<Donation>): void`
  - Code → `ViewMyDonationHistoriesPage.display_my_donation_histories(donations)` in [boundary/view_my_donation_histories_page.py](../boundary/view_my_donation_histories_page.py)
- **Controller:** `ViewMyDonationHistoriesController`
  - `viewMyDonationHistories(accountId: String): List<Donation>`
  - Code → `ViewMyDonationHistoriesController.view_my_donation_histories(account_id)` in [controller/view_my_donation_histories_controller.py](../controller/view_my_donation_histories_controller.py)
- **Entity:** `Donation` *(attrs as US-32)*
  - `viewMyDonationHistories(accountId: String): List<Donation>`
  - Code → `Donation.view_my_donation_histories(account_id)` in [entity/donation.py](../entity/donation.py)

## US-34 — Create fundraising activity category *(Platform manager)*
- **Boundary:** `CreateFundraisingActivityCategoryPage`
  - `displaySuccess(FRACategory: FundraisingActivityCategory): void`
  - Code → `CreateFundraisingActivityCategoryPage.display_success(category)` in [boundary/create_fundraising_activity_category_page.py](../boundary/create_fundraising_activity_category_page.py)
- **Controller:** `CreateFundraisingActivityCategoryController`
  - `createCategory(categoryName: String, description: String): FundraisingActivityCategory`
  - Code → `CreateFundraisingActivityCategoryController.create_category(category_name, description)` in [controller/create_fundraising_activity_category_controller.py](../controller/create_fundraising_activity_category_controller.py)
- **Entity:** `FundraisingActivityCategory` *(FRACatId: String, categoryName: String, description: String, suspended: Boolean)*
  - `createCategory(categoryName: String, description: String): FundraisingActivityCategory`
  - Code → `FundraisingActivityCategory.create_category(category_name, description)` in [entity/fundraising_activity_category.py](../entity/fundraising_activity_category.py)

## US-35 — View fundraising activity category *(Platform manager)*
- **Boundary:** `ViewFundraisingActivityCategoryPage`
  - `displayFundraisingActivityCategory(FRACategory: FundraisingActivityCategory): void`
  - Code → `ViewFundraisingActivityCategoryPage.display_fundraising_activity_category(category)` in [boundary/view_fundraising_activity_category_page.py](../boundary/view_fundraising_activity_category_page.py)
- **Controller:** `ViewFundraisingActivityCategoryController`
  - `viewFundraisingActivityCategory(FRACatId: String): FundraisingActivityCategory`
  - Code → `ViewFundraisingActivityCategoryController.view_fundraising_activity_category(fra_cat_id)` in [controller/view_fundraising_activity_category_controller.py](../controller/view_fundraising_activity_category_controller.py)
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `viewFundraisingActivityCategory(FRACatId: String): FundraisingActivityCategory`
  - Code → `FundraisingActivityCategory.view_fundraising_activity_category(fra_cat_id)` in [entity/fundraising_activity_category.py](../entity/fundraising_activity_category.py)

## US-36 — Update fundraising activity category *(Platform manager)*
- **Boundary:** `UpdateFundraisingActivityCategoryPage`
  - `displaySuccess(): void`
  - Code → `UpdateFundraisingActivityCategoryPage.display_success()` in [boundary/update_fundraising_activity_category_page.py](../boundary/update_fundraising_activity_category_page.py)
- **Controller:** `UpdateFundraisingActivityCategoryController`
  - `updateFundraisingActivityCategory(FRACatId: String, categoryName: String, description: String): Boolean`
  - Code → `UpdateFundraisingActivityCategoryController.update_fundraising_activity_category(fra_cat_id, category_name, description)` in [controller/update_fundraising_activity_category_controller.py](../controller/update_fundraising_activity_category_controller.py)
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `updateFundraisingActivityCategory(FRACatId: String, categoryName: String, description: String): Boolean`
  - Code → `FundraisingActivityCategory.update_fundraising_activity_category(fra_cat_id, category_name, description)` in [entity/fundraising_activity_category.py](../entity/fundraising_activity_category.py)

## US-37 — Search fundraising activity categories *(Platform manager)*
- **Boundary:** `ViewFundraisingActivityCategoriesPage`
  - `displayMatchingFundraisingActivityCategory(FRACategoryList: List<FundraisingActivityCategory>): void`
  - Code → `ViewFundraisingActivityCategoriesPage.display_matching_fundraising_activity_category(categories)` in [boundary/view_fundraising_activity_categories_page.py](../boundary/view_fundraising_activity_categories_page.py)
- **Controller:** `SearchFundraisingActivityCategoryController`
  - `searchFundraisingActivityCategory(searchCriteria: String): List<FundraisingActivityCategory>`
  - Code → `SearchFundraisingActivityCategoryController.search_fundraising_activity_category(search_criteria)` in [controller/search_fundraising_activity_category_controller.py](../controller/search_fundraising_activity_category_controller.py)
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `searchFundraisingActivityCategory(searchCriteria: String): List<FundraisingActivityCategory>`
  - Code → `FundraisingActivityCategory.search_fundraising_activity_category(search_criteria)` in [entity/fundraising_activity_category.py](../entity/fundraising_activity_category.py)

## US-38 — Suspend fundraising activity category *(Platform manager)*
- **Boundary:** `ViewFundraisingActivityCategoryPage`
  - `displaySuccess(): void`
  - Code → `ViewFundraisingActivityCategoryPage.display_success()` in [boundary/view_fundraising_activity_category_page.py](../boundary/view_fundraising_activity_category_page.py)
- **Controller:** `SuspendFundraisingActivityCategoryController`
  - `suspendFundraisingActivityCategory(FRACatId: String): Boolean`
  - Code → `SuspendFundraisingActivityCategoryController.suspend_fundraising_activity_category(fra_cat_id)` in [controller/suspend_fundraising_activity_category_controller.py](../controller/suspend_fundraising_activity_category_controller.py)
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `suspendFundraisingActivityCategory(FRACatId: String): Boolean`
  - Code → `FundraisingActivityCategory.suspend_fundraising_activity_category(fra_cat_id)` in [entity/fundraising_activity_category.py](../entity/fundraising_activity_category.py)

## US-39 — Log in *(Platform manager)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
  - Code → `LoginPage.display_success()` in [boundary/login_page.py](../boundary/login_page.py)
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
  - Code → `LoginController.login(email, password)` in [controller/login_controller.py](../controller/login_controller.py)
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`
  - Code → `UserAccount.login(email, password)` in [entity/user_account.py](../entity/user_account.py)

## US-40 — Log out *(Platform manager)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
  - Code → `LogoutPage.logout()` in [boundary/logout_page.py](../boundary/logout_page.py)
- **Controller:** *(none)*
- **Entity:** *(none)*

## US-41 — Generate daily report *(Platform manager)*
- **Boundary:** `GenerateReportPage`
  - `displayReport(report: Report): void`
  - Code → `GenerateReportPage.display_report(report)` in [boundary/generate_report_page.py](../boundary/generate_report_page.py)
- **Controller:** `GenerateDailyReportController`
  - `generateDailyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
  - Code → `GenerateDailyReportController.generate_daily_report(start_date, end_date, platform_manager_id)` in [controller/generate_daily_report_controller.py](../controller/generate_daily_report_controller.py)
- **Entity:** `Report` *(reportId: String, reportType: String, startDate: Date, endDate: Date, generatedAt: datetime, platformManagerId: String, totalDonationAmount: Decimal, totalDonationCount: Integer, totalActivityCount: Integer, totalFundraiserCount: Integer, totalDoneeCount: Integer)*
  - `generateDailyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
  - Code → `Report.generate_daily_report(start_date, end_date, platform_manager_id)` in [entity/report.py](../entity/report.py)

## US-42 — Generate weekly report *(Platform manager)*
- **Boundary:** `GenerateReportPage`
  - `displayReport(report: Report): void`
  - Code → `GenerateReportPage.display_report(report)` in [boundary/generate_report_page.py](../boundary/generate_report_page.py)
- **Controller:** `GenerateWeeklyReportController`
  - `generateWeeklyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
  - Code → `GenerateWeeklyReportController.generate_weekly_report(start_date, end_date, platform_manager_id)` in [controller/generate_weekly_report_controller.py](../controller/generate_weekly_report_controller.py)
- **Entity:** `Report` *(attrs as US-41)*
  - `generateWeeklyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
  - Code → `Report.generate_weekly_report(start_date, end_date, platform_manager_id)` in [entity/report.py](../entity/report.py)

## US-43 — Generate monthly report *(Platform manager)*
- **Boundary:** `GenerateReportPage`
  - `displayReport(report: Report): void`
  - Code → `GenerateReportPage.display_report(report)` in [boundary/generate_report_page.py](../boundary/generate_report_page.py)
- **Controller:** `GenerateMonthlyReportController`
  - `generateMonthlyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
  - Code → `GenerateMonthlyReportController.generate_monthly_report(start_date, end_date, platform_manager_id)` in [controller/generate_monthly_report_controller.py](../controller/generate_monthly_report_controller.py)
- **Entity:** `Report` *(attrs as US-41)*
  - `generateMonthlyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
  - Code → `Report.generate_monthly_report(start_date, end_date, platform_manager_id)` in [entity/report.py](../entity/report.py)

---

## Observed drifts (worth a [diagram_typos.md](diagram_typos.md) entry)

All drifts identified during this audit are now resolved — see "Resolved during this audit" below.

### Resolved during this audit
- ~~**`UserAccount.phone_num` was not UNIQUE**~~ **Resolved 2026-05-18.** Schema gained `phone_num TEXT NOT NULL UNIQUE` alongside the existing `UNIQUE(email)` (lecturer-approved 2026-05-15). `create_account` / `update_user_account` already trap `IntegrityError` and return `None` / `False`; create + update boundaries gained a `_which_unique_collided()` helper that re-queries the DB to surface a targeted "email / phone number / email and phone number already in use" message. Bulk seed switched to a global-unique phone generator so all 100 seeded accounts have distinct numbers.
- ~~**`FundraisingActivity.completed` was a derived-only `@property` (briefly)**~~ **Resolved 2026-05-18.** Flipped to derive+store: schema column re-added, computed at INSERT/UPDATE time, refreshed on app startup via `FundraisingActivity.refresh_completed_flags()`. US-30/31 queries flip back from `WHERE end_date < ?` to `WHERE completed = 1`. Diagram-literal interpretation of `completed: Boolean` — a real stored column, just with a deterministic computation rule rather than user input.
- ~~**`init_db()` did not auto-migrate when schema.sql gained a column**~~ **Resolved 2026-05-18.** New generic `_reconcile_columns()` parses `CREATE TABLE` blocks from `schema.sql` and ALTER TABLE ADD COLUMN's any columns missing from the existing DB. Covers every table (favourite, report, and any future schema additions auto-heal). Existing `app.db` files no longer need `rm app.db` on a column-add.
- ~~**Bulk seed didn't cover favourites or reports**~~ **Resolved 2026-05-18.** Added `seed_bulk_favourites()` (100 distinct donee × activity pairs, composite-PK-safe cycle) and `seed_bulk_reports()` (100 reports cycling daily/weekly/monthly across the 4 PMs, hitting the diagram-defined `Report.generate_*` aggregators). `seed_bulk_all()` orchestrates all six bulk helpers — every scalable table now lands at 100 rows.
- ~~**Six Search\*Controller class names: diagram plural vs code singular**~~ **Resolved 2026-05-18.** Re-exported diagrams flipped the controller class names from the `Search*sController` plural form to the singular form the code uses: US-5 `SearchUserProfileController`, US-10 `SearchUserAccountController`, US-17 `SearchMyFundraisingActivityController`, US-20 `SearchFundraisingActivityController`, US-30 `SearchMyCompletedFundraisingActivityController`, US-37 `SearchFundraisingActivityCategoryController`. No code change.
- ~~**US-23 boundary method `displaySuccess()` collided with US-22's `displaySuccess()` on the same `ViewFundraisingActivityPage` class**~~ **Resolved 2026-05-18.** Re-exported US-23 diagram now types the boundary method as `displayRemoveSuccess(): void` on both the class diagram and sequence diagram, matching the code's `display_remove_success()`. US-22 keeps `displaySuccess()` for Save. No code change.
- ~~**US-37 boundary method name abbreviation (`display_matching_fra_category`)**~~ **Resolved 2026-05-18.** Code renamed to `display_matching_fundraising_activity_category`, matching the diagram's `displayMatchingFundraisingActivityCategory` exactly (modulo snake_case). Single-method rename in [boundary/view_fundraising_activity_categories_page.py](../boundary/view_fundraising_activity_categories_page.py); no other call sites or tests referenced the abbreviated form. No behaviour change.
- ~~**US-31 boundary method param type missing the `List<…>` wrapper**~~ **Resolved 2026-05-18.** Re-exported diagram now types the param as `myCompletedFRAList: List<FundraisingActivity>` on both the class and sequence diagrams, matching the controller return type. Code was already passing a list — no code change needed.
- ~~**US-28 / US-29 entity attribute drift (`category: String` instead of `FRACatId: String`)**~~ **Resolved 2026-05-18.** Re-exported diagrams now type the entity attribute as `FRACatId: String`, matching the rest of the post-2026-05-18 FRA class diagrams (US-13/14/15/17/20/21/30/31). Code was already on `fra_cat_id` — no code change needed.
- ~~**US-15 signature-shape drift**~~ **Resolved 2026-05-18.** Code now takes the 6 unpacked fields exactly as the diagram defines: `update_my_fundraising_activity(owner_account_id, fra_id, title, description, target_amount, fra_cat_id, start_date, end_date)`. The previous `updated_my_fra: FundraisingActivity` parameter is gone. As a side effect, `completed` and `suspended` are no longer settable through update — `completed` is now a derived `@property` on the entity (`end_date < today`), and `suspended` is owned by US-16 / Exception A unsuspend. The `completed` column was dropped from the schema.
- ~~**US-28 / US-29 boundary placement**~~ **Resolved 2026-05-18.** Diagram puts both count-display methods on `ViewMyFundraisingActivityPage` (fundraiser-only); code had them on `ViewFundraisingActivityPage` (donee detail) with a code-only owner-gate, and the consolidated `ManageMyFundraisingActivityPage` was reading `activity.view_count` / `activity.save_count` directly off the dataclass — bypassing the diagram-defined controllers entirely. After the rewire: the per-US `ViewMyFundraisingActivityPage` renders the metrics via `ViewFundraisingActivityViewCountController` + `ViewFundraisingActivitySaveCountController`; the donee-side detail (`ViewFundraisingActivityPage` + shared `render_activity_detail` helper) no longer renders the counts at all; the consolidated `ManageMyFundraisingActivityPage` now calls the same controllers (Exception C: same call chain as the per-US page).

Other naming choices that look like deviations but are deliberate consolidations (Exception C) — combined `Manage*` / `Browse*` / `My*` pages, the shared `GenerateReportPage` for daily/weekly/monthly — are catalogued in [diagram_typos.md](diagram_typos.md) under "UX consolidation".
