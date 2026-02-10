"""
User Service for Portfolio Management Tool.

Delegates all data methods to pmt_core.services.user.UserService.
"""

import logging
from typing import Optional

from pmt_core.services.user import UserService as CoreUserService

logger = logging.getLogger(__name__)


class UserService:
    """
    Service for user management.
    Delegates to pmt_core UserService for data.
    """

    def __init__(self):
        self.core_service = CoreUserService()

    async def get_user_profile(self, user_id: Optional[str] = None) -> dict:
        """Get user profile. Delegates to core."""
        return await self.core_service.get_user_profile(user_id)

    async def update_user_profile(
        self, user_id: Optional[str] = None, **kwargs
    ) -> dict:
        """Update user profile. Delegates to core."""
        return await self.core_service.update_user_profile(user_id, **kwargs)

    async def get_user_settings(self, user_id: Optional[str] = None) -> dict:
        """Get user settings. Delegates to core."""
        return await self.core_service.get_user_settings(user_id)

    async def update_user_settings(
        self, user_id: Optional[str] = None, **settings
    ) -> dict:
        """Update user settings. Delegates to core."""
        return await self.core_service.update_user_settings(user_id, **settings)

    async def get_user_portfolios(self, user_id: Optional[str] = None) -> list[dict]:
        """Get user portfolios. Delegates to core."""
        return await self.core_service.get_user_portfolios(user_id)

    async def create_portfolio(
        self, name: str, description: str = "", user_id: Optional[str] = None
    ) -> dict:
        """Create a portfolio. Delegates to core."""
        return await self.core_service.create_portfolio(name, description, user_id)

    async def get_goals(self, user_id: Optional[str] = None) -> list[dict]:
        """Get financial goals. Delegates to core."""
        return await self.core_service.get_goals(user_id)

    async def save_goal(
        self, goal_data: dict, user_id: Optional[str] = None
    ) -> dict:
        """Save a goal. Delegates to core."""
        return await self.core_service.save_goal(goal_data, user_id)

    async def delete_goal(
        self, goal_id: str, user_id: Optional[str] = None
    ) -> bool:
        """Delete a goal. Delegates to core."""
        return await self.core_service.delete_goal(goal_id, user_id)
