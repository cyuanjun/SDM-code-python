"""ViewProfilesController <<Controller>> — Sprint 1 Exception A.

Pure delegator. Wraps UserProfile.view_all_profiles so the boundary
CreateAccountPage can populate its profile dropdown without importing
the entity directly. Logged in docs/todo.md as an Exception A diagram
update owed before final marking.
"""
from __future__ import annotations

from entity.user_profile import UserProfile


class ViewProfilesController:
    def view_all_profiles(self) -> list[UserProfile]:
        return UserProfile.view_all_profiles()
