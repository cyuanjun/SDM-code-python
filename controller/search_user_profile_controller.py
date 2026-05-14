"""SearchUserProfileController <<Controller>> — Sprint 3 US-5.

Pure delegator.
"""
from __future__ import annotations

from entity.user_profile import UserProfile


class SearchUserProfileController:
    def search_user_profile(self, search_criteria: str) -> list[UserProfile]:
        return UserProfile.search_user_profile(search_criteria)
