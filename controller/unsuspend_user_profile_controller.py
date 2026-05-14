"""UnsuspendUserProfileController — Exception A (UX). Pure delegator.

Mirror of SuspendUserProfileController. Not on any diagram; logged in
docs/diagram_typos.md as a UX toggle deviation.
"""
from __future__ import annotations

from entity.user_profile import UserProfile


class UnsuspendUserProfileController:
    def unsuspend_user_profile(self, profile_id: str) -> bool:
        return UserProfile.unsuspend_user_profile(profile_id)
