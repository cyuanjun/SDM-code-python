"""SearchUserProfileController <<Controller>> — pure delegator, US-5."""
from __future__ import annotations

from entity.user_profile import UserProfile


class SearchUserProfileController:
    def submit_search_criteria(self, search_criteria: str) -> list[UserProfile]:
        return UserProfile.submit_search_criteria(search_criteria)
