"""
Overview Mixin — State mixin for the Dashboard Overview tab.

Loads user data and recent activity from UserService.
"""

import reflex as rx
from starter_app.services import UserService
from starter_app.states.dashboard.types import UserItem, ActivityItem

_user_service = UserService()


class OverviewMixin(rx.State, mixin=True):
    """Mixin providing Dashboard Overview data state."""

    # Data state
    users: list[UserItem] = []
    recent_activity: list[ActivityItem] = []
    is_loading_overview: bool = False
    overview_error: str = ""

    # Stats (computed from users)
    total_users: int = 0
    active_users: int = 0

    # Search / filter
    user_search: str = ""

    @rx.event
    def load_overview_data(self):
        """Load overview data from UserService."""
        self.is_loading_overview = True
        self.overview_error = ""
        try:
            self.users = _user_service.get_users()
            self.recent_activity = _user_service.get_recent_activity()
            self.total_users = _user_service.get_total_count()
            self.active_users = _user_service.get_active_count()
        except Exception as e:
            self.overview_error = str(e)
        finally:
            self.is_loading_overview = False

    @rx.event
    def set_user_search(self, query: str):
        """Set user search filter."""
        self.user_search = query

    @rx.var(cache=True)
    def filtered_users(self) -> list[UserItem]:
        """Filter users by search query."""
        if not self.user_search:
            return self.users
        query = self.user_search.lower()
        return [
            u for u in self.users
            if query in u.get("name", "").lower()
            or query in u.get("email", "").lower()
        ]

    @rx.var(cache=True)
    def active_user_pct(self) -> str:
        """Percentage of active users."""
        if self.total_users == 0:
            return "0%"
        return f"{(self.active_users / self.total_users * 100):.1f}%"
