# Implementation reference

End-to-end snapshot of the implementation for every user story in the project, plus the cross-cutting infrastructure that ties them together. This is the doc you read alongside the source diagrams when you need to know *what the code actually does* for a given US, *what assumptions it makes*, and *what's deferred*.

If a fact about wiring or naming isn't in here, the truth is in the source files this doc links to.

## Overview

CSIT314 group project — online fundraising platform (Python + Streamlit + SQLite, B-C-E architecture). All **43 user stories** across **4 sprints** implemented; **373 tests passing**; **10 sidebar entries** routed by role. Per-US detail starts at [Sprint 1](#sprint-1) below — this Overview is the bird's-eye view.

### Coverage matrix (all 43 stories)

| US | Sprint | Actor | Story | Combined page |
|---|---|---|---|---|
| US-1 | 1 | Admin | Create user profile | Manage User Profiles |
| US-2 | 2 | Admin | View user profile | Manage User Profiles |
| US-3 | 2 | Admin | Update user profile | Manage User Profiles |
| US-4 | 3 | Admin | Suspend user profile | Manage User Profiles |
| US-5 | 3 | Admin | Search user profile | Manage User Profiles |
| US-6 | 1 | Admin | Create user account | Manage User Accounts |
| US-7 | 2 | Admin | View user account | Manage User Accounts |
| US-8 | 2 | Admin | Update user account | Manage User Accounts |
| US-9 | 3 | Admin | Suspend user account | Manage User Accounts |
| US-10 | 3 | Admin | Search user account | Manage User Accounts |
| US-11 | 1 | Admin | Log in | Log In |
| US-12 | 1 | Admin | Log out | Log Out |
| US-13 | 1 | Fundraiser | Create fundraising activity | Manage My Fundraising Activities |
| US-14 | 2 | Fundraiser | View my fundraising activity | Manage My Fundraising Activities |
| US-15 | 2 | Fundraiser | Update my fundraising activity | Manage My Fundraising Activities |
| US-16 | 3 | Fundraiser | Suspend my fundraising activity | Manage My Fundraising Activities |
| US-17 | 3 | Fundraiser | Search my fundraising activities | Manage My Fundraising Activities |
| US-18 | 1 | Fundraiser | Log in | Log In |
| US-19 | 1 | Fundraiser | Log out | Log Out |
| US-20 | 2 | Donee | Search fundraising activities | Browse Fundraising Activities |
| US-21 | 1 | Donee | View fundraising activity | Browse Fundraising Activities |
| US-22 | 2 | Donee | Save fundraising activity to favourites | Browse Fundraising Activities |
| US-23 | 3 | Donee | Remove from favourite list | My Favourites |
| US-24 | 2 | Donee | View favourite list | My Favourites |
| US-25 | 3 | Donee | Search my favourites list | My Favourites |
| US-26 | 1 | Donee | Log in | Log In |
| US-27 | 1 | Donee | Log out | Log Out |
| US-28 | 4 | Fundraiser | View fundraising activity view count | Manage My Fundraising Activities |
| US-29 | 4 | Fundraiser | View fundraising activity save count | Manage My Fundraising Activities |
| US-30 | 3 | Fundraiser | Search my completed fundraising activities | Manage My Fundraising Activities |
| US-31 | 3 | Fundraiser | View my completed fundraising activities | Manage My Fundraising Activities |
| US-32 | 3 | Donee | Search my donation history | My Donations |
| US-33 | 3 | Donee | View my donation history | My Donations |
| US-34 | 4 | Platform Manager | Create fundraising activity category | Manage FRA Categories |
| US-35 | 4 | Platform Manager | View fundraising activity category | Manage FRA Categories |
| US-36 | 4 | Platform Manager | Update fundraising activity category | Manage FRA Categories |
| US-37 | 4 | Platform Manager | Search fundraising activity categories | Manage FRA Categories |
| US-38 | 4 | Platform Manager | Suspend fundraising activity category | Manage FRA Categories |
| US-39 | 1 | Platform Manager | Log in | Log In |
| US-40 | 1 | Platform Manager | Log out | Log Out |
| US-41 | 4 | Platform Manager | Generate daily report | Generate Report |
| US-42 | 4 | Platform Manager | Generate weekly report | Generate Report |
| US-43 | 4 | Platform Manager | Generate monthly report | Generate Report |

### Sidebar / role matrix

10 sidebar entries; each role sees its own actor's allow-list (driven by `PAGES_BY_ROLE` in [app.py](../app.py)). `.info (debug)` is visible to every role for development inspection (Exception B; to be hidden before final demo).

| Sidebar entry | Combined page | Visible to | Stories covered |
|---|---|---|---|
| Log In | `LoginPage` | logged-out users | US-11, 18, 26, 39 (one shared `LoginPage` / `LoginController` / `UserAccount.login`) |
| Log Out | `LogoutPage` | every signed-in role | US-12, 19, 27, 40 (one shared `LogoutPage.logout()`) |
| [Admin] Manage User Profiles | `ManageUserProfilePage` | `admin` | US-1, 2, 3, 4, 5 |
| [Admin] Manage User Accounts | `ManageUserAccountPage` | `admin` | US-6, 7, 8, 9, 10 |
| [Fundraiser] Manage My Fundraising Activities | `ManageMyFundraisingActivityPage` | `fundraiser` | US-13, 14, 15, 16, 17, 28, 29, 30, 31 |
| [Donee] Browse Fundraising Activities | `BrowseFundraisingActivityPage` | `donee` | US-20, 21, 22 |
| [Donee] My Favourites | `MyFavouritesPage` | `donee` | US-23, 24, 25 |
| [Donee] My Donations | `MyDonationsPage` | `donee` | US-32, 33 |
| [PM] Manage FRA Categories | `ManageFundraisingActivityCategoryPage` | `platform_manager` | US-34, 35, 36, 37, 38 |
| [PM] Generate Report | `GenerateReportPage` | `platform_manager` | US-41, 42, 43 (shared boundary, deferred-by-design) |
| .info (debug) | `InfoPage` | every role + logged-out | — (Exception B; hide before demo) |

### Key implementation decisions (count + index)

Numbers below are summaries — the detail tables further down hold the full text and links.

- **Exception A** — 12 off-diagram entity methods added to power UX (list dropdowns + count writes + unsuspend toggles): `UserProfile.view_all_profiles`, `UserAccount.view_all_user_accounts`, `FundraisingActivity.view_all_fundraising_activities` + `view_my_fundraising_activities` + `increment_view_count` + `increment_save_count`, `FundraisingActivityCategory.view_all_categories`, `Donation.view_my_donations`, plus four `unsuspend_*` methods.
- **Exception B** — 1 debug-only page (`.info`, [boundary/non_diagram/info_page.py](../boundary/non_diagram/info_page.py)).
- **Exception C** — 7 combined sidebar pages compose 27 per-US Boundary classes (every per-US class still exists as a tested artifact).
- **Lecturer decisions (4)** — donation seed (2026-05-15), `UNIQUE(email)` on UserAccount (2026-05-15), no `displayError` on Sprint 1 boundaries (2026-05-16), login failure return type implicit on US-11/18/26/39 (2026-05-16).
- **Deferred typos** — US-32 "My" naming; US-41/42/43 shared `GenerateReportPage`.
- **Open architectural items (1)** — plain-text passwords on `UserAccount` (deferred to a hardening sprint).
- **Resolved diagram typos** — 14 resolved across Sprints 1–4 over 2026-05-14 to 2026-05-16; 6 deferred (see above) and 2 lecturer-deferred (displayError, login failure return type). See [docs/diagram_typos.md](diagram_typos.md) for the full struck-through list.

---

## How to read this doc

- The **per-US sections** (Sprints 1 – 4) each follow the same template: actor + story sentence → diagram surface (Boundary / Controller / Entity classes + methods + attributes) → code locations with line numbers → which combined sidebar page exposes the US → tests → notes / assumptions / deferred items.
- **Diagram links** point to `diagrams/sprint-N_diagrams/US-NN.jpg`.
- **Code links** point to specific files (and line numbers where one method is the focus).
- The **bottom of the doc** has the cross-cutting context: stack, architecture rules, the three documented Exceptions, lecturer decisions, deferred typos, open architectural items, persistence, RBAC, seeds, and tests / CI.

## Project at a glance

- **Stack:** Python 3 + Streamlit + SQLite via stdlib `sqlite3` + pytest (incl. `streamlit.testing.v1.AppTest` for boundary smoke tests). CI on GitHub Actions (Python 3.11). No ORM, no linter / formatter.
- **Architecture:** B-C-E (Boundary-Controller-Entity). One Streamlit page per Boundary, one pure delegator per Controller, all DB access through an Entity.
- **Coverage:** all 43 user stories across 4 sprints implemented. **373 tests passing** locally and in CI.
- **Sidebar:** 10 entries via 7 combined `Manage*` / `Browse*` / `My*` pages + `Log In` / `Log Out` + the debug `.info` page. Each role sees its own actor's allow-list (RBAC via `PAGES_BY_ROLE` in [app.py](../app.py)).
- **Entities (7):** `UserProfile`, `UserAccount`, `FundraisingActivity`, `FundraisingActivityCategory`, `Favourite`, `Donation`, `Report`.

---

## Sprint 1

Diagrams: [diagrams/sprint-1_diagrams/](../diagrams/sprint-1_diagrams/). Stories: US-1, US-6, US-11, US-12, US-13, US-18, US-19, US-21, US-26, US-27, US-39, US-40.

### US-1 — Create user profile ([diagram](../diagrams/sprint-1_diagrams/US-01.jpg))

**Actor:** User admin — *As a user admin, I want to create a user profile so that a role exists in the system that accounts can be linked to.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `CreateProfilePage` | `displaySuccess(profile: UserProfile): void` |
| Controller | `CreateProfileController` | `createProfile(role: String, description: String): UserProfile` |
| Entity | `UserProfile (profileId: String, role: String, description: String, suspended: Boolean)` | `createProfile(role: String, description: String): UserProfile` |

**Code**
- [boundary/create_profile_page.py](../boundary/create_profile_page.py)
- [controller/create_profile_controller.py:11](../controller/create_profile_controller.py#L11)
- [entity/user_profile.py:27](../entity/user_profile.py#L27)

**Sidebar wiring:** Composed into `ManageUserProfilePage` (Exception C) under sidebar entry **[Admin] Manage User Profiles**, visible to the `admin` role.

**Tests**
- [tests/test_user_profile.py](../tests/test_user_profile.py)
- [tests/test_create_profile_controller.py](../tests/test_create_profile_controller.py)
- [tests/test_create_profile_page.py](../tests/test_create_profile_page.py)

**Notes / assumptions / deferred:** Boundary enforces non-empty `role` and `description` via `validate_profile`. The diagram's `suspended: String` was a typo — code uses `Boolean`, **resolved 2026-05-14** in the re-exported diagram. `displayError` is not on the diagram (lecturer-deferred 2026-05-16 — error display is treated as implicit). The Exception A method [`UserProfile.view_all_profiles`](../entity/user_profile.py#L130) sits alongside `create_profile` to power the dropdown on US-6's `CreateAccountPage`.

### US-6 — Create user account ([diagram](../diagrams/sprint-1_diagrams/US-06.jpg))

**Actor:** User admin — *As a user admin, I want to create a user account so that someone can log in and act under one of the four roles.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `CreateAccountPage` | `displaySuccess(account: UserAccount): void` |
| Controller | `CreateAccountController` | `createAccount(email, password, name, DOB: Date, phoneNum, profileId: String): UserAccount` |
| Entity | `UserAccount (accountId: String, email: String, password: String, name: String, DOB: Date, phoneNum: String, profileId: String, suspended: Boolean)` | `createAccount(email, password, name, DOB: Date, phoneNum, profileId: String): UserAccount` |

**Code**
- [boundary/create_account_page.py](../boundary/create_account_page.py)
- [controller/create_account_controller.py:12](../controller/create_account_controller.py#L12)
- [entity/user_account.py:42](../entity/user_account.py#L42)

**Sidebar wiring:** Composed into `ManageUserAccountPage` (Exception C) under sidebar entry **[Admin] Manage User Accounts**, visible to the `admin` role.

**Tests**
- [tests/test_user_account.py](../tests/test_user_account.py)
- [tests/test_create_account_controller.py](../tests/test_create_account_controller.py)
- [tests/test_create_account_page.py](../tests/test_create_account_page.py)

**Notes / assumptions / deferred:** Boundary validates that email contains `@`, password / name / phone are non-empty, and DOB is between 1900-01-01 and today. `profileId` is selected from a dropdown populated via the Exception A `ViewProfilesController.view_all_profiles()`. The schema-level `UNIQUE` constraint on `user_account.email` (lecturer-instructed 2026-05-15) causes `create_account` to return `None` on conflict; the diagram still types the return as `UserAccount` with no failure branch — lecturer-deferred 2026-05-16. The diagram's `profileId: Integer` was a typo — code uses `String`, **resolved 2026-05-14**.

### US-11 — Log in (User admin) ([diagram](../diagrams/sprint-1_diagrams/US-11.jpg))

**Actor:** User admin — *As a user admin, I want to log in so that I can access admin-only pages.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LoginPage` | `displaySuccess(): void` |
| Controller | `LoginController` | `login(email: String, password: String): UserAccount` |
| Entity | `UserAccount (accountId, email, password, name, DOB: Date, phoneNum, profileId: String, suspended: Boolean)` | `login(email: String, password: String): UserAccount` |

**Code**
- [boundary/login_page.py](../boundary/login_page.py) (shared across US-11/18/26/39)
- [controller/login_controller.py:15](../controller/login_controller.py#L15)
- [entity/user_account.py:142](../entity/user_account.py#L142)

**Sidebar wiring:** Sidebar entry **Log In** maps directly to `LoginPage`, visible to logged-out users only (`PAGES_BY_ROLE[None]`).

**Tests**
- [tests/test_login_controller.py](../tests/test_login_controller.py)
- [tests/test_login_page.py](../tests/test_login_page.py)
- [tests/test_user_account.py](../tests/test_user_account.py) (negative `login` cases)

**Notes / assumptions / deferred:** One `LoginPage` / `LoginController` / `UserAccount.login` triple satisfies US-11, US-18, US-26, US-39 — the four diagrams are identical apart from the actor stick figure. The diagram's `UserAccount.profileId: Integer` typo was **resolved 2026-05-14** (now `String`). The implementation returns `None` on no-match so the Boundary can call `display_error`; the missing failure branch on the diagram is **lecturer-deferred 2026-05-16** (`None`-on-no-match is the accepted implicit convention). Successful login writes the `UserAccount` to `st.session_state["user"]` and triggers `st.rerun()` so the sidebar caption refreshes immediately.

### US-12 — Log out (User admin) ([diagram](../diagrams/sprint-1_diagrams/US-12.jpg))

**Actor:** User admin — *As a user admin, I want to log out so that my session ends and the sidebar reverts to logged-out state.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LogoutPage` | `logout(): void` |
| Controller | — (none on diagram) | — |
| Entity | — (none on diagram) | — |

**Code**
- [boundary/logout_page.py:15](../boundary/logout_page.py#L15) (shared across US-12/19/27/40)

**Sidebar wiring:** Sidebar entry **Log Out** maps directly to `LogoutPage`. Visible to every signed-in role (`admin`, `fundraiser`, `donee`, `platform_manager`).

**Tests**
- [tests/test_logout_page.py](../tests/test_logout_page.py)

**Notes / assumptions / deferred:** Logout is a pure Boundary self-call per the diagram — no controller, no entity. The `logout()` method pops `"user"` from `st.session_state` then calls `st.rerun()` so the sidebar caption flips back to "Not signed in" on the very next pass. One `LogoutPage` satisfies US-12, US-19, US-27, US-40 (diagrams differ only by actor). No validation needed since there's no input. No diagram divergences logged for this story.

### US-13 — Create fundraising activity ([diagram](../diagrams/sprint-1_diagrams/US-13.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to create a fundraising activity so that donees can browse and donate to my campaign.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `CreateFundraisingActivityPage` | `displaySuccess(fundraisingActivity: FundraisingActivity): void` |
| Controller | `CreateFundraisingActivityController` | `createFundraisingActivity(title, description, targetAmount: Decimal, category, startDate: Date, endDate: Date, ownerAccountId: String): FundraisingActivity` |
| Entity | `FundraisingActivity (FRAId: String, title: String, description: String, targetAmount: Decimal, category: String, startDate: Date, endDate: Date, completed: Boolean, suspended: Boolean, ownerAccountId: String, viewCount: Integer, saveCount: Integer)` | `createFundraisingActivity(title, description, targetAmount: Decimal, category, startDate: Date, endDate: Date, ownerAccountId: String): FundraisingActivity` |

**Code**
- [boundary/create_fundraising_activity_page.py](../boundary/create_fundraising_activity_page.py)
- [controller/create_fundraising_activity_controller.py:14](../controller/create_fundraising_activity_controller.py#L14)
- [entity/fundraising_activity.py:49](../entity/fundraising_activity.py#L49)

**Sidebar wiring:** Composed into `ManageMyFundraisingActivityPage` (Exception C) under sidebar entry **[Fundraiser] Manage My Fundraising Activities**, visible to the `fundraiser` role.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py)
- [tests/test_create_fundraising_activity_controller.py](../tests/test_create_fundraising_activity_controller.py)
- [tests/test_create_fundraising_activity_page.py](../tests/test_create_fundraising_activity_page.py)

**Notes / assumptions / deferred:** Boundary requires non-empty title/description/category, a positive `Decimal` `target_amount` (parsed from text), and `start_date <= end_date`. `owner_account_id` is read from `st.session_state["user"].account_id` (the logged-in fundraiser). The original diagram omitted `ownerAccountId` from the method signature — **resolved 2026-05-16** in the re-exported diagram (now 7-param). `target_amount` is stored as TEXT to preserve Decimal precision; `view_count` and `save_count` default to 0 even though their read/increment methods land in later sprints.

### US-18 — Log in (Fundraiser) ([diagram](../diagrams/sprint-1_diagrams/US-18.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to log in so that I can manage my fundraising activities.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LoginPage` | `displaySuccess(): void` |
| Controller | `LoginController` | `login(email: String, password: String): UserAccount` |
| Entity | `UserAccount (accountId, email, password, name, DOB: Date, phoneNum, profileId: String, suspended: Boolean)` | `login(email: String, password: String): UserAccount` |

**Code**
- [boundary/login_page.py](../boundary/login_page.py) (shared with US-11/26/39)
- [controller/login_controller.py:15](../controller/login_controller.py#L15)
- [entity/user_account.py:142](../entity/user_account.py#L142)

**Sidebar wiring:** Sidebar entry **Log In**, visible only when logged out (`PAGES_BY_ROLE[None]`). After login the sidebar re-renders with the fundraiser's allow-list.

**Tests**
- [tests/test_login_controller.py](../tests/test_login_controller.py)
- [tests/test_login_page.py](../tests/test_login_page.py)
- [tests/test_user_account.py](../tests/test_user_account.py) (negative `login` cases)

**Notes / assumptions / deferred:** Shares the exact same B-C-E chain as US-11; only the actor differs on the diagram. Login failure branch (`None` return) is **lecturer-deferred 2026-05-16**. Email validation (`@` present, non-empty) and password non-empty checks live in the boundary. `st.session_state["user"]` is set on success then `st.rerun()` fires so the role-gated sidebar (built from `PAGES_BY_ROLE["fundraiser"]`) picks up the new identity on the next pass and exposes the **[Fundraiser] Manage My Fundraising Activities** entry.

### US-19 — Log out (Fundraiser) ([diagram](../diagrams/sprint-1_diagrams/US-19.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to log out so that my session ends and my fundraiser-only pages are no longer accessible.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LogoutPage` | `logout(): void` |
| Controller | — (none on diagram) | — |
| Entity | — (none on diagram) | — |

**Code**
- [boundary/logout_page.py:15](../boundary/logout_page.py#L15) (shared with US-12/27/40)

**Sidebar wiring:** Sidebar entry **Log Out**, visible to the `fundraiser` role (and every other signed-in role).

**Tests**
- [tests/test_logout_page.py](../tests/test_logout_page.py)

**Notes / assumptions / deferred:** Identical implementation to US-12 / US-27 / US-40 — the four logout diagrams differ only by actor. `LogoutPage.logout()` is a static Boundary self-call (no controller, no entity); pops `"user"` from `st.session_state` and `st.rerun()`s so the sidebar caption and allow-list flip to the logged-out view. No validation, no display_error path. No diagram divergences logged.

### US-21 — View fundraising activity ([diagram](../diagrams/sprint-1_diagrams/US-21.jpg))

**Actor:** Donee — *As a donee, I want to view a fundraising activity in detail so that I can decide whether to donate or favourite it.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFundraisingActivityPage` | `displayFundraisingActivity(fundraisingActivity: FundraisingActivity): void` |
| Controller | `ViewFundraisingActivityController` | `viewFundraisingActivity(activityId: String): FundraisingActivity` |
| Entity | `FundraisingActivity (FRAId: String, title: String, description: String, targetAmount: Decimal, category: String, startDate: Date, endDate: Date, completed: Boolean, suspended: Boolean, ownerAccountId: String, viewCount: Integer, saveCount: Integer)` | `viewFundraisingActivity(activityId: String): FundraisingActivity` |

**Code**
- [boundary/view_fundraising_activity_page.py](../boundary/view_fundraising_activity_page.py) (also hosts US-22 save button + US-28/29 count metrics)
- [controller/view_fundraising_activity_controller.py:15](../controller/view_fundraising_activity_controller.py#L15)
- [entity/fundraising_activity.py:281](../entity/fundraising_activity.py#L281)

**Sidebar wiring:** Composed into `BrowseFundraisingActivityPage` (Exception C) under sidebar entry **[Donee] Browse Fundraising Activities**, visible to the `donee` role.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py)
- [tests/test_view_fundraising_activity_controller.py](../tests/test_view_fundraising_activity_controller.py)
- [tests/test_view_fundraising_activity_page.py](../tests/test_view_fundraising_activity_page.py)

**Notes / assumptions / deferred:** Entity returns `None` for a missing row so the Boundary can call `st.error`. Exception A method [`view_all_fundraising_activities`](../entity/fundraising_activity.py#L298) populates the list view the donee picks from (logged in [docs/todo.md](todo.md)). Opening the detail also fires the Exception A [`increment_view_count`](../entity/fundraising_activity.py#L337) (per US-28). The same boundary class also wires US-22's save button and US-28/29 count metrics; counts are owner-gated so a donee never sees the fundraiser's analytics.

### US-26 — Log in (Donee) ([diagram](../diagrams/sprint-1_diagrams/US-26.jpg))

**Actor:** Donee — *As a donee, I want to log in so that I can browse activities, favourite them, and donate.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LoginPage` | `displaySuccess(): void` |
| Controller | `LoginController` | `login(email: String, password: String): UserAccount` |
| Entity | `UserAccount (accountId, email, password, name, DOB: Date, phoneNum, profileId: String, suspended: Boolean)` | `login(email: String, password: String): UserAccount` |

**Code**
- [boundary/login_page.py](../boundary/login_page.py) (shared with US-11/18/39)
- [controller/login_controller.py:15](../controller/login_controller.py#L15)
- [entity/user_account.py:142](../entity/user_account.py#L142)

**Sidebar wiring:** Sidebar entry **Log In**, visible only when logged out. After login the sidebar exposes **[Donee] Browse Fundraising Activities**, **[Donee] My Favourites**, and **[Donee] My Donations**.

**Tests**
- [tests/test_login_controller.py](../tests/test_login_controller.py)
- [tests/test_login_page.py](../tests/test_login_page.py)
- [tests/test_user_account.py](../tests/test_user_account.py) (negative `login` cases)

**Notes / assumptions / deferred:** Same shared B-C-E chain as US-11/18/39; only the actor differs in the diagram. `login` excludes `suspended = 1` rows via `WHERE … AND suspended = 0`, so a suspended donee cannot authenticate. Failure return (`None`) is **lecturer-deferred 2026-05-16**. Plain-text password storage (open architectural item in [docs/todo.md](todo.md)) is inherited from the diagram-defined `password: String` attribute; hashing is parked for a future hardening sprint.

### US-27 — Log out (Donee) ([diagram](../diagrams/sprint-1_diagrams/US-27.jpg))

**Actor:** Donee — *As a donee, I want to log out so that my browsing / favouriting / donating session ends.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LogoutPage` | `logout(): void` |
| Controller | — (none on diagram) | — |
| Entity | — (none on diagram) | — |

**Code**
- [boundary/logout_page.py:15](../boundary/logout_page.py#L15) (shared with US-12/19/40)

**Sidebar wiring:** Sidebar entry **Log Out**, visible to the `donee` role (and every other signed-in role).

**Tests**
- [tests/test_logout_page.py](../tests/test_logout_page.py)

**Notes / assumptions / deferred:** Pure Boundary self-call — same implementation as US-12/19/40 per the diagrams. `logout()` clears `st.session_state["user"]` and `st.rerun()`s; on the next pass `_current_role()` returns `None` so `PAGES_BY_ROLE[None]` is restored and the donee-only entries disappear from the sidebar. No diagram divergences logged.

### US-39 — Log in (Platform manager) ([diagram](../diagrams/sprint-1_diagrams/US-39.jpg))

**Actor:** Platform manager — *As a platform manager, I want to log in so that I can manage categories and generate platform reports.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LoginPage` | `displaySuccess(): void` |
| Controller | `LoginController` | `login(email: String, password: String): UserAccount` |
| Entity | `UserAccount (accountId, email, password, name, DOB: Date, phoneNum, profileId: String, suspended: Boolean)` | `login(email: String, password: String): UserAccount` |

**Code**
- [boundary/login_page.py](../boundary/login_page.py) (shared with US-11/18/26)
- [controller/login_controller.py:15](../controller/login_controller.py#L15)
- [entity/user_account.py:142](../entity/user_account.py#L142)

**Sidebar wiring:** Sidebar entry **Log In**, visible only when logged out. After login the sidebar exposes **[PM] Manage FRA Categories** and **[PM] Generate Report**.

**Tests**
- [tests/test_login_controller.py](../tests/test_login_controller.py)
- [tests/test_login_page.py](../tests/test_login_page.py)
- [tests/test_user_account.py](../tests/test_user_account.py) (negative `login` cases)

**Notes / assumptions / deferred:** Fourth and final reuse of the shared login B-C-E chain (US-11/18/26/39 are identical apart from the actor). Login failure return (`None`) is **lecturer-deferred 2026-05-16**. The platform manager role is identified by `profile.role == "platform_manager"` looked up via `ViewUserProfileController.view_user_profile` in `app._current_role()`; the seeded default `pm001@a.com` / `123` is provided by `seed_default_platform_manager()` to bypass the chicken-and-egg admin-creates-the-first-PM problem (bootstrap deviation, [docs/todo.md](todo.md)).

### US-40 — Log out (Platform manager) ([diagram](../diagrams/sprint-1_diagrams/US-40.jpg))

**Actor:** Platform manager — *As a platform manager, I want to log out so that my session ends and PM-only pages are inaccessible.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `LogoutPage` | `logout(): void` |
| Controller | — (none on diagram) | — |
| Entity | — (none on diagram) | — |

**Code**
- [boundary/logout_page.py:15](../boundary/logout_page.py#L15) (shared with US-12/19/27)

**Sidebar wiring:** Sidebar entry **Log Out**, visible to the `platform_manager` role (and every other signed-in role).

**Tests**
- [tests/test_logout_page.py](../tests/test_logout_page.py)

**Notes / assumptions / deferred:** Final reuse of the shared logout boundary across the four actor logout stories (US-12/19/27/40). Pure Boundary self-call — diagram defines no controller or entity. After `logout()` clears the session and re-runs, the sidebar drops the PM-only entries (**Manage FRA Categories**, **Generate Report**) and reverts to the logged-out allow-list. No diagram divergences logged.

---

## Sprint 2

Diagrams: [diagrams/sprint-2_diagrams/](../diagrams/sprint-2_diagrams/). Stories: US-2, US-3, US-7, US-8, US-14, US-15, US-20, US-22, US-24.

### US-2 — View user profile ([diagram](../diagrams/sprint-2_diagrams/US-02.jpg))

**Actor:** User admin — *As a user admin, I want to view a user profile so that I can review the profile's information.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewUserProfilePage` | `displayUserProfile(profile: UserProfile): void` |
| Controller | `ViewUserProfileController` | `viewUserProfile(profileId: String): UserProfile` |
| Entity | `UserProfile (profileId, role, description, suspended: Boolean)` | `viewUserProfile(profileId: String): UserProfile` |

**Code**
- [boundary/view_user_profile_page.py](../boundary/view_user_profile_page.py) — `ViewUserProfilePage.render` lines 24–67
- [controller/view_user_profile_controller.py:12](../controller/view_user_profile_controller.py#L12)
- [entity/user_profile.py:42](../entity/user_profile.py#L42)

**Sidebar wiring:** Composed into `ManageUserProfilePage` under sidebar entry **[Admin] Manage User Profiles**, visible to the `admin` role.

**Tests**
- [tests/test_user_profile.py](../tests/test_user_profile.py) — entity happy + missing-row negative
- [tests/test_view_user_profile_controller.py](../tests/test_view_user_profile_controller.py) — delegation + `None` mirror
- [tests/test_view_user_profile_page.py](../tests/test_view_user_profile_page.py) — `AppTest` smoke

**Notes / assumptions / deferred:** Entity returns `None` for missing rows; the page surfaces "Selected profile no longer exists." The picker is powered by the Exception A `UserProfile.view_all_profiles()` so the admin doesn't have to type `prof_NNN` (logged in [docs/todo.md](todo.md) under "Exception A"). The page is also the boundary for US-4 suspend (extra Suspend button); does not affect this view contract.

### US-3 — Update user profile ([diagram](../diagrams/sprint-2_diagrams/US-03.jpg))

**Actor:** User admin — *As a user admin, I want to update a user profile so that the latest information is shown.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `UpdateUserProfilePage` | `displaySuccess(): void` |
| Controller | `UpdateUserProfileController` | `updateUserProfile(profileId: String, updatedProfile: UserProfile): Boolean` |
| Entity | `UserProfile (profileId, role, description, suspended: Boolean)` | `updateUserProfile(profileId: String, updatedProfile: UserProfile): Boolean` |

**Code**
- [boundary/update_user_profile_page.py](../boundary/update_user_profile_page.py)
- [controller/update_user_profile_controller.py:10](../controller/update_user_profile_controller.py#L10)
- [entity/user_profile.py:62](../entity/user_profile.py#L62)

**Sidebar wiring:** Folded into `ManageUserProfilePage` (Exception C) under **[Admin] Manage User Profiles**. Admin role only.

**Tests**
- [tests/test_user_profile.py](../tests/test_user_profile.py) — entity update happy + missing-id negative (`rowcount == 0` → `False`)
- [tests/test_update_user_profile_controller.py](../tests/test_update_user_profile_controller.py) — delegation + `False` mirror
- [tests/test_update_user_profile_page.py](../tests/test_update_user_profile_page.py) — page smoke

**Notes / assumptions / deferred:** Boundary validation requires non-empty `role` and `description` (`validate_profile`) before the controller is touched. Entity-side `update` returns `False` when no row matches `profile_id`; the page maps that to `display_error()`. Picker reuses the Exception A `UserProfile.view_all_profiles()` method (already logged for US-6 in [docs/todo.md](todo.md)).

### US-7 — View user account ([diagram](../diagrams/sprint-2_diagrams/US-07.jpg))

**Actor:** User admin — *As a user admin, I want to view a user account so that I can review account details.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewUserAccountPage` | `displayUserAccount(account: UserAccount): void` |
| Controller | `ViewUserAccountController` | `viewUserAccount(accountId: String): UserAccount` |
| Entity | `UserAccount (accountId, email, password, name, DOB: Date, phoneNum, profileId, suspended: Boolean)` | `viewUserAccount(accountId: String): UserAccount` |

**Code**
- [boundary/view_user_account_page.py](../boundary/view_user_account_page.py)
- [controller/view_user_account_controller.py:14](../controller/view_user_account_controller.py#L14)
- [entity/user_account.py:74](../entity/user_account.py#L74)

**Sidebar wiring:** Folded into `ManageUserAccountPage` under **[Admin] Manage User Accounts**. Admin role only.

**Tests**
- [tests/test_user_account.py](../tests/test_user_account.py) — entity happy + missing-id `None` negative
- [tests/test_view_user_account_controller.py](../tests/test_view_user_account_controller.py) — delegation + `None` mirror; also covers `view_all_user_accounts`
- [tests/test_view_user_account_page.py](../tests/test_view_user_account_page.py), [tests/test_view_user_accounts_page.py](../tests/test_view_user_accounts_page.py) — page smoke

**Notes / assumptions / deferred:** Exception A method `UserAccount.view_all_user_accounts()` hangs off the same controller ([entity/user_account.py:86](../entity/user_account.py#L86), [controller/view_user_account_controller.py:18](../controller/view_user_account_controller.py#L18)) so the admin can pick from a list — logged in [docs/todo.md](todo.md). This page also hosts the US-9 Suspend button (Sprint 3); does not change the US-7 surface. Plain-text storage is still flagged under "Open architectural items" in [docs/todo.md](todo.md).

### US-8 — Update user account ([diagram](../diagrams/sprint-2_diagrams/US-08.jpg))

**Actor:** User admin — *As a user admin, I want to update a user account so that account information remains up to date.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `UpdateUserAccountPage` | `displaySuccess(): void` |
| Controller | `UpdateUserAccountController` | `updateUserAccount(accountId: String, updatedAccount: UserAccount): Boolean` |
| Entity | `UserAccount (accountId, email, password, name, DOB, phoneNum, profileId, suspended: Boolean)` | `updateUserAccount(accountId: String, updatedAccount: UserAccount): Boolean` |

**Code**
- [boundary/update_user_account_page.py](../boundary/update_user_account_page.py)
- [controller/update_user_account_controller.py:10](../controller/update_user_account_controller.py#L10)
- [entity/user_account.py:97](../entity/user_account.py#L97)

**Sidebar wiring:** Folded into `ManageUserAccountPage` under **[Admin] Manage User Accounts**. Admin role only.

**Tests**
- [tests/test_user_account.py](../tests/test_user_account.py) — happy + missing-id `False` + email-conflict `False` (UNIQUE constraint)
- [tests/test_update_user_account_controller.py](../tests/test_update_user_account_controller.py) — delegation + `False` mirror
- [tests/test_update_user_account_page.py](../tests/test_update_user_account_page.py) — page smoke

**Notes / assumptions / deferred:** Boundary validation enforces `@` in email + non-empty `email/password/name/phone_num`. The entity catches `sqlite3.IntegrityError` from the `UNIQUE(email)` constraint (lecturer instruction 2026-05-15, see [docs/todo.md](todo.md) "Resolved") and returns `False`, which the page maps to "email may already be in use." The picker reuses Exception A `view_all_user_accounts`. Profile dropdown is populated by `ViewProfilesController.view_all_profiles` (Exception A from US-6).

### US-14 — View my fundraising activity ([diagram](../diagrams/sprint-2_diagrams/US-14.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to view details of a specific fundraising activity so that I can review its information.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyFundraisingActivityPage` | `displayMyFundraisingActivity(fundraisingActivity: FundraisingActivity): void` |
| Controller | `ViewMyFundraisingActivityController` | `viewMyFundraisingActivity(ownerAccountId: String, FRAId: String): FundraisingActivity` |
| Entity | `FundraisingActivity (FRAId, title, description, targetAmount: Decimal, category, startDate: Date, endDate: Date, completed: Boolean, suspended: Boolean, ownerAccountId, viewCount: Integer, saveCount: Integer)` | `viewMyFundraisingActivity(ownerAccountId: String, FRAId: String): FundraisingActivity` |

**Code**
- [boundary/view_my_fundraising_activity_page.py](../boundary/view_my_fundraising_activity_page.py)
- [controller/view_my_fundraising_activity_controller.py:14](../controller/view_my_fundraising_activity_controller.py#L14)
- [entity/fundraising_activity.py:92](../entity/fundraising_activity.py#L92)

**Sidebar wiring:** Folded into `ManageMyFundraisingActivityPage` under **[Fundraiser] Manage My Fundraising Activities**. Fundraiser role only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — owner-match happy + missing-id `None` + cross-owner `None` negative
- [tests/test_view_my_fundraising_activity_controller.py](../tests/test_view_my_fundraising_activity_controller.py) — delegation + `None` mirror; also covers `view_my_fundraising_activities`
- [tests/test_view_my_fundraising_activity_page.py](../tests/test_view_my_fundraising_activity_page.py) — page smoke

**Notes / assumptions / deferred:** Ownership is enforced at the entity (`WHERE fra_id = ? AND owner_account_id = ?`) so cross-owner access yields `None`. `owner_account_id` is sourced from `st.session_state["user"].account_id` — the page bails with a warning if not logged in. Exception A method `FundraisingActivity.view_my_fundraising_activities(owner_account_id)` powers the picker. Same page is the US-16 suspend boundary (Sprint 3). The original diagram typed the parameter as `FundraiserActivity`; **resolved 2026-05-16** per [docs/diagram_typos.md](diagram_typos.md).

### US-15 — Update my fundraising activity ([diagram](../diagrams/sprint-2_diagrams/US-15.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to update my fundraising activity so that its information stays current.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `UpdateMyFundraisingActivityPage` | `displaySuccess(): void` |
| Controller | `UpdateMyFundraisingActivityController` | `updateMyFundraisingActivity(ownerAccountId: String, FRAId: String, updatedMyFRA: FundraisingActivity): Boolean` |
| Entity | `FundraisingActivity (attrs as US-14)` | `updateMyFundraisingActivity(ownerAccountId: String, FRAId: String, updatedMyFRA: FundraisingActivity): Boolean` |

**Code**
- [boundary/update_my_fundraising_activity_page.py](../boundary/update_my_fundraising_activity_page.py)
- [controller/update_my_fundraising_activity_controller.py:13](../controller/update_my_fundraising_activity_controller.py#L13)
- [entity/fundraising_activity.py:244](../entity/fundraising_activity.py#L244)

**Sidebar wiring:** Folded into `ManageMyFundraisingActivityPage`. Fundraiser role only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — owner-match happy + cross-owner `False` + missing-id `False`
- [tests/test_update_my_fundraising_activity_controller.py](../tests/test_update_my_fundraising_activity_controller.py) — delegation + `False` mirror
- [tests/test_update_my_fundraising_activity_page.py](../tests/test_update_my_fundraising_activity_page.py) — page smoke

**Notes / assumptions / deferred:** Boundary validation requires non-empty `title/description/category`, a positive `Decimal` target, and `start_date <= end_date`. Entity refuses cross-owner writes via `WHERE fra_id = ? AND owner_account_id = ?` → `rowcount == 0` → `False`. Diagram originally omitted `ownerAccountId` from the class signature and used `FundraiserActivity` type names; re-exported 2026-05-16 fixed the 3-param signature + the type. Further refined 2026-05-17: method renamed `updateFundraisingActivity` → `updateMyFundraisingActivity` and parameter to `updatedMyFRA` for consistency with the per-US class names and to mark this as an owner-scoped operation — code uses `update_my_fundraising_activity` / `updated_my_fra` (per [docs/diagram_typos.md](diagram_typos.md)).

### US-20 — Search fundraising activities ([diagram](../diagrams/sprint-2_diagrams/US-20.jpg))

**Actor:** Donee — *As a donee, I want to search fundraising activities so that I can find causes relevant to my interests.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFundraisingActivitiesPage` | `displayMatchingFundraisingActivities(FRAList: List<FundraisingActivity>): void` |
| Controller | `SearchFundraisingActivityController` | `searchFundraisingActivity(searchCriteria: String): List<FundraisingActivity>` |
| Entity | `FundraisingActivity (attrs as US-14)` | `searchFundraisingActivity(searchCriteria: String): List<FundraisingActivity>` |

**Code**
- [boundary/view_fundraising_activities_page.py](../boundary/view_fundraising_activities_page.py)
- [controller/search_fundraising_activity_controller.py:10](../controller/search_fundraising_activity_controller.py#L10)
- [entity/fundraising_activity.py:223](../entity/fundraising_activity.py#L223)

**Sidebar wiring:** Folded into `BrowseFundraisingActivityPage` under **[Donee] Browse Fundraising Activities**. Donee role only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — substring match across title/description/category + no-match empty list
- [tests/test_search_fundraising_activity_controller.py](../tests/test_search_fundraising_activity_controller.py) — delegation + empty-list mirror
- [tests/test_view_fundraising_activities_page.py](../tests/test_view_fundraising_activities_page.py) — page smoke

**Notes / assumptions / deferred:** Boundary requires a non-empty search term (`validate_criteria`); empty input never reaches the controller. Entity does a case-insensitive `LIKE` on `title`, `description`, and `category` — no filter on `completed` or `suspended`. Original diagram named the boundary `ViewFundraisingActivities` (no `Page` suffix); **resolved 2026-05-16** to match the implementation (see [docs/diagram_typos.md](diagram_typos.md)).

### US-22 — Save fundraising activity to favourites ([diagram](../diagrams/sprint-2_diagrams/US-22.jpg))

**Actor:** Donee — *As a donee, I want to save a fundraising activity to my favourite list so that I can revisit it later.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFundraisingActivityPage` | `displaySuccess(): void` |
| Controller | `SaveFundraisingActivityController` | `saveFundraisingActivity(accountId: String, FRAId: String): Boolean` |
| Entity | `Favourite (accountId, FRAId)` | `saveFundraisingActivity(accountId: String, FRAId: String): Boolean` |

**Code**
- [boundary/view_fundraising_activity_page.py](../boundary/view_fundraising_activity_page.py) — Save button at lines 105–117
- [controller/save_fundraising_activity_controller.py:11](../controller/save_fundraising_activity_controller.py#L11)
- [entity/favourite.py:27](../entity/favourite.py#L27)

**Sidebar wiring:** Shares the donee detail page (`ViewFundraisingActivityPage`) wired through `BrowseFundraisingActivityPage` under **[Donee] Browse Fundraising Activities**. Donee role only.

**Tests**
- [tests/test_favourite.py](../tests/test_favourite.py) — save happy + duplicate `False` + FK violation raises
- [tests/test_save_fundraising_activity_controller.py](../tests/test_save_fundraising_activity_controller.py) — delegation + `False` mirror
- [tests/test_view_fundraising_activity_page.py](../tests/test_view_fundraising_activity_page.py) — page smoke

**Notes / assumptions / deferred:** Shares its boundary class with US-21 (donee detail view) and US-28/29 (owner-gated counts). The entity pre-checks for the `(account_id, fra_id)` pair to distinguish a genuine duplicate (`False`) from an FK violation on a missing account/activity (raises `IntegrityError`). On success the entity also fires Exception A `FundraisingActivity.increment_save_count(fra_id, +1)` so US-29 counts stay current.

### US-24 — View favourite list ([diagram](../diagrams/sprint-2_diagrams/US-24.jpg))

**Actor:** Donee — *As a donee, I want to view my favourites list so that I can review all of my favourite fundraising activities.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFavouriteListPage` | `displayFavouriteList(favouriteList: List<Favourite>): void` |
| Controller | `ViewFavouriteListController` | `viewFavouriteList(accountId: String): List<Favourite>` |
| Entity | `Favourite (accountId, FRAId)` | `viewFavouriteList(accountId: String): List<Favourite>` |

**Code**
- [boundary/view_favourite_list_page.py](../boundary/view_favourite_list_page.py)
- [controller/view_favourite_list_controller.py:12](../controller/view_favourite_list_controller.py#L12)
- [entity/favourite.py:111](../entity/favourite.py#L111)

**Sidebar wiring:** Folded into `MyFavouritesPage` under **[Donee] My Favourites**. Donee role only.

**Tests**
- [tests/test_favourite.py](../tests/test_favourite.py) — list happy + empty-list for unknown account negative
- [tests/test_view_favourite_list_controller.py](../tests/test_view_favourite_list_controller.py) — delegation + empty-list mirror
- [tests/test_view_favourite_list_page.py](../tests/test_view_favourite_list_page.py) — page smoke

**Notes / assumptions / deferred:** The original diagram named the boundary `ViewFavouritePage`, controller `ViewFavouriteController`, and entity method `viewFavourite(accountId): Favourite` (singular). **Resolved 2026-05-16** by re-exporting with the `List` suffix throughout — code was renamed to match. Same page is reused for US-23 remove-favourite (Sprint 3); US-23's re-exported diagram 2026-05-17 now also names the boundary `ViewFavouriteListPage`, so the previously-deferred mismatch is resolved.

---

## Sprint 3

Diagrams: [diagrams/sprint-3_diagrams/](../diagrams/sprint-3_diagrams/). Stories: US-4, US-5, US-9, US-10, US-16, US-17, US-23, US-25, US-30, US-31, US-32, US-33.

### US-4 — Suspend user profile ([diagram](../diagrams/sprint-3_diagrams/US-04.jpg))

**Actor:** User admin — *As a user admin, I want to suspend a user profile so that the profile is no longer in the system.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewUserProfilePage` | `displaySuccess(): void` |
| Controller | `SuspendUserProfileController` | `suspendUserProfile(profileId: String): Boolean` |
| Entity | `UserProfile (profileId, role, description, suspended: Boolean)` | `suspendUserProfile(profileId: String): Boolean` |

**Code**
- [boundary/view_user_profile_page.py:23](../boundary/view_user_profile_page.py#L23) (shared with US-2)
- [controller/suspend_user_profile_controller.py:10](../controller/suspend_user_profile_controller.py#L10)
- [entity/user_profile.py:83](../entity/user_profile.py#L83) — sets `suspended = 1` and returns `cursor.rowcount > 0`

**Sidebar wiring:** Surfaced via `ManageUserProfilePage` under **[Admin] Manage User Profiles**; admin only.

**Tests**
- [tests/test_user_profile.py](../tests/test_user_profile.py) — happy + missing-id negative
- [tests/test_suspend_user_profile_controller.py](../tests/test_suspend_user_profile_controller.py) — delegation happy + `False` mirror
- [tests/test_view_user_profile_page.py](../tests/test_view_user_profile_page.py) — page smoke

**Notes / assumptions / deferred:** The Boundary doubles as the entry for the *unsuspend* toggle on the combined `ManageUserProfilePage` — Exception A method `UserProfile.unsuspend_user_profile` ([entity/user_profile.py:95](../entity/user_profile.py#L95)) plus `UnsuspendUserProfileController` provide the mirror; logged in [docs/diagram_typos.md](diagram_typos.md). Reuses the US-2 boundary as the suspend-action page (same pattern as US-9 reusing `ViewUserAccountPage`).

### US-5 — Search user profile ([diagram](../diagrams/sprint-3_diagrams/US-05.jpg))

**Actor:** User admin — *As a user admin, I want to search for user profiles so that I can quickly locate a specific user profile.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewUserProfilesPage` | `displayMatchingUserProfile(profileList: List<UserProfile>): void` |
| Controller | `SearchUserProfileController` | `searchUserProfile(searchCriteria: String): List<UserProfile>` |
| Entity | `UserProfile (profileId, role, description, suspended: Boolean)` | `searchUserProfile(searchCriteria: String): List<UserProfile>` |

**Code**
- [boundary/view_user_profiles_page.py:17](../boundary/view_user_profiles_page.py#L17)
- [controller/search_user_profile_controller.py:10](../controller/search_user_profile_controller.py#L10)
- [entity/user_profile.py:107](../entity/user_profile.py#L107) — case-insensitive `LIKE %criteria%` against `role` + `description`

**Sidebar wiring:** Reached via `ManageUserProfilePage` (search box at top); admin only.

**Tests**
- [tests/test_user_profile.py](../tests/test_user_profile.py) — match + empty-result negative
- [tests/test_search_user_profile_controller.py](../tests/test_search_user_profile_controller.py) — delegation + empty-list mirror
- [tests/test_view_user_profiles_page.py](../tests/test_view_user_profiles_page.py) — page smoke

**Notes / assumptions / deferred:** Empty `search_criteria` matches everything (becomes `%%`) — `ManageUserProfilePage` uses this as a "list all" fallback when the admin clears the search input. Cleanest US in Sprint 3 — no deferred items.

### US-9 — Suspend user account ([diagram](../diagrams/sprint-3_diagrams/US-09.jpg))

**Actor:** User admin — *As a user admin, I want to suspend a user account so that they can no longer log in to the system.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewUserAccountPage` | `displaySuccess(): void` |
| Controller | `SuspendUserAccountController` | `suspendUserAccount(accountId: String): Boolean` |
| Entity | `UserAccount (accountId, email, password, name, DOB, phoneNum, profileId, suspended: Boolean)` | `suspendUserAccount(accountId: String): Boolean` |

**Code**
- [boundary/view_user_account_page.py:25](../boundary/view_user_account_page.py#L25) (shared with US-7)
- [controller/suspend_user_account_controller.py:10](../controller/suspend_user_account_controller.py#L10)
- [entity/user_account.py:154](../entity/user_account.py#L154) — `UserAccount.login` ([:142](../entity/user_account.py#L142)) filters `suspended = 0`, so suspending immediately bars login

**Sidebar wiring:** Surfaced via `ManageUserAccountPage` under **[Admin] Manage User Accounts**; admin only.

**Tests**
- [tests/test_user_account.py](../tests/test_user_account.py) — suspend happy + missing-id negative + login-after-suspend
- [tests/test_suspend_user_account_controller.py](../tests/test_suspend_user_account_controller.py) — delegation + `False` mirror
- [tests/test_view_user_account_page.py](../tests/test_view_user_account_page.py) — page smoke

**Notes / assumptions / deferred:** Two diagram typos on US-09 (`profileId: Integer`; class/sequence boundary mismatch) were both **resolved 2026-05-16** — code already matched. Mirror `UserAccount.unsuspend_user_account` ([entity/user_account.py:166](../entity/user_account.py#L166)) is an Exception A toggle for the consolidated page.

### US-10 — Search user account ([diagram](../diagrams/sprint-3_diagrams/US-10.jpg))

**Actor:** User admin — *As a user admin, I want to search for a user account so that I can quickly locate a specific account.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewUserAccountsPage` | `displayMatchingUserAccount(accountList: List<UserAccount>): void` |
| Controller | `SearchUserAccountController` | `searchUserAccount(searchCriteria: String): List<UserAccount>` |
| Entity | `UserAccount (attrs as US-9)` | `searchUserAccount(searchCriteria: String): List<UserAccount>` |

**Code**
- [boundary/view_user_accounts_page.py:15](../boundary/view_user_accounts_page.py#L15)
- [controller/search_user_account_controller.py:10](../controller/search_user_account_controller.py#L10)
- [entity/user_account.py:178](../entity/user_account.py#L178) — case-insensitive `LIKE` against `email` + `name`

**Sidebar wiring:** Reached via `ManageUserAccountPage` (search box at top); admin only.

**Tests**
- [tests/test_user_account.py](../tests/test_user_account.py) — match + no-match negative
- [tests/test_search_user_account_controller.py](../tests/test_search_user_account_controller.py) — delegation + empty-list mirror
- [tests/test_view_user_accounts_page.py](../tests/test_view_user_accounts_page.py) — page smoke

**Notes / assumptions / deferred:** Empty input behaves as "list all" so the combined page can lean on a single search box. Suspended accounts are still returned (the admin needs to see them to unsuspend) — only `login` filters on `suspended`. No deferred items.

### US-16 — Suspend my fundraising activity ([diagram](../diagrams/sprint-3_diagrams/US-16.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to suspend donations for my fundraising activity so that I can stop receiving contributions.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyFundraisingActivityPage` | `displaySuccess(): void` |
| Controller | `SuspendMyFundraisingActivityController` | `suspendMyFundraisingActivity(ownerAccountId: String, FRAId: String): Boolean` |
| Entity | `FundraisingActivity (attrs as US-14)` | `suspendMyFundraisingActivity(ownerAccountId: String, FRAId: String): Boolean` |

**Code**
- [boundary/view_my_fundraising_activity_page.py:26](../boundary/view_my_fundraising_activity_page.py#L26) (shared with US-14)
- [controller/suspend_my_fundraising_activity_controller.py:10](../controller/suspend_my_fundraising_activity_controller.py#L10)
- [entity/fundraising_activity.py:130](../entity/fundraising_activity.py#L130) — `UPDATE … WHERE fra_id = ? AND owner_account_id = ?` so cross-owner writes return `False`

**Sidebar wiring:** Surfaced via `ManageMyFundraisingActivityPage` under **[Fundraiser] Manage My Fundraising Activities**; fundraiser only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — own-row happy + missing + cross-owner negatives
- [tests/test_suspend_my_fundraising_activity_controller.py](../tests/test_suspend_my_fundraising_activity_controller.py) — delegation + `False` mirror
- [tests/test_view_my_fundraising_activity_page.py](../tests/test_view_my_fundraising_activity_page.py) — page smoke

**Notes / assumptions / deferred:** Two source-diagram typos (boundary previously `ViewFundraisingActivityPage`; `suspended: Bool`) **both resolved 2026-05-16**. Mirror `FundraisingActivity.unsuspend_my_fundraising_activity` ([entity/fundraising_activity.py:146](../entity/fundraising_activity.py#L146)) is an Exception A toggle, same owner-scoped `WHERE` clause.

### US-17 — Search my fundraising activities ([diagram](../diagrams/sprint-3_diagrams/US-17.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to search my fundraising activities so that I can quickly locate a specific campaign.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyFundraisingActivitiesPage` | `displayMatchingMyFundraisingActivity(myFRAList: List<FundraisingActivity>): void` |
| Controller | `SearchMyFundraisingActivityController` | `searchMyFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>` |
| Entity | `FundraisingActivity (attrs as US-14)` | `searchMyFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>` |

**Code**
- [boundary/view_my_fundraising_activities_page.py:20](../boundary/view_my_fundraising_activities_page.py#L20)
- [controller/search_my_fundraising_activity_controller.py:10](../controller/search_my_fundraising_activity_controller.py#L10)
- [entity/fundraising_activity.py:162](../entity/fundraising_activity.py#L162) — owner-scoped `LIKE` against `title / description / category`

**Sidebar wiring:** Surfaced via `ManageMyFundraisingActivityPage` (the "All" tab's search box); fundraiser only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — match + cross-owner-isolation negative + empty-result negative
- [tests/test_search_my_fundraising_activity_controller.py](../tests/test_search_my_fundraising_activity_controller.py) — delegation + empty-list mirror
- [tests/test_view_my_fundraising_activities_page.py](../tests/test_view_my_fundraising_activities_page.py) — page smoke

**Notes / assumptions / deferred:** Empty `searchCriteria` returns every activity owned by `ownerAccountId`. Owner sourced from `st.session_state["user"].account_id` — the Boundary never asks for it. Diagram `Bool` regression on FundraisingActivity attributes was **resolved 2026-05-16**. No outstanding deferred items.

### US-23 — Remove from favourite list ([diagram](../diagrams/sprint-3_diagrams/US-23.jpg))

**Actor:** Donee — *As a donee, I want to remove a fundraising activity from my favourites list so that I can keep my favourites list relevant.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFavouriteListPage` | `displaySuccess(): void` |
| Controller | `RemoveFavouriteController` | `removeFavourite(FRAId: String, accountId: String): Boolean` |
| Entity | `Favourite (FRAId, accountId)` | `removeFavourite(FRAId: String, accountId: String): Boolean` |

**Code**
- [boundary/view_favourite_list_page.py:17](../boundary/view_favourite_list_page.py#L17) (shared with US-24)
- [controller/remove_favourite_controller.py:10](../controller/remove_favourite_controller.py#L10)
- [entity/favourite.py:55](../entity/favourite.py#L55) — `DELETE … WHERE fra_id = ? AND account_id = ?`, then calls `FundraisingActivity.increment_save_count(fra_id, -1)` on success

**Sidebar wiring:** Surfaced via `MyFavouritesPage` under **[Donee] My Favourites**; donee only.

**Tests**
- [tests/test_favourite.py](../tests/test_favourite.py) — happy delete + non-existent-pair negative + cross-account isolation
- [tests/test_remove_favourite_controller.py](../tests/test_remove_favourite_controller.py) — delegation + `False` mirror
- [tests/test_view_favourite_list_page.py](../tests/test_view_favourite_list_page.py) — page smoke

**Notes / assumptions / deferred:** Re-exported diagram 2026-05-17 names the boundary `ViewFavouriteListPage` (class + sequence consistent) and fixes the user-story wording ("suspend" → "remove"; "favourite list" → "favourites list"). The previously-deferred boundary naming typo is now resolved. The save-count decrement is an Exception A side effect that keeps US-29's `view_fundraising_activity_save_count` in sync.

### US-25 — Search my favourites list ([diagram](../diagrams/sprint-3_diagrams/US-25.jpg))

**Actor:** Donee — *As a donee, I want to search my favourites list so that I can quickly locate specific favourite activities.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFavouriteListPage` *(shared with US-23/24)* | `displayMatchingFavourites(favouriteList: List<Favourite>): void` |
| Controller | `SearchFavouriteController` | `searchFavourite(accountId: String, searchCriteria: String): List<Favourite>` |
| Entity | `Favourite (FRAId, accountId)` | `searchFavourite(accountId: String, searchCriteria: String): List<Favourite>` |

**Code**
- [boundary/view_favourite_list_page.py:21](../boundary/view_favourite_list_page.py#L21) *(shared with US-23/24)*
- [controller/search_favourite_controller.py:11](../controller/search_favourite_controller.py#L11)
- [entity/favourite.py:73](../entity/favourite.py#L73) — JOINs `fundraising_activity` and matches `title / description / category` scoped to `account_id`

**Sidebar wiring:** Surfaced via `MyFavouritesPage` (search box at top); donee only.

**Tests**
- [tests/test_favourite.py](../tests/test_favourite.py) — match + cross-account-isolation + empty-result negatives
- [tests/test_search_favourite_controller.py](../tests/test_search_favourite_controller.py) — delegation + empty-list mirror
- [tests/test_view_favourite_list_page.py](../tests/test_view_favourite_list_page.py) — page smoke (shared with US-23/24)

**Notes / assumptions / deferred:** Re-exported diagram 2026-05-17 drops the `viewMode` param (class + sequence both 2-param now) and names the boundary `ViewFavouriteListPage` shared with US-23/24. Code's per-US `SearchFavouritePage` retired and merged into `view_favourite_list_page.py` (mirrors US-14/17 + US-30/31 patterns). Param order also flipped to `(accountId, searchCriteria)` — owner first, consistent with other owner-scoped methods. Both previously-deferred US-25 typos are now resolved.

### US-30 — Search my completed fundraising activities ([diagram](../diagrams/sprint-3_diagrams/US-30.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to search the history of my completed fundraising activities so that I can locate past campaigns.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyCompletedFundraisingActivitiesPage` *(shared with US-31)* | `displayMatchingMyCompletedFundraisingActivity(myCompletedFRAList: List<FundraisingActivity>): void` |
| Controller | `SearchMyCompletedFundraisingActivityController` | `searchMyCompletedFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>` |
| Entity | `FundraisingActivity (attrs as US-14)` | `searchMyCompletedFundraisingActivity(ownerAccountId: String, searchCriteria: String): List<FundraisingActivity>` |

**Code**
- [boundary/view_my_completed_fundraising_activities_page.py:19](../boundary/view_my_completed_fundraising_activities_page.py#L19)
- [controller/search_my_completed_fundraising_activity_controller.py:10](../controller/search_my_completed_fundraising_activity_controller.py#L10)
- [entity/fundraising_activity.py:184](../entity/fundraising_activity.py#L184) — owner-scoped + `completed = 1` filter + `LIKE` against `title / description / category`

**Sidebar wiring:** Surfaced via `ManageMyFundraisingActivityPage` (the "Completed" tab); fundraiser only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — completed match + skip-non-completed + cross-owner-isolation negatives
- [tests/test_search_my_completed_fundraising_activity_controller.py](../tests/test_search_my_completed_fundraising_activity_controller.py) — delegation + empty-list mirror
- [tests/test_view_my_completed_fundraising_activities_page.py](../tests/test_view_my_completed_fundraising_activities_page.py) — page smoke

**Notes / assumptions / deferred:** Re-exported diagram 2026-05-17 dropped the FRA short form and adopted full form (`searchMyCompletedFundraisingActivity`) — code renamed to match (previously `search_my_completed_fra`). US-30 and US-31 share the boundary class `ViewMyCompletedFundraisingActivitiesPage`; the page lives in a single file `boundary/view_my_completed_fundraising_activities_page.py` (mirrors the US-14/17 pattern where two USes contribute methods to one Boundary class).

### US-31 — View my completed fundraising activities ([diagram](../diagrams/sprint-3_diagrams/US-31.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to view a list of my completed fundraising activities so that I can keep track of them.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyCompletedFundraisingActivitiesPage` *(shared with US-30)* | `displayMyCompletedFundraisingActivities(myCompletedFRAList: List<FundraisingActivity>): void` |
| Controller | `ViewMyCompletedFundraisingActivitiesController` | `viewMyCompletedFundraisingActivities(ownerAccountId: String): List<FundraisingActivity>` |
| Entity | `FundraisingActivity (attrs as US-14)` | `viewMyCompletedFundraisingActivities(ownerAccountId: String): List<FundraisingActivity>` |

**Code**
- [boundary/view_my_completed_fundraising_activities_page.py](../boundary/view_my_completed_fundraising_activities_page.py) — shared with US-30
- [controller/view_my_completed_fundraising_activities_controller.py](../controller/view_my_completed_fundraising_activities_controller.py)
- [entity/fundraising_activity.py:204](../entity/fundraising_activity.py#L204) — owner-scoped + `completed = 1` filter; returns list

**Sidebar wiring:** Surfaced via `ManageMyFundraisingActivityPage` (the "Completed" tab). Clicking a row reuses US-13's `view_my_fundraising_activity(owner, fra_id)` for the detail panel — since the picker only shows completed activities, the picked id is always for a completed one, so no separate per-id "completed" lookup is needed. Fundraiser only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — completed-only owner happy + cross-owner-excluded + empty-when-no-completed negatives
- [tests/test_view_my_completed_fundraising_activities_controller.py](../tests/test_view_my_completed_fundraising_activities_controller.py) — delegation + empty-list mirror
- [tests/test_view_my_completed_fundraising_activities_page.py](../tests/test_view_my_completed_fundraising_activities_page.py) — page smoke (shared with US-30)

**Notes / assumptions / deferred:** Re-exported diagram 2026-05-17 reframed US-31 from a per-id detail view into a list view (`viewMyCompletedFundraisingActivities(owner): List<FundraisingActivity>`). The old per-id method `view_my_completed_activity(owner, fra_id)` was removed; the detail panel in `ManageMyFundraisingActivityPage` now reuses US-13's `view_my_fundraising_activity(owner, fra_id)`. The "is completed" guard moves from the entity (old: `WHERE completed = 1`) into the boundary picker (the click-source is the completed-only list, so the picked id is guaranteed completed).

### US-32 — Search my donation history ([diagram](../diagrams/sprint-3_diagrams/US-32.jpg))

**Actor:** Donee — *As a donee, I want to search my donation history so that I can review and track my past contributions.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyDonationHistoriesPage` | `displayMatchingMyDonationHistory(donationList: List<Donation>): void` |
| Controller | `SearchMyDonationHistoryController` (diagram) / `SearchDonationHistoryController` (code) | `searchMyDonationHistory(searchCriteria: String, accountId: String): List<Donation>` |
| Entity | `Donation (donationId, accountId, FRAId, amount: Decimal, donationDate: Date)` | `searchMyDonationHistory(searchCriteria: String, accountId: String): List<Donation>` |

**Code**
- [boundary/view_my_donation_histories_page.py:17](../boundary/view_my_donation_histories_page.py#L17)
- [controller/search_donation_history_controller.py:10](../controller/search_donation_history_controller.py#L10) (no "My" in class/method name)
- [entity/donation.py:61](../entity/donation.py#L61) — JOINs `fundraising_activity` and matches `title / description / category` scoped to `account_id`

**Sidebar wiring:** Surfaced via `MyDonationsPage` under **[Donee] My Donations**; donee only.

**Tests**
- [tests/test_donation.py](../tests/test_donation.py) — match + cross-account-isolation + empty-result negatives
- [tests/test_search_donation_history_controller.py](../tests/test_search_donation_history_controller.py) — delegation + empty-list mirror
- [tests/test_view_my_donation_histories_page.py](../tests/test_view_my_donation_histories_page.py) — page smoke

**Notes / assumptions / deferred:** **Deferred 2026-05-16** — diagram (now consistent across class + sequence) uses `SearchMyDonationHistoryController` / `searchMyDonationHistory`; code drops "My" — `SearchDonationHistoryController.search_donation_history`. Identical behaviour; just a name preference. The `accountId: Integer` typo on the source diagram was **resolved 2026-05-16**. No "create donation" use case exists on any diagram — the three rows displayed at demo time come from `seed_demo_donations` ([data/seed.py](../data/seed.py)) using `Donation.create_donation`.

### US-33 — View my donation history ([diagram](../diagrams/sprint-3_diagrams/US-33.jpg))

**Actor:** Donee — *As a donee, I want to view donation history so that I can track the campaigns I supported.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyDonationHistoryPage` | `displayMyDonationHistory(donation: Donation): void` |
| Controller | `ViewMyDonationHistoryController` | `viewMyDonationHistory(accountId: String, donationId: String): Donation` |
| Entity | `Donation (donationId, accountId, FRAId, amount, donationDate)` | `viewMyDonationHistory(accountId: String, donationId: String): Donation` |

**Code**
- [boundary/view_my_donation_history_page.py:20](../boundary/view_my_donation_history_page.py#L20)
- [controller/view_my_donation_history_controller.py:13](../controller/view_my_donation_history_controller.py#L13) (also hosts the Exception A `view_my_donations` picker)
- [entity/donation.py:83](../entity/donation.py#L83) — `WHERE donation_id = ? AND account_id = ?`; returns `None` for missing rows or cross-donee access

**Sidebar wiring:** Surfaced via `MyDonationsPage` (clicking a search row opens the detail panel); donee only.

**Tests**
- [tests/test_donation.py](../tests/test_donation.py) — happy + missing-id + cross-account-isolation negatives
- [tests/test_view_my_donation_history_controller.py](../tests/test_view_my_donation_history_controller.py) — delegation + `None` mirror; also covers `view_my_donations`
- [tests/test_view_my_donation_history_page.py](../tests/test_view_my_donation_history_page.py) — page smoke

**Notes / assumptions / deferred:** Exception A method `Donation.view_my_donations(account_id)` ([entity/donation.py:99](../entity/donation.py#L99)) added so the Boundary can list every donation owned by the signed-in donee before they pick one — logged in [docs/todo.md](todo.md). Diagram return type `Donation` (no failure branch) is implemented as `Optional[Donation]` under the same implicit-failure convention.

---

## Sprint 4

Diagrams: [diagrams/sprint-4_diagrams/](../diagrams/sprint-4_diagrams/). Stories: US-28, US-29, US-34, US-35, US-36, US-37, US-38, US-41, US-42, US-43.

### US-28 — View fundraising activity view count ([diagram](../diagrams/sprint-4_diagrams/US-28.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to view the number of views of my fundraising activity so that I can measure audience interest.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyFundraisingActivityPage` | `displayFundraisingActivityViewCount(viewCount: Integer): void` |
| Controller | `ViewFundraisingActivityViewCountController` | `viewFundraisingActivityViewCount(FRAId: String): Integer` |
| Entity | `FundraisingActivity (FRAId, title, description, targetAmount, category, startDate, endDate, completed, suspended, ownerAccountId, viewCount: Integer, saveCount: Integer)` | `viewFundraisingActivityViewCount(FRAId: String): Integer` |

**Code**
- [boundary/view_my_fundraising_activity_page.py](../boundary/view_my_fundraising_activity_page.py) — count rendered via `activity.view_count` on the dataclass
- [controller/view_fundraising_activity_view_count_controller.py](../controller/view_fundraising_activity_view_count_controller.py)
- [entity/fundraising_activity.py:312](../entity/fundraising_activity.py#L312) `view_fundraising_activity_view_count`
- [entity/fundraising_activity.py:337](../entity/fundraising_activity.py#L337) `increment_view_count` (Exception A)

**Sidebar wiring:** Surfaced via `ManageMyFundraisingActivityPage` (read-only detail view) under **[Fundraiser] Manage My Fundraising Activities**; fundraiser only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — entity happy + missing-row returns 0 + increment-on-missing returns False
- [tests/test_view_fundraising_activity_view_count_controller.py](../tests/test_view_fundraising_activity_view_count_controller.py) — delegation + integer mirror
- [tests/test_view_my_fundraising_activity_page.py](../tests/test_view_my_fundraising_activity_page.py) — page smoke

**Notes / assumptions / deferred:** Diagram redraw **2026-05-16** moved the boundary from the donee's `ViewFundraisingActivityPage` to the fundraiser's `ViewMyFundraisingActivityPage` — resolved in [docs/diagram_typos.md](diagram_typos.md). The entity returns `0` (rather than raising) for a missing FRAId so the UI can always render a number. `increment_view_count` is an Exception A write fired from US-21 when a donee opens an activity.

### US-29 — View fundraising activity save count ([diagram](../diagrams/sprint-4_diagrams/US-29.jpg))

**Actor:** Fundraiser — *As a fundraiser, I want to view the number of times my fundraising activity has been saved to a donee's favourite list so that I can gauge potential donor interest.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewMyFundraisingActivityPage` | `displayFundraisingActivitySaveCount(saveCount: Integer): void` |
| Controller | `ViewFundraisingActivitySaveCountController` | `viewFundraisingActivitySaveCount(FRAId: String): Integer` |
| Entity | `FundraisingActivity (attrs as US-28)` | `viewFundraisingActivitySaveCount(FRAId: String): Integer` |

**Code**
- [boundary/view_my_fundraising_activity_page.py](../boundary/view_my_fundraising_activity_page.py) — shares the US-28 page; same dataclass field `activity.save_count`
- [controller/view_fundraising_activity_save_count_controller.py](../controller/view_fundraising_activity_save_count_controller.py)
- [entity/fundraising_activity.py:325](../entity/fundraising_activity.py#L325) `view_fundraising_activity_save_count`
- [entity/fundraising_activity.py:350](../entity/fundraising_activity.py#L350) `increment_save_count(fra_id, delta)` (Exception A; floors at 0)

**Sidebar wiring:** Same as US-28 — the "Saves" metric on the read-only detail view inside `ManageMyFundraisingActivityPage`; fundraiser only.

**Tests**
- [tests/test_fundraising_activity.py](../tests/test_fundraising_activity.py) — entity happy + missing-row + increment by +1 / −1 + floor-at-zero guard
- [tests/test_view_fundraising_activity_save_count_controller.py](../tests/test_view_fundraising_activity_save_count_controller.py)
- [tests/test_view_my_fundraising_activity_page.py](../tests/test_view_my_fundraising_activity_page.py)

**Notes / assumptions / deferred:** Same boundary correction as US-28 (was the donee's view page on the original diagram). `increment_save_count` is Exception A: US-22 fires `delta=+1` when a donee favourites; US-23 fires `delta=−1` on remove. The `MAX(save_count + ?, 0)` guard prevents a missing favourite row from driving the count negative.

### US-34 — Create fundraising activity category ([diagram](../diagrams/sprint-4_diagrams/US-34.jpg))

**Actor:** Platform manager — *As a platform manager, I want to create a fundraising activity category so that fundraising activities can be classified properly.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `CreateFundraisingActivityCategoryPage` | `displaySuccess(FRACategory: FundraisingActivityCategory): void` |
| Controller | `CreateFundraisingActivityCategoryController` | `createCategory(categoryName: String, description: String): FundraisingActivityCategory` |
| Entity | `FundraisingActivityCategory (FRACatId, categoryName, description, suspended: Boolean)` | `createCategory(categoryName: String, description: String): FundraisingActivityCategory` |

**Code**
- [boundary/create_fundraising_activity_category_page.py](../boundary/create_fundraising_activity_category_page.py)
- [controller/create_fundraising_activity_category_controller.py](../controller/create_fundraising_activity_category_controller.py)
- [entity/fundraising_activity_category.py:31](../entity/fundraising_activity_category.py#L31) `create_category`

**Sidebar wiring:** Exposed inside `ManageFundraisingActivityCategoryPage` via the "+ Create new category" button under **[PM] Manage FRA Categories**; platform manager only.

**Tests**
- [tests/test_fundraising_activity_category.py](../tests/test_fundraising_activity_category.py) — happy + format guards
- [tests/test_fundraising_activity_category_controllers.py](../tests/test_fundraising_activity_category_controllers.py)
- [tests/test_fundraising_activity_category_pages.py](../tests/test_fundraising_activity_category_pages.py)

**Notes / assumptions / deferred:** Empty-field validation lives in the boundary per the architecture rule. No uniqueness constraint on `category_name` — the diagram does not declare one. The Boundary surfaces the created category id + name in the success message.

### US-35 — View fundraising activity category ([diagram](../diagrams/sprint-4_diagrams/US-35.jpg))

**Actor:** Platform manager — *As a platform manager, I want to view a fundraising activity category so that I can inspect its details.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFundraisingActivityCategoryPage` | `displayFundraisingActivityCategory(FRACategory: FundraisingActivityCategory): void` |
| Controller | `ViewFundraisingActivityCategoryController` | `viewFundraisingActivityCategory(FRACatId: String): FundraisingActivityCategory` |
| Entity | `FundraisingActivityCategory (attrs as US-34)` | `viewFundraisingActivityCategory(FRACatId: String): FundraisingActivityCategory` |

**Code**
- [boundary/view_fundraising_activity_category_page.py](../boundary/view_fundraising_activity_category_page.py) — list-then-detail picker, shared with US-38's suspend button
- [controller/view_fundraising_activity_category_controller.py](../controller/view_fundraising_activity_category_controller.py) — hosts both the singular `view_fundraising_activity_category` and the Exception A `view_all_categories`
- [entity/fundraising_activity_category.py:50](../entity/fundraising_activity_category.py#L50) `view_fundraising_activity_category`
- [entity/fundraising_activity_category.py:124](../entity/fundraising_activity_category.py#L124) `view_all_categories` (Exception A)

**Sidebar wiring:** Surfaced as the detail panel of `ManageFundraisingActivityCategoryPage` after a row is clicked; platform manager only.

**Tests**
- [tests/test_fundraising_activity_category.py](../tests/test_fundraising_activity_category.py) — happy + missing-row → `None`
- [tests/test_fundraising_activity_category_controllers.py](../tests/test_fundraising_activity_category_controllers.py) — happy + `None`-forwarding
- [tests/test_fundraising_activity_category_pages.py](../tests/test_fundraising_activity_category_pages.py)

**Notes / assumptions / deferred:** `view_all_categories` is an Exception A list-method on the same controller — needed to populate the picker before the diagram-defined singular call fires. Listed under "Exception A" in [docs/todo.md](todo.md). Missing rows return `None`; the Boundary clears the stale selection key.

### US-36 — Update fundraising activity category ([diagram](../diagrams/sprint-4_diagrams/US-36.jpg))

**Actor:** Platform manager — *As a platform manager, I want to update a fundraising activity category so that category information remains accurate.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `UpdateFundraisingActivityCategoryPage` | `displaySuccess(): void` |
| Controller | `UpdateFundraisingActivityCategoryController` | `updateFundraisingActivityCategory(FRACatId: String, updatedFRACategory: FundraisingActivityCategory): Boolean` |
| Entity | `FundraisingActivityCategory (attrs as US-34)` | `updateFundraisingActivityCategory(FRACatId: String, updatedFRACategory: FundraisingActivityCategory): Boolean` |

**Code**
- [boundary/update_fundraising_activity_category_page.py](../boundary/update_fundraising_activity_category_page.py)
- [controller/update_fundraising_activity_category_controller.py](../controller/update_fundraising_activity_category_controller.py)
- [entity/fundraising_activity_category.py:63](../entity/fundraising_activity_category.py#L63) — returns `cursor.rowcount > 0`

**Sidebar wiring:** Surfaced as the "Update" button on the detail panel of `ManageFundraisingActivityCategoryPage`; platform manager only.

**Tests**
- [tests/test_fundraising_activity_category.py](../tests/test_fundraising_activity_category.py) — happy + unknown FRACatId returns `False`
- [tests/test_fundraising_activity_category_controllers.py](../tests/test_fundraising_activity_category_controllers.py)
- [tests/test_fundraising_activity_category_pages.py](../tests/test_fundraising_activity_category_pages.py)

**Notes / assumptions / deferred:** Both name and description are required by the Boundary before delegation. The `suspended` flag is included on the updated dataclass but the combined `Manage*` page keeps it pinned to the current value — the suspend toggle is exposed via separate buttons. No diagram divergences pending.

### US-37 — Search fundraising activity categories ([diagram](../diagrams/sprint-4_diagrams/US-37.jpg))

**Actor:** Platform manager — *As a platform manager, I want to search fundraising activity categories so that I can quickly find a specific category.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFundraisingActivityCategoriesPage` | `displayMatchingFundraisingActivityCategory(FRACategoryList: List<FundraisingActivityCategory>): void` |
| Controller | `SearchFundraisingActivityCategoryController` | `searchFundraisingActivityCategory(searchCriteria: String): List<FundraisingActivityCategory>` |
| Entity | `FundraisingActivityCategory (attrs as US-34)` | `searchFundraisingActivityCategory(searchCriteria: String): List<FundraisingActivityCategory>` |

**Code**
- [boundary/view_fundraising_activity_categories_page.py](../boundary/view_fundraising_activity_categories_page.py)
- [controller/search_fundraising_activity_category_controller.py](../controller/search_fundraising_activity_category_controller.py)
- [entity/fundraising_activity_category.py:84](../entity/fundraising_activity_category.py#L84) — case-insensitive `LIKE %term%` against `category_name` + `description`

**Sidebar wiring:** Surfaced as the search box at the top of `ManageFundraisingActivityCategoryPage`'s list view; platform manager only.

**Tests**
- [tests/test_fundraising_activity_category.py](../tests/test_fundraising_activity_category.py) — name match + description match + no-match → `[]`
- [tests/test_fundraising_activity_category_controllers.py](../tests/test_fundraising_activity_category_controllers.py) — happy + empty-list delegation
- [tests/test_fundraising_activity_category_pages.py](../tests/test_fundraising_activity_category_pages.py)

**Notes / assumptions / deferred:** Empty / whitespace-only criteria are rejected by the Boundary. Matching uses `COALESCE(description, '')` so categories with `NULL` descriptions don't trip the `LIKE`. No outstanding diagram typos.

### US-38 — Suspend fundraising activity category ([diagram](../diagrams/sprint-4_diagrams/US-38.jpg))

**Actor:** Platform manager — *As a platform manager, I want to suspend a fundraising category so that obsolete categories are no longer used.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `ViewFundraisingActivityCategoryPage` | `displaySuccess(): void` |
| Controller | `SuspendFundraisingActivityCategoryController` | `suspendFundraisingActivityCategory(FRACatId: String): Boolean` |
| Entity | `FundraisingActivityCategory (attrs as US-34)` | `suspendFundraisingActivityCategory(FRACatId: String): Boolean` |

**Code**
- [boundary/view_fundraising_activity_category_page.py](../boundary/view_fundraising_activity_category_page.py) — same boundary class as US-35; the Suspend button renders only when `category.suspended` is false
- [controller/suspend_fundraising_activity_category_controller.py](../controller/suspend_fundraising_activity_category_controller.py)
- [controller/unsuspend_fundraising_activity_category_controller.py](../controller/unsuspend_fundraising_activity_category_controller.py) — Exception A mirror
- [entity/fundraising_activity_category.py:100](../entity/fundraising_activity_category.py#L100) `suspend_fundraising_activity_category`
- [entity/fundraising_activity_category.py:111](../entity/fundraising_activity_category.py#L111) `unsuspend_fundraising_activity_category` (Exception A)

**Sidebar wiring:** Surfaced as the Suspend / Unsuspend toggle on the detail panel of `ManageFundraisingActivityCategoryPage`; platform manager only.

**Tests**
- [tests/test_fundraising_activity_category.py](../tests/test_fundraising_activity_category.py) — happy + unknown id returns `False`
- [tests/test_fundraising_activity_category_controllers.py](../tests/test_fundraising_activity_category_controllers.py)
- [tests/test_fundraising_activity_category_pages.py](../tests/test_fundraising_activity_category_pages.py)

**Notes / assumptions / deferred:** `unsuspend_fundraising_activity_category` + its dedicated controller are an Exception A toggle pair — listed under "Unsuspend toggle (Exception A, UX)" in [docs/diagram_typos.md](diagram_typos.md). Both must be added to the US-38 class diagram (or a new "unsuspend" use case defined) before final marking.

### US-41 — Generate daily report ([diagram](../diagrams/sprint-4_diagrams/US-41.jpg))

**Actor:** Platform manager — *As a platform manager, I want to generate a daily report so that I can track daily platform activity.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `GenerateReportPage` | `displayReport(report: Report): void` |
| Controller | `GenerateDailyReportController` | `generateDailyReport(startDate: Date, endDate: Date, platformManagerId: String): Report` |
| Entity | `Report (reportId, reportType, startDate: Date, endDate: Date, generatedAt: datetime, platformManagerId, totalDonationAmount: Decimal, totalDonationCount, totalActivityCount, totalFundraiserCount, totalDoneeCount)` | `generateDailyReport(startDate: Date, endDate: Date, platformManagerId: String): Report` |

**Code**
- [boundary/generate_report_page.py](../boundary/generate_report_page.py) — internal radio routes daily/weekly/monthly; `platform_manager_id` sourced from `st.session_state["user"].account_id`
- [controller/generate_daily_report_controller.py](../controller/generate_daily_report_controller.py)
- [entity/report.py:42](../entity/report.py#L42) `generate_daily_report`
- [entity/report.py:66](../entity/report.py#L66) `_generate` (shared aggregation helper)

**Sidebar wiring:** Sidebar entry **[PM] Generate Report** → `GenerateReportPage`; platform manager only. The same page hosts US-42 and US-43.

**Tests**
- [tests/test_report.py](../tests/test_report.py) — happy + zero-row window (empty donations → `total=0`)
- [tests/test_report_controllers.py](../tests/test_report_controllers.py) — three pure-delegator tests
- [tests/test_generate_report_page.py](../tests/test_generate_report_page.py)

**Notes / assumptions / deferred:** The `platformManagerId` 3rd parameter and `generatedAt: datetime` typing were **resolved 2026-05-16** ([docs/diagram_typos.md](diagram_typos.md)). Boundary enforces `start_date <= end_date` before delegating. Aggregates donations within the window and counts all activities / fundraiser / donee accounts (snapshot, not windowed).

### US-42 — Generate weekly report ([diagram](../diagrams/sprint-4_diagrams/US-42.jpg))

**Actor:** Platform manager — *As a platform manager, I want to generate a weekly report so that I can track short-term platform trends.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `GenerateReportPage` | `displayReport(report: Report): void` |
| Controller | `GenerateWeeklyReportController` | `generateWeeklyReport(startDate: Date, endDate: Date, platformManagerId: String): Report` |
| Entity | `Report (attrs as US-41)` | `generateWeeklyReport(startDate: Date, endDate: Date, platformManagerId: String): Report` |

**Code**
- [boundary/generate_report_page.py](../boundary/generate_report_page.py) — same class as US-41; the `report_type == "weekly"` branch
- [controller/generate_weekly_report_controller.py](../controller/generate_weekly_report_controller.py)
- [entity/report.py:50](../entity/report.py#L50) `generate_weekly_report`

**Sidebar wiring:** Same as US-41 — the weekly radio option on **[PM] Generate Report**; platform manager only.

**Tests**
- [tests/test_report.py](../tests/test_report.py) — weekly variant (asserts `report_type == "weekly"`)
- [tests/test_report_controllers.py](../tests/test_report_controllers.py)
- [tests/test_generate_report_page.py](../tests/test_generate_report_page.py)

**Notes / assumptions / deferred:** `report_type` discriminator is the only behavioural difference from US-41/43 — the `_generate` helper handles the actual aggregation. The shared `GenerateReportPage` consolidation is **deferred** (accepted as deliberate). Same diagram fixes as US-41.

### US-43 — Generate monthly report ([diagram](../diagrams/sprint-4_diagrams/US-43.jpg))

**Actor:** Platform manager — *As a platform manager, I want to generate a monthly report so that I can track long-term platform trends.*

**Diagram-defined surface**

| Layer | Class | Method |
|---|---|---|
| Boundary | `GenerateReportPage` | `displayReport(report: Report): void` |
| Controller | `GenerateMonthlyReportController` | `generateMonthlyReport(startDate: Date, endDate: Date, platformManagerId: String): Report` |
| Entity | `Report (attrs as US-41)` | `generateMonthlyReport(startDate: Date, endDate: Date, platformManagerId: String): Report` |

**Code**
- [boundary/generate_report_page.py](../boundary/generate_report_page.py) — `report_type == "monthly"` branch
- [controller/generate_monthly_report_controller.py](../controller/generate_monthly_report_controller.py)
- [entity/report.py:58](../entity/report.py#L58) `generate_monthly_report`

**Sidebar wiring:** Same as US-41/42 — the monthly radio option on **[PM] Generate Report**; platform manager only.

**Tests**
- [tests/test_report.py](../tests/test_report.py) — monthly variant + the shared `_aggregate_stats` zero / non-zero paths
- [tests/test_report_controllers.py](../tests/test_report_controllers.py)
- [tests/test_generate_report_page.py](../tests/test_generate_report_page.py)

**Notes / assumptions / deferred:** Same shared-boundary consolidation as US-41/42 — listed under "Deferred typos" in [docs/todo.md](todo.md). The window is not enforced to match the report cadence (a "monthly" report over a 2-day window still aggregates correctly) — the cadence label is informational metadata only.

---

## Architecture conventions

1. **Validation lives in the Boundary.** Empty fields, format checks, date sanity, positive amounts — checked before any controller is called. Business-rule failures (uniqueness, existence, ownership) are reported by the Entity via `None` / `False` return values; the Boundary turns those into `st.error(...)` messages.
2. **Controllers are pure delegators.** One method per controller, takes Boundary input, calls one Entity method, returns the result. No branching, no transformation, no logging.
3. **No `get_*` / `retrieve_*` method names.** Entity methods are named after user-facing actions (`login`, `create_account`, `view_user_profile`, `save_fundraising_activity`). SQL `SELECT`s are an internal implementation detail.
4. **Class-name suffixes are fixed.** Boundary classes end in `Page` (or `LogoutPage`), Controller classes end in `Controller`, Entity classes have no suffix.
5. **Method signatures match the diagrams character-for-character** (modulo `snake_case`). Same arity, same return type.
6. **Boundary never imports Entity directly for behaviour** — all Entity *access* goes through a Controller. Boundary may import an Entity dataclass purely to *construct* an instance to pass into a controller method (e.g. for update operations whose signature is `update_user_profile(profile_id, UserProfile)`).
7. **Ownership scoping** is enforced at the Entity layer for fundraiser stories — every `*_my_*` method takes `owner_account_id` and joins / filters on it.

## The three documented Exceptions

These are the narrow carve-outs from the strict rules above. Each is tracked in [docs/todo.md](todo.md) so it can be reconciled with the diagrams before final marking.

### Exception A — Off-diagram entity methods to power UX

Methods added to entities (with pure-delegator controllers) so a Boundary can show a list / dropdown / count that the diagrams don't declare. Each is named per the project's verb convention (no `get_*` / `retrieve_*`).

- `UserProfile.view_all_profiles()` — populates the profile dropdown on `CreateAccountPage` (US-6).
- `UserAccount.view_all_user_accounts()` — populates the account-picker on Manage user accounts (US-7 / US-8).
- `FundraisingActivity.view_all_fundraising_activities()` — populates the donee browse list (US-21).
- `FundraisingActivity.view_my_fundraising_activities(owner_account_id)` — owner-scoped picker on Manage my fundraising activities (US-14 / US-15).
- `Donation.view_my_donations(account_id)` — picker on `MyDonationsPage` (US-33).
- `FundraisingActivity.increment_view_count(fra_id)` and `increment_save_count(fra_id, delta)` — count writes triggered by US-21 (view), US-22 (save), US-23 (remove).
- Four `unsuspend_*` methods on `UserProfile` / `UserAccount` / `FundraisingActivity` / `FundraisingActivityCategory` — mirror the diagram-defined suspends so the consolidated Manage pages can toggle.

### Exception B — Debug-only utilities

[boundary/non_diagram/info_page.py](../boundary/non_diagram/info_page.py) (`.info (debug)`) reads every table directly via `persistence/db.get_connection()`, bypassing the B-C-E layers. Tracked in [docs/todo.md](todo.md); to be hidden before the final recorded demo.

### Exception C — UX consolidation (combined Boundary pages)

The reworked diagrams define 27 per-US Boundary classes. The sidebar would be unusable with 27 entries, so the implementation wires **seven combined pages** that compose search + list + detail + inline create + update + suspend/unsuspend per resource. Every per-US Boundary class still exists as a tested artifact — the diagrams stay 1:1 with their stories; only *which* class is wired into the sidebar differs.

| Combined page (sidebar entry) | Per-US Boundary classes it replaces in the sidebar |
|---|---|
| `ManageUserProfilePage` | `CreateProfilePage`, `ViewUserProfilePage`, `UpdateUserProfilePage`, `ViewUserProfilesPage` (+ US-4 suspend button) |
| `ManageUserAccountPage` | `CreateAccountPage`, `ViewUserAccountPage`, `UpdateUserAccountPage`, `ViewUserAccountsPage` (+ US-9 suspend button) |
| `ManageMyFundraisingActivityPage` | `CreateFundraisingActivityPage`, `ViewMyFundraisingActivityPage`, `UpdateMyFundraisingActivityPage`, `ViewMyFundraisingActivitiesPage`, `ViewMyCompletedFundraisingActivitiesPage` |
| `BrowseFundraisingActivityPage` | `ViewFundraisingActivityPage` (+ US-22 save), `ViewFundraisingActivitiesPage` (US-20 search) |
| `MyFavouritesPage` | `ViewFavouriteListPage` (US-23 remove + US-24 list + US-25 search) |
| `MyDonationsPage` | `ViewMyDonationHistoryPage`, `ViewMyDonationHistoriesPage` |
| `ManageFundraisingActivityCategoryPage` | `CreateFundraisingActivityCategoryPage`, `ViewFundraisingActivityCategoryPage`, `UpdateFundraisingActivityCategoryPage`, `ViewFundraisingActivityCategoriesPage` (+ US-38 suspend) |

`GenerateReportPage` (US-41 / US-42 / US-43) is already shared on the diagrams — no Exception C needed there.

## Lecturer decisions

Items the lecturer has explicitly accepted; diagrams and code stay as-is. See [docs/todo.md "Lecturer decisions"](todo.md).

- **Demo donations seed (2026-05-15).** Three donations seeded against the default donee + fundraiser so US-32 / US-33 have data to display.
- **Email uniqueness on `UserAccount` (2026-05-15).** `UNIQUE` constraint at the schema level. `create_account` returns `Optional[UserAccount]`; `update_user_account` returns `False` on conflict.
- **No `displayError` on Sprint 1 boundaries (2026-05-16).** Error display is treated as implicit; diagrams will not be updated.
- **Login failure return type on US-11 / US-18 / US-26 / US-39 (2026-05-16).** Implementation's `None`-on-no-match accepted as the implicit convention.

## Deferred typos (accepted code-vs-diagram divergences)

Sprint 3 / Sprint 4 items where the diagram and code disagree but the team has chosen to live with the divergence. Each has an inline `Deferred 2026-05-16` note in [diagram_typos.md](diagram_typos.md). See [todo.md "Deferred typos"](todo.md) for the consolidated index.

- **US-30 / US-31 shared boundary** — both diagrams name `ViewMyCompletedFundraisingActivitiesPage`; code consolidates into a single file `boundary/view_my_completed_fundraising_activities_page.py` (mirrors the US-14/17 pattern where two USes contribute methods to one Boundary class). Resolved 2026-05-17.
- **US-32 "My" naming** — diagram `SearchMyDonationHistoryController` / `searchMyDonationHistory`; code drops "My" (`SearchDonationHistoryController` / `Donation.search_donation_history`).
- **US-41 / US-42 / US-43 shared `GenerateReportPage`** — accepted as a deliberate consolidation; one boundary handles daily / weekly / monthly via a radio selector.

## Open architectural items

- **Plain-text passwords.** Sprint 1's `UserAccount` stores the password as plain text per the diagram. Hashing (bcrypt / argon2) belongs in a hardening sprint.

## Persistence

- **DB file:** `app.db` at the repo root (gitignored). Created on first call to `init_db()` which runs [persistence/schema.sql](../persistence/schema.sql).
- **Connection helper:** [persistence/db.py](../persistence/db.py) exposes `get_connection()` (returns a `sqlite3.Connection` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`) and `init_db()`. Entities open a connection per operation — no shared session.
- **Schema:** 7 tables — `user_profile`, `user_account` (with `UNIQUE` on `email`), `fundraising_activity` (with `view_count`, `save_count`, `completed`, `suspended`), `fundraising_activity_category`, `favourite` (composite PK `(account_id, fra_id)`), `donation`, `report`. All `*_id` PKs are `TEXT` storing the prefixed `prefix_NNN` form directly.
- **Prefixed string IDs:** [persistence/ids.py](../persistence/ids.py) defines `format_id(prefix, n)` + `next_id(conn, table, id_column, prefix)`. Entities call `next_id` on every INSERT to mint the next `prof_NNN`, `acc_NNN`, `fra_NNN`, `cat_NNN`, `don_NNN`, `rep_NNN`. Tests assert against the prefixed form.

## Session, routing, RBAC

- **Session state:** the logged-in user lives in `st.session_state["user"]` as a `UserAccount` instance. Login writes it; logout clears it; pages read it directly. Mutating session state is always followed by `st.rerun()` so the sidebar caption (which renders before page logic) picks up the new value on the next pass.
- **Routing:** [app.py](../app.py) holds two dicts:
  - `PAGES`: sidebar-label → Boundary-class (10 entries + `.info (debug)`)
  - `PAGES_BY_ROLE`: role → allow-list of labels (`None`, `admin`, `fundraiser`, `donee`, `platform_manager`)
- **`_current_role()`** looks up the session user's profile via `ViewUserProfileController.view_user_profile` and returns `profile.role` (or `None`). `main()` then filters `PAGES.keys()` by the role's allow-list before rendering the sidebar radio.
- **Sidebar caption:** shows `Signed in as <name> (<role>) <email>` for signed-in users; `Not signed in` otherwise.

## Seed data

[data/seed.py](../data/seed.py) is idempotent — every function checks for existence before inserting. Auto-runs on `streamlit run app.py` (no manual seed needed). Standalone: `python -m data.seed`. Reset: `rm app.db && python -m data.seed`.

Seeded on every startup:

| Role | Email | Password |
|---|---|---|
| Admin | `a001@a.com` | `123` |
| Fundraiser | `fr001@a.com` | `123` |
| Donee | `d001@a.com` | `123` |
| Platform Manager | `pm001@a.com` | `123` |

Plus a demo `FundraisingActivity` ("Demo hospital fund") owned by the seeded fundraiser, and **three demo `Donation` rows** from the seeded donee against it — lecturer-approved bootstrap convention so US-32 / US-33 have data on first launch.

## Tests + CI

- **TDD expectations:** every entity method ships with a happy-path test **and** at least one negative-path test (missing row, FK violation, uniqueness violation, cross-tenant access where ownership applies). Controllers have a delegation test + a negative-path delegation mirror. Boundary smoke tests use `streamlit.testing.v1.AppTest`.
- **Test isolation:** [tests/conftest.py](../tests/conftest.py) defines an `autouse` fixture that monkey-patches `persistence.db.DB_PATH` to a `tmp_path` file and re-initialises the schema before every test. Never write tests that assume `app.db`.
- **Run:** `pytest` (full suite, 373 tests) or `pytest -v` (matches CI). Single test: `pytest tests/test_user_account.py::test_login_succeeds`. By keyword: `pytest -k favourite`.
- **CI:** [.github/workflows/ci.yml](../.github/workflows/ci.yml) pins Python 3.11 and runs `pytest -v` on every push.

## Cross-references

- Project rules, anti-patterns, sprint workflow → [CLAUDE.md](../CLAUDE.md)
- Diagram-vs-code typo log → [docs/diagram_typos.md](diagram_typos.md)
- Bootstrap deviations, Exception A entries, lecturer decisions, deferred typos, open items → [docs/todo.md](todo.md)
- Source UML diagrams → [diagrams/](../diagrams/)
