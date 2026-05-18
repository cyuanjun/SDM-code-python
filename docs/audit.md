# Audit — diagram surface (US-1 → US-43)

Transcription of the Boundary / Controller / Entity surface for every user story, taken directly from the source diagrams in [diagrams/sprint-N_diagrams/](../diagrams/). Ordered numerically US-1 → US-43 (not by sprint).

Each layer lists what the **diagram** says, then the matching `Code →` identifier + file path showing what's actually implemented (in `snake_case`). Where a `Code →` line shows a different class or method name than the diagram, that's a drift — collected at the bottom of this file.

Conventions:
- Class names are taken verbatim from the diagrams (so `category` vs `FRACatId` reflects the diagram as drawn).
- Methods are `methodName(arg: Type, …): ReturnType`. Logout pages don't have a Controller / Entity.
- Entity attribute lists are recorded once per entity and referenced as *(attrs as US-N)* on subsequent appearances.
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
- **Controller:** `SearchUserProfilesController`
  - `searchUserProfile(searchCriteria: String): List<UserProfile>`
  - Code → `SearchUserProfileController.search_user_profile(search_criteria)` in [controller/search_user_profile_controller.py](../controller/search_user_profile_controller.py) ⚠️ class name singular in code, plural in diagram
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
- **Controller:** `SearchUserAccountsController`
  - `searchUserAccount(searchCriteria: String): List<UserAccount>`
  - Code → `SearchUserAccountController.search_user_account(search_criteria)` in [controller/search_user_account_controller.py](../controller/search_user_account_controller.py) ⚠️ class name singular in code, plural in diagram
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
- **Controller:** `SearchMyFundraisingActivitiesController`
  - `searchMyFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
  - Code → `SearchMyFundraisingActivityController.search_my_fundraising_activity(owner_account_id, search_criteria)` in [controller/search_my_fundraising_activity_controller.py](../controller/search_my_fundraising_activity_controller.py) ⚠️ class name singular in code, plural in diagram
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
- **Controller:** `SearchFundraisingActivitiesController`
  - `searchFundraisingActivity(searchCriteria: String): List<FundraisingActivity>`
  - Code → `SearchFundraisingActivityController.search_fundraising_activity(search_criteria)` in [controller/search_fundraising_activity_controller.py](../controller/search_fundraising_activity_controller.py) ⚠️ class name singular in code, plural in diagram
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
  - `displaySuccess(): void`
  - Code → `ViewFundraisingActivityPage.display_remove_success()` in [boundary/view_fundraising_activity_page.py](../boundary/view_fundraising_activity_page.py) ⚠️ code uses `display_remove_success` to distinguish from US-22's `display_success`
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
- ⚠️ **Drift:** the US-28 diagram still lists the entity attribute as `category: String` rather than `FRACatId: String` — the 2026-05-18 FRACatId rename hasn't cascaded onto this diagram yet. Code follows the corrected `fra_cat_id`.

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
- ⚠️ **Drift:** same `category: String` → `FRACatId: String` cascade gap as US-28.

## US-30 — Search my completed fundraising activities *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivitiesPage`
  - `displayMatchingMyCompletedFundraisingActivity(myCompletedFRAList: List<FundraisingActivity>): void`
  - Code → `ViewMyFundraisingActivitiesPage.display_matching_my_completed_fundraising_activity(activities)` in [boundary/view_my_fundraising_activities_page.py](../boundary/view_my_fundraising_activities_page.py)
- **Controller:** `SearchMyCompletedFundraisingActivitiesController`
  - `searchMyCompletedFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
  - Code → `SearchMyCompletedFundraisingActivityController.search_my_completed_fundraising_activity(owner_account_id, search_criteria)` in [controller/search_my_completed_fundraising_activity_controller.py](../controller/search_my_completed_fundraising_activity_controller.py) ⚠️ class name singular in code, plural in diagram
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
- ⚠️ **Diagram typo:** the boundary method's parameter type reads `myCompletedFRAList: FundraisingActivity` — missing the `List<…>` wrapper. Code passes a list.

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
  - Code → `ViewFundraisingActivityCategoriesPage.display_matching_fra_category(categories)` in [boundary/view_fundraising_activity_categories_page.py](../boundary/view_fundraising_activity_categories_page.py) ⚠️ code abbreviates `fundraising_activity_category` → `fra_category`
- **Controller:** `SearchFundraisingActivityCategoriesController`
  - `searchFundraisingActivityCategory(searchCriteria: String): List<FundraisingActivityCategory>`
  - Code → `SearchFundraisingActivityCategoryController.search_fundraising_activity_category(search_criteria)` in [controller/search_fundraising_activity_category_controller.py](../controller/search_fundraising_activity_category_controller.py) ⚠️ class name singular in code, plural in diagram
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

### Pure diagram typos / gaps
- **US-28 / US-29 entity attribute** — diagram still lists `category: String`; the 2026-05-18 FRACatId rename cascaded through US-13/14/15/17/20/21/30/31 but missed these two.
- **US-31 boundary method** — `displayMyCompletedFundraisingActivities(myCompletedFRAList: FundraisingActivity)` is missing the `List<…>` wrapper on the parameter type.
<!-- US-28/29 boundary class name — resolved 2026-05-18: see "Resolved during this audit" below -->


### Code-side singular/plural class-name drifts (controller stays a pure delegator, no behaviour change)
Diagram uses the plural form of the entity in the controller class name, code uses the singular. Either rename the code or correct the diagrams — picking one direction would unify the convention.
- **US-5:** diagram `SearchUserProfilesController` → code `SearchUserProfileController`
- **US-10:** diagram `SearchUserAccountsController` → code `SearchUserAccountController`
- **US-17:** diagram `SearchMyFundraisingActivitiesController` → code `SearchMyFundraisingActivityController`
- **US-20:** diagram `SearchFundraisingActivitiesController` → code `SearchFundraisingActivityController`
- **US-30:** diagram `SearchMyCompletedFundraisingActivitiesController` → code `SearchMyCompletedFundraisingActivityController`
- **US-37:** diagram `SearchFundraisingActivityCategoriesController` → code `SearchFundraisingActivityCategoryController`

### Resolved during this audit
- ~~**US-15 signature-shape drift**~~ **Resolved 2026-05-18.** Code now takes the 6 unpacked fields exactly as the diagram defines: `update_my_fundraising_activity(owner_account_id, fra_id, title, description, target_amount, fra_cat_id, start_date, end_date)`. The previous `updated_my_fra: FundraisingActivity` parameter is gone. As a side effect, `completed` and `suspended` are no longer settable through update — `completed` is now a derived `@property` on the entity (`end_date < today`), and `suspended` is owned by US-16 / Exception A unsuspend. The `completed` column was dropped from the schema.
- ~~**US-28 / US-29 boundary placement**~~ **Resolved 2026-05-18.** Diagram puts both count-display methods on `ViewMyFundraisingActivityPage` (fundraiser-only); code had them on `ViewFundraisingActivityPage` (donee detail) with a code-only owner-gate, and the consolidated `ManageMyFundraisingActivityPage` was reading `activity.view_count` / `activity.save_count` directly off the dataclass — bypassing the diagram-defined controllers entirely. After the rewire: the per-US `ViewMyFundraisingActivityPage` renders the metrics via `ViewFundraisingActivityViewCountController` + `ViewFundraisingActivitySaveCountController`; the donee-side detail (`ViewFundraisingActivityPage` + shared `render_activity_detail` helper) no longer renders the counts at all; the consolidated `ManageMyFundraisingActivityPage` now calls the same controllers (Exception C: same call chain as the per-US page).

### Cosmetic
- **US-23 boundary method** — diagram says `displaySuccess()`, code uses `display_remove_success()` to keep it distinct from US-22's `display_success()` on the same `ViewFundraisingActivityPage`. Either the diagram should name it `displayRemoveSuccess()` or accept that one Boundary class has two `displaySuccess()` paths.
- **US-37 boundary method** — diagram says `displayMatchingFundraisingActivityCategory`; code abbreviates to `display_matching_fra_category`. Rename to spell it out (`display_matching_fundraising_activity_category`) for consistency with the other Boundary display methods.

Other naming choices that look like deviations but are deliberate consolidations (Exception C) — combined `Manage*` / `Browse*` / `My*` pages, the shared `GenerateReportPage` for daily/weekly/monthly — are catalogued in [diagram_typos.md](diagram_typos.md) under "UX consolidation".
