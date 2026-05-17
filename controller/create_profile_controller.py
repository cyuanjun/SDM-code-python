"""CreateProfileController <<Controller>> — Sprint 1 US-1.

Pure delegator per the project architecture rule (CLAUDE.md). Takes the
Boundary's input, calls UserProfile.create_profile, returns the result
(or None on duplicate-role conflict, per the UNIQUE constraint on role).
"""
from __future__ import annotations

from typing import Optional

from entity.user_profile import UserProfile


class CreateProfileController:
    def create_profile(
        self, role: str, description: str
    ) -> Optional[UserProfile]:
        return UserProfile.create_profile(role=role, description=description)
