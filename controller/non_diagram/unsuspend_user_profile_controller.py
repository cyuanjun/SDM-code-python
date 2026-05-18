"""UnsuspendUserProfileController <<Controller>>."""
from __future__ import annotations

from entity.user_profile import UserProfile


class UnsuspendUserProfileController:
    def unsuspend_user_profile(self, profile_id: str) -> bool:
        return UserProfile.unsuspend_user_profile(profile_id)
