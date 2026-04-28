"""UpdateUserProfileController <<Controller>> — pure delegator, see Sprint 2 diagram US-3."""
from __future__ import annotations

from entity.user_profile import UserProfile


class UpdateUserProfileController:
    def update_user_profile(
        self, profile_id: str, updated_profile: UserProfile
    ) -> bool:
        return UserProfile.update_user_profile(profile_id, updated_profile)
