"""ViewProfilesController <<Controller>>."""
from __future__ import annotations

from entity.user_profile import UserProfile


class ViewProfilesController:
    def view_all_profiles(self) -> list[UserProfile]:
        return UserProfile.view_all_profiles()
