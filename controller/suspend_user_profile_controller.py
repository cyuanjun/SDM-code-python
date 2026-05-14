"""SuspendUserProfileController <<Controller>> — Sprint 3 US-4.

Pure delegator. Forwards profileId to UserProfile.suspend_user_profile.
"""
from __future__ import annotations

from entity.user_profile import UserProfile


class SuspendUserProfileController:
    def suspend_user_profile(self, profile_id: str) -> bool:
        return UserProfile.suspend_user_profile(profile_id)
