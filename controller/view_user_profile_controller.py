"""ViewUserProfileController <<Controller>> — Sprint 2 US-2.

Pure delegator. Forwards a profileId to UserProfile.view_user_profile.
"""
from __future__ import annotations

from typing import Optional

from entity.user_profile import UserProfile


class ViewUserProfileController:
    def view_user_profile(self, profile_id: str) -> Optional[UserProfile]:
        return UserProfile.view_user_profile(profile_id)
