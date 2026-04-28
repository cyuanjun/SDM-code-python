"""ViewProfilesController <<Controller>> — pure delegator.

Note: this controller is not in any Sprint 1 sequence diagram. It exists to
populate the profile dropdown on CreateAccountPage. It anticipates Sprint 2
work on US-2 (view user profile) and US-5 (search user profiles), and the
class diagram will need to be updated to reflect view_all_profiles().
"""
from __future__ import annotations

from entity.user_profile import UserProfile


class ViewProfilesController:
    def view_all_profiles(self) -> list[UserProfile]:
        return UserProfile.view_all_profiles()
