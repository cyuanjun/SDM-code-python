"""CreateProfileController <<Controller>> — pure delegator, see Sprint 1 diagram US-1."""
from __future__ import annotations

from typing import Optional

from entity.user_profile import UserProfile


class CreateProfileController:
    def create_profile(self, role: str, description: str) -> Optional[UserProfile]:
        return UserProfile.create_profile(role, description)
