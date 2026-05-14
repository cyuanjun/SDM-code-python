"""CreateProfileController <<Controller>> — Sprint 1 US-1.

Pure delegator per the project architecture rule (CLAUDE.md). Takes the
Boundary's input, calls UserProfile.create_profile, returns the result.
"""
from __future__ import annotations

from entity.user_profile import UserProfile


class CreateProfileController:
    def create_profile(self, role: str, description: str) -> UserProfile:
        return UserProfile.create_profile(role=role, description=description)
