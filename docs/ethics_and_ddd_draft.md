# SDM FundRaise Platform — Ethical Issues and Data-Driven Development Plan

CSIT314 Software Development Methodologies — Group Project Draft

---

## Document Purpose

This document is a report-ready draft for two SDM deliverables: an **ethical issues plan** and a **data-driven development (DDD) proposal**. The content is written specifically for the FundRaise Platform project, where donees search for and donate to fundraising activities, and fundraisers create and manage their own fundraising activities.

The ethical issues section discusses two process-related issues (how the team works) and two product-related issues (what the system does). The DDD section explains how platform data and machine learning can be used to recommend fundraising activities to donees and to help fundraisers gauge whether their target is realistic, following a nine-step process from problem definition through monitoring and ethical considerations.

---

## 1. Ethical Issues

Ethical issues are not limited to privacy or security inside the product. The team also has to consider how it works during development. This section discusses two ethical issues during the development process and two ethical issues within the product itself.

### 1.1 Process-related Ethical Issues

These issues concern how the team works together while building the system.

**A. Fair Work Distribution**

During the development process, the team considered fairness by ensuring that the workload was distributed as equally as possible among all members. Tasks were assigned each sprint based on the sprint backlog and each member's responsibility, covering coding, diagram authoring, testing, persistence/schema design, and documentation. This helped prevent unfair workload imbalance, where one member would do most of the work while others did very little. Author attribution was preserved in the commit history, and weekly stand-ups were used to check that each member was contributing meaningfully across the four sprints.

**B. Inclusiveness and Equal Opportunity to Contribute**

The team also considered inclusiveness by giving every member the opportunity to share their strengths, preferences, and concerns during sprint planning. Work was allocated based on each member's abilities — such as UI design with Streamlit, backend implementation, SQLite/schema design, diagram preparation, or test writing — so that members could contribute in the area where they were most effective. At the same time, each member retained at least one core implementation responsibility per sprint, so nobody was silently sidelined and every member gained experience across the Boundary–Controller–Entity layers.

### 1.2 Product-related Ethical Issues

These issues concern what is built into the system.

**A. Data Privacy**

The FundRaise Platform considers data privacy by ensuring that users can only access and manage their own personal information and fundraising-related records. A fundraiser should only be able to update, suspend, or delete their own fundraising activity, and should not be able to modify another fundraiser's records. A donee should similarly only see and manage their own favourites and (once donation history is implemented) their own donation records. This protects user privacy and prevents unauthorised access to sensitive information such as profile details, contact data, and donation amounts.

**B. Role-based Access Control and Permission Control**

The system applies role-based access control so that each actor — User Admin, Fundraiser, Donee, and Platform Manager — can only perform actions that are appropriate to their role. A Fundraiser may create and manage fundraising activities; a Donee may search activities, save favourites, and donate; a User Admin may manage user accounts and profiles. However, an administrator should not freely modify or delete a fundraiser's activity unless there is a valid policy reason such as removing inappropriate content. This separation protects user ownership of records and limits unnecessary access to private data, ensuring that each role has only the permissions it actually needs.

---

## 2. Data-Driven Development Proposal

The lecturer suggested using data-driven development to improve the FundRaise Platform. Two related ideas fit naturally with the system: (1) recommending the most suitable fundraising activities to each donee based on their interests, preferences, and donation amount, and (2) helping a fundraiser estimate whether their fundraising target is realistic given similar past activities.

### 2.1 The Idea — Donor–Activity Matching and Target-Realism Estimation

A donee enters their interests, preferred categories, and intended donation amount when they create a profile and use the platform. A fundraiser creates a fundraising activity with a category, target amount, description, and deadline. The FundRaise Platform can apply a machine-learning model to match each donee with the activities they are most likely to support, and to estimate how likely a fundraiser's target is to be reached. This benefits donees (who currently have to scroll a long list of activities), benefits fundraisers (who can adjust unrealistic targets before launch), and benefits the platform overall by improving the rate at which campaigns succeed.

### 2.2 Nine-Step Data-Driven Development Process

**1. Problem / Requirement.** Many donees on the platform struggle to find fundraising activities that match their interests because they have to manually browse or keyword-search through a long list of activities. At the same time, some fundraisers set unrealistic targets without knowing how similar past activities have performed. The FundRaise Platform can therefore use donee profile data, favourites, donation history, and fundraising-activity attributes to (a) recommend the most suitable activities to each donee and (b) estimate whether a fundraiser's chosen target is realistic. This provides a more personalised experience for donees and more informed planning for fundraisers.

**2. Data Collection.** The system will collect data from existing platform records, including donee profile information (categories of interest, location), favourites, search history, and donation history once US-32/US-33 are implemented. From the fundraiser side, it will use fundraising-activity metadata such as category, target amount, current amount raised, time remaining, and the historical completion rate of similar activities. Only data that is necessary for matching and target estimation should be collected, in order to reduce privacy risks. Where data is missing, voluntary profile fields are preferred over inferring sensitive attributes.

**3. Data Cleaning.** Before the data is used, the system must clean it to remove errors and inconsistencies. For example, duplicate accounts, incomplete profiles, free-text category fields that should map to a fixed set, and fundraising activities with unrealistic target amounts must be detected and handled. Missing values may be removed, imputed with documented rules (such as a default "unknown" category), or flagged for review depending on importance. Leftover seed data from `data/seed.py` must also be excluded so it does not bias the trained model.

**4. Data Preparation.** After cleaning, the data is prepared into useful features for the model. For each donee, the system can derive an interest vector from past favourites, donations, and category browsing patterns. For each fundraising activity, features such as days-remaining, percent-funded, category popularity, and fundraiser reputation can be calculated. The prepared data is then split into training, validation, and test sets, ideally divided by time so that the model is evaluated on its ability to predict future behaviour rather than to interpolate past behaviour.

**5. Model Training.** The recommendation model can be trained using historical donor–activity interactions. A simple, interpretable starting point such as collaborative filtering or a logistic-regression ranker is preferred, and more complex neural recommenders should be considered only if the baseline is clearly insufficient. A separate regression or classification model can be trained to predict whether a given fundraising activity will reach its target, using features such as category, target amount, deadline, and fundraiser history. Training runs should be reproducible by fixing random seeds, pinning dependency versions, and recording model artefacts alongside the data snapshot used.

**6. Model Evaluation.** The model is evaluated by checking whether its recommendations and target estimates match real donee behaviour and historical fundraising outcomes. Useful metrics include precision@5 and click-through rate for the recommender, and accuracy and calibration for the target-realism estimator. The team should also compare the model against a simple non-ML baseline (such as ranking by category popularity) to confirm that the data-driven approach actually provides uplift. If the model produces unrealistic recommendations or systematically excludes newer or smaller fundraisers, it must be adjusted before deployment.

**7. Model Deployment.** Once the model has been evaluated, it can be integrated into the FundRaise Platform through a new `RecommendController` that the donee's home-page Boundary invokes, keeping the ML logic out of the Entity classes and preserving the project's Boundary–Controller–Entity architecture. The Streamlit application sends the donee's context to the backend service, which returns a ranked list of recommended activities together with a short explanation (for example, "matches your interest in education"). The fundraiser-side target estimator can be surfaced during the create-activity flow as advisory feedback rather than a hard block, so that fundraisers stay in control of their own decisions.

**8. Model Monitoring.** After deployment, the model should be monitored to ensure that it continues to perform well in production. Each recommendation impression and the downstream click or donation should be logged, so the team can track live precision over time and detect drift — for example, a new fundraising category that the model has never seen. If recommendation quality drops or target estimates become inaccurate, the model should be retrained on newer data. Periodic retraining (for example monthly) together with a manual override switch help maintain quality and allow the recommender to be disabled if it misbehaves.

**9. Ethical Considerations.** Because the FundRaise Platform handles donor preferences, fundraiser target amounts, and eventually donation history, ethical issues must be considered throughout the model's lifecycle. Only data that is genuinely necessary for matching and target estimation should be collected, and donees and fundraisers should understand how their data is used. The recommender should be checked for fairness so that popular or well-funded campaigns do not crowd out smaller or newer fundraising activities, and the target-realism estimator should not discourage legitimate fundraisers from launching campaigns that serve niche causes. Sensitive data must be protected through access control consistent with the role-based and ownership rules described in Section 1.2.
