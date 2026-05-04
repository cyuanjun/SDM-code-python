"""DeleteUserProfileController <<Controller>> — pure delegator, US-4."""
from __future__ import annotations

from entity.user_profile import UserProfile


class DeleteUserProfileController:
    def delete_user_profile(self, profile_id: str) -> bool:
        return UserProfile.delete_user_profile(profile_id)
