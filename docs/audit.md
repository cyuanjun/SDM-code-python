# Audit — diagram surface (US-1 → US-43)

Transcription of the Boundary / Controller / Entity surface for every user story, taken directly from the source diagrams in [diagrams/sprint-N_diagrams/](../diagrams/). Ordered numerically US-1 → US-43 (not by sprint).

Conventions:
- Class names are taken verbatim from the diagrams (so `category` vs `FRACatId` reflects the diagram as drawn).
- Methods are `methodName(arg: Type, …): ReturnType`. Logout pages don't have a Controller / Entity.
- Entity attribute lists are recorded once per entity and referenced as *(attrs as US-N)* on subsequent appearances.
- Diagram drifts and consolidations noted inline where applicable; full prose lives in [diagram_typos.md](diagram_typos.md) and [todo.md](todo.md).

---

## US-1 — Create user profile *(User admin)*
- **Boundary:** `CreateProfilePage`
  - `displaySuccess(profile: UserProfile): void`
- **Controller:** `CreateProfileController`
  - `createProfile(role: String, description: String): UserProfile`
- **Entity:** `UserProfile` *(profileId: String, role: String, description: String, suspended: Boolean)*
  - `createProfile(role: String, description: String): UserProfile`

## US-2 — View user profile *(User admin)*
- **Boundary:** `ViewUserProfilePage`
  - `displayUserProfile(profile: UserProfile): void`
- **Controller:** `ViewUserProfileController`
  - `viewUserProfile(profileId: String): UserProfile`
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `viewUserProfile(profileId: String): UserProfile`

## US-3 — Update user profile *(User admin)*
- **Boundary:** `UpdateUserProfilePage`
  - `displaySuccess(): void`
- **Controller:** `UpdateUserProfileController`
  - `updateUserProfile(profileId: String, role: String, description: String): Boolean`
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `updateUserProfile(profileId: String, role: String, description: String): Boolean`

## US-4 — Suspend user profile *(User admin)*
- **Boundary:** `ViewUserProfilePage`
  - `displaySuccess(): void`
- **Controller:** `SuspendUserProfileController`
  - `suspendUserProfile(profileId: String): Boolean`
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `suspendUserProfile(profileId: String): Boolean`

## US-5 — Search user profile *(User admin)*
- **Boundary:** `ViewUserProfilesPage`
  - `displayMatchingUserProfile(profileList: List<UserProfile>): void`
- **Controller:** `SearchUserProfilesController`
  - `searchUserProfile(searchCriteria: String): List<UserProfile>`
- **Entity:** `UserProfile` *(attrs as US-1)*
  - `searchUserProfile(searchCriteria: String): List<UserProfile>`

## US-6 — Create user account *(User admin)*
- **Boundary:** `CreateAccountPage`
  - `displaySuccess(account: UserAccount): void`
- **Controller:** `CreateAccountController`
  - `createAccount(email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): UserAccount`
- **Entity:** `UserAccount` *(accountId: String, email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String, suspended: Boolean)*
  - `createAccount(email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): UserAccount`

## US-7 — View user account *(User admin)*
- **Boundary:** `ViewUserAccountPage`
  - `displayUserAccount(account: UserAccount): void`
- **Controller:** `ViewUserAccountController`
  - `viewUserAccount(accountId: String): UserAccount`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `viewUserAccount(accountId: String): UserAccount`

## US-8 — Update user account *(User admin)*
- **Boundary:** `UpdateUserAccountPage`
  - `displaySuccess(): void`
- **Controller:** `UpdateUserAccountController`
  - `updateUserAccount(accountId: String, email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): Boolean`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `updateUserAccount(accountId: String, email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String): Boolean`

## US-9 — Suspend user account *(User admin)*
- **Boundary:** `ViewUserAccountPage`
  - `displaySuccess(): void`
- **Controller:** `SuspendUserAccountController`
  - `suspendUserAccount(accountId: String): Boolean`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `suspendUserAccount(accountId: String): Boolean`

## US-10 — Search user account *(User admin)*
- **Boundary:** `ViewUserAccountsPage`
  - `displayMatchingUserAccount(accountList: List<UserAccount>): void`
- **Controller:** `SearchUserAccountsController`
  - `searchUserAccount(searchCriteria: String): List<UserAccount>`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `searchUserAccount(searchCriteria: String): List<UserAccount>`

## US-11 — Log in *(User admin)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`

## US-12 — Log out *(User admin)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
- **Controller:** *(none — boundary self-call)*
- **Entity:** *(none)*

## US-13 — Create fundraising activity *(Fundraiser)*
- **Boundary:** `CreateFundraisingActivityPage`
  - `displaySuccess(fundraisingActivity: FundraisingActivity): void`
- **Controller:** `CreateFundraisingActivityController`
  - `createFundraisingActivity(title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date, ownerAccountId: String): FundraisingActivity`
- **Entity:** `FundraisingActivity` *(FRAId: String, title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date, completed: Boolean, suspended: Boolean, ownerAccountId: String, viewCount: Integer, saveCount: Integer)*
  - `createFundraisingActivity(title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date, ownerAccountId: String): FundraisingActivity`

## US-14 — View my fundraising activity *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displayMyFundraisingActivity(fundraisingActivity: FundraisingActivity): void`
- **Controller:** `ViewMyFundraisingActivityController`
  - `viewMyFundraisingActivity(ownerAccountId: String, FRAId: String): FundraisingActivity`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewMyFundraisingActivity(ownerAccountId: String, FRAId: String): FundraisingActivity`

## US-15 — Update my fundraising activity *(Fundraiser)*
- **Boundary:** `UpdateMyFundraisingActivityPage`
  - `displaySuccess(): void`
- **Controller:** `UpdateMyFundraisingActivityController`
  - `updateMyFundraisingActivity(ownerAccountId: String, FRAId: String, title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date): Boolean`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `updateMyFundraisingActivity(ownerAccountId: String, FRAId: String, title: String, description: String, targetAmount: Decimal, FRACatId: String, startDate: Date, endDate: Date): Boolean`

## US-16 — Suspend my fundraising activity *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displaySuccess(): void`
- **Controller:** `SuspendMyFundraisingActivityController`
  - `suspendMyFundraisingActivity(ownerAccountId: String, FRAId: String): Boolean`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `suspendMyFundraisingActivity(ownerAccountId: String, FRAId: String): Boolean`

## US-17 — Search my fundraising activities *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivitiesPage`
  - `displayMatchingMyFundraisingActivity(myFRAList: List<FundraisingActivity>): void`
- **Controller:** `SearchMyFundraisingActivitiesController`
  - `searchMyFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `searchMyFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`

## US-18 — Log in *(Fundraiser)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`

## US-19 — Log out *(Fundraiser)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
- **Controller:** *(none)*
- **Entity:** *(none)*

## US-20 — Search fundraising activities *(Donee)*
- **Boundary:** `ViewFundraisingActivitiesPage`
  - `displayMatchingFundraisingActivities(FRAList: List<FundraisingActivity>): void`
- **Controller:** `SearchFundraisingActivitiesController`
  - `searchFundraisingActivity(searchCriteria: String): List<FundraisingActivity>`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `searchFundraisingActivity(searchCriteria: String): List<FundraisingActivity>`

## US-21 — View fundraising activity *(Donee)*
- **Boundary:** `ViewFundraisingActivityPage`
  - `displayFundraisingActivity(fundraisingActivity: FundraisingActivity): void`
- **Controller:** `ViewFundraisingActivityController`
  - `viewFundraisingActivity(activityId: String): FundraisingActivity`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewFundraisingActivity(activityId: String): FundraisingActivity`

## US-22 — Save fundraising activity to favourites *(Donee)*
- **Boundary:** `ViewFundraisingActivityPage`
  - `displaySuccess(): void`
- **Controller:** `SaveFundraisingActivityController`
  - `saveFundraisingActivity(accountId: String, FRAId: String): Boolean`
- **Entity:** `Favourite` *(accountId: String, FRAId: String)*
  - `saveFundraisingActivity(accountId: String, FRAId: String): Boolean`

## US-23 — Remove from favourite list *(Donee)*
- **Boundary:** `ViewFundraisingActivityPage`
  - `displaySuccess(): void`
- **Controller:** `RemoveFavouriteController`
  - `removeFavourite(FRAId: String, accountId: String): Boolean`
- **Entity:** `Favourite` *(attrs as US-22)*
  - `removeFavourite(FRAId: String, accountId: String): Boolean`

## US-24 — View favourite list *(Donee)*
- **Boundary:** `ViewFavouriteListPage`
  - `displayFavouriteList(favouriteList: List<Favourite>): void`
- **Controller:** `ViewFavouriteListController`
  - `viewFavouriteList(accountId: String): List<Favourite>`
- **Entity:** `Favourite` *(attrs as US-22)*
  - `viewFavouriteList(accountId: String): List<Favourite>`

## US-25 — Search my favourites list *(Donee)*
- **Boundary:** `ViewFavouriteListPage`
  - `displayMatchingFavourites(favouriteList: List<Favourite>): void`
- **Controller:** `SearchFavouriteController`
  - `searchFavourite(accountId: String, searchCriteria: String): List<Favourite>`
- **Entity:** `Favourite` *(attrs as US-22)*
  - `searchFavourite(accountId: String, searchCriteria: String): List<Favourite>`

## US-26 — Log in *(Donee)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`

## US-27 — Log out *(Donee)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
- **Controller:** *(none)*
- **Entity:** *(none)*

## US-28 — View fundraising activity view count *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displayFundraisingActivityViewCount(viewCount: Integer): void`
- **Controller:** `ViewFundraisingActivityViewCountController`
  - `viewFundraisingActivityViewCount(FRAId: String): Integer`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewFundraisingActivityViewCount(FRAId: String): Integer`
- ⚠️ **Drift:** the US-28 diagram still lists the entity attribute as `category: String` rather than `FRACatId: String` — the 2026-05-18 FRACatId rename hasn't cascaded onto this diagram yet. Code follows the corrected `fra_cat_id`. Flag for the diagram_typos.md sweep.

## US-29 — View fundraising activity save count *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivityPage`
  - `displayFundraisingActivitySaveCount(saveCount: Integer): void`
- **Controller:** `ViewFundraisingActivitySaveCountController`
  - `viewFundraisingActivitySaveCount(FRAId: String): Integer`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewFundraisingActivitySaveCount(FRAId: String): Integer`
- ⚠️ **Drift:** same `category: String` → `FRACatId: String` cascade gap as US-28.

## US-30 — Search my completed fundraising activities *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivitiesPage`
  - `displayMatchingMyCompletedFundraisingActivity(myCompletedFRAList: List<FundraisingActivity>): void`
- **Controller:** `SearchMyCompletedFundraisingActivitiesController`
  - `searchMyCompletedFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `searchMyCompletedFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>`

## US-31 — View my completed fundraising activities *(Fundraiser)*
- **Boundary:** `ViewMyFundraisingActivitiesPage`
  - `displayMyCompletedFundraisingActivities(myCompletedFRAList: FundraisingActivity): void`
- **Controller:** `ViewMyCompletedFundraisingActivitiesController`
  - `viewMyCompletedFundraisingActivities(ownerAccountId: String): List<FundraisingActivity>`
- **Entity:** `FundraisingActivity` *(attrs as US-13)*
  - `viewMyCompletedFundraisingActivities(ownerAccountId: String): List<FundraisingActivity>`
- ⚠️ **Diagram typo:** the boundary method's parameter type reads `myCompletedFRAList: FundraisingActivity` — missing the `List<…>` wrapper. Code passes a list. Worth a typo entry.

## US-32 — Search my donation history *(Donee)*
- **Boundary:** `ViewMyDonationHistoriesPage`
  - `displayMatchingMyDonationHistories(donationList: List<Donation>): void`
- **Controller:** `SearchMyDonationHistoriesController`
  - `searchMyDonationHistory(accountId: String, searchCriteria: String): List<Donation>`
- **Entity:** `Donation` *(donationId: String, accountId: String, FRAId: String, amount: Decimal, donationDate: Date)*
  - `searchMyDonationHistory(accountId: String, searchCriteria: String): List<Donation>`

## US-33 — View my donation histories *(Donee)*
- **Boundary:** `ViewMyDonationHistoriesPage`
  - `displayMyDonationHistories(donationList: List<Donation>): void`
- **Controller:** `ViewMyDonationHistoriesController`
  - `viewMyDonationHistories(accountId: String): List<Donation>`
- **Entity:** `Donation` *(attrs as US-32)*
  - `viewMyDonationHistories(accountId: String): List<Donation>`

## US-34 — Create fundraising activity category *(Platform manager)*
- **Boundary:** `CreateFundraisingActivityCategoryPage`
  - `displaySuccess(FRACategory: FundraisingActivityCategory): void`
- **Controller:** `CreateFundraisingActivityCategoryController`
  - `createCategory(categoryName: String, description: String): FundraisingActivityCategory`
- **Entity:** `FundraisingActivityCategory` *(FRACatId: String, categoryName: String, description: String, suspended: Boolean)*
  - `createCategory(categoryName: String, description: String): FundraisingActivityCategory`

## US-35 — View fundraising activity category *(Platform manager)*
- **Boundary:** `ViewFundraisingActivityCategoryPage`
  - `displayFundraisingActivityCategory(FRACategory: FundraisingActivityCategory): void`
- **Controller:** `ViewFundraisingActivityCategoryController`
  - `viewFundraisingActivityCategory(FRACatId: String): FundraisingActivityCategory`
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `viewFundraisingActivityCategory(FRACatId: String): FundraisingActivityCategory`

## US-36 — Update fundraising activity category *(Platform manager)*
- **Boundary:** `UpdateFundraisingActivityCategoryPage`
  - `displaySuccess(): void`
- **Controller:** `UpdateFundraisingActivityCategoryController`
  - `updateFundraisingActivityCategory(FRACatId: String, categoryName: String, description: String): Boolean`
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `updateFundraisingActivityCategory(FRACatId: String, categoryName: String, description: String): Boolean`

## US-37 — Search fundraising activity categories *(Platform manager)*
- **Boundary:** `ViewFundraisingActivityCategoriesPage`
  - `displayMatchingFundraisingActivityCategory(FRACategoryList: List<FundraisingActivityCategory>): void`
- **Controller:** `SearchFundraisingActivityCategoriesController`
  - `searchFundraisingActivityCategory(searchCriteria: String): List<FundraisingActivityCategory>`
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `searchFundraisingActivityCategory(searchCriteria: String): List<FundraisingActivityCategory>`

## US-38 — Suspend fundraising activity category *(Platform manager)*
- **Boundary:** `ViewFundraisingActivityCategoryPage`
  - `displaySuccess(): void`
- **Controller:** `SuspendFundraisingActivityCategoryController`
  - `suspendFundraisingActivityCategory(FRACatId: String): Boolean`
- **Entity:** `FundraisingActivityCategory` *(attrs as US-34)*
  - `suspendFundraisingActivityCategory(FRACatId: String): Boolean`

## US-39 — Log in *(Platform manager)*
- **Boundary:** `LoginPage`
  - `displaySuccess(): void`
- **Controller:** `LoginController`
  - `login(email: String, password: String): UserAccount`
- **Entity:** `UserAccount` *(attrs as US-6)*
  - `login(email: String, password: String): UserAccount`

## US-40 — Log out *(Platform manager)*
- **Boundary:** `LogoutPage`
  - `logout(): void`
- **Controller:** *(none)*
- **Entity:** *(none)*

## US-41 — Generate daily report *(Platform manager)*
- **Boundary:** `GenerateReportPage`
  - `displayReport(report: Report): void`
- **Controller:** `GenerateDailyReportController`
  - `generateDailyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
- **Entity:** `Report` *(reportId: String, reportType: String, startDate: Date, endDate: Date, generatedAt: datetime, platformManagerId: String, totalDonationAmount: Decimal, totalDonationCount: Integer, totalActivityCount: Integer, totalFundraiserCount: Integer, totalDoneeCount: Integer)*
  - `generateDailyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`

## US-42 — Generate weekly report *(Platform manager)*
- **Boundary:** `GenerateReportPage`
  - `displayReport(report: Report): void`
- **Controller:** `GenerateWeeklyReportController`
  - `generateWeeklyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
- **Entity:** `Report` *(attrs as US-41)*
  - `generateWeeklyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`

## US-43 — Generate monthly report *(Platform manager)*
- **Boundary:** `GenerateReportPage`
  - `displayReport(report: Report): void`
- **Controller:** `GenerateMonthlyReportController`
  - `generateMonthlyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`
- **Entity:** `Report` *(attrs as US-41)*
  - `generateMonthlyReport(startDate: Date, endDate: Date, platformManagerId: String): Report`

---

## Observed drifts (worth a [diagram_typos.md](diagram_typos.md) entry)

- **US-28 / US-29 entity attribute** — diagram still lists `category: String`; the 2026-05-18 FRACatId rename cascaded through US-13/14/15/17/20/21/30/31 but missed these two.
- **US-31 boundary method** — `displayMyCompletedFundraisingActivities(myCompletedFRAList: FundraisingActivity)` is missing the `List<…>` wrapper on the parameter type.

Other naming choices that look like deviations but are deliberate consolidations (Exception C) — combined `Manage*` / `Browse*` / `My*` pages, the shared `GenerateReportPage` for daily/weekly/monthly — are catalogued in [diagram_typos.md](diagram_typos.md) under "UX consolidation".
