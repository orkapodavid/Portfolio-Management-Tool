import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import (
    PortfolioDashboardState,
    NotificationItem,
)


def get_paginated_alerts(
    alerts: list[NotificationItem], current_page: int, items_per_page: int
) -> tuple[list[NotificationItem], int, int]:
    """Helper to slice alerts and calculate total pages."""
    total_items = len(alerts)
    if total_items == 0:
        return ([], 1, 1)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    safe_page = max(1, min(current_page, total_pages))
    start_idx = (safe_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    return (alerts[start_idx:end_idx], safe_page, total_pages)


class NotificationPaginationState(rx.State):
    current_page: int = 1
    items_per_page: int = 6

    @rx.var
    async def total_pages(self) -> int:
        dashboard = await self.get_state(PortfolioDashboardState)
        total_items = len(dashboard.notifications)
        if total_items == 0:
            return 1
        return (total_items + self.items_per_page - 1) // self.items_per_page

    @rx.var
    async def paginated_notifications(self) -> list[NotificationItem]:
        dashboard = await self.get_state(PortfolioDashboardState)
        sliced_data, _, _ = get_paginated_alerts(
            dashboard.notifications, self.current_page, self.items_per_page
        )
        return sliced_data

    @rx.event
    async def next_page(self):
        tp = await self.total_pages
        if self.current_page < tp:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def reset_pagination(self):
        self.current_page = 1