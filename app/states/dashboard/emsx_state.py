"""
EMSX State - Portfolio Dashboard Substate

Handles Bloomberg EMSX order management for the portfolio dashboard.

This follows Reflex best practices for state architecture:
- Focused responsibility (only EMSX orders)
- Service integration (uses EMSXService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Flat state structure with focused substates

Created as part of portfolio_dashboard_state.py restructuring.
"""

import reflex as rx
from app.services import EMSXService
from app.states.dashboard.types import EMSAOrderItem


class EMSXState(rx.State):
    """
    State management for Bloomberg EMSX orders and routes.

    Responsibilities:
    - Load active EMSX orders
    - Load order routes
    - Handle order status updates
    - Handle filtering and search for orders

    Best Practices Applied:
    1. Single Responsibility: Only handles EMSX data
    2. Service Integration: Uses EMSXService for order management
    3. Independent State: Doesn't inherit from other states
    4. Async Loading: Loads data asynchronously on demand
    """

    # Data storage
    orders: list[EMSAOrderItem] = []
    routes: list[EMSAOrderItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_view: str = "orders"  # "orders", "routes"
    selected_order_id: str = ""

    async def on_load(self):
        """
        Called when EMSX view loads.

        Best Practice: Use on_load for initial data fetching.
        """
        await self.load_emsx_data()

    async def load_emsx_data(self):
        """
        Load EMSX orders and routes from EMSXService.

        Service Integration Pattern:
        1. Set loading state
        2. Instantiate service
        3. Call service methods
        4. Update state with results
        5. Clear loading state
        """
        self.is_loading = True
        try:
            service = EMSXService()

            # Load EMSX orders and routes
            # TODO: Replace with real service calls when EMSXService is implemented
            self.orders = await service.get_orders()
            self.routes = await service.get_routes()

        except Exception as e:
            import logging

            logging.exception(f"Error loading EMSX data: {e}")
        finally:
            self.is_loading = False

    @rx.event
    async def refresh_orders(self):
        """Refresh EMSX orders."""
        await self.load_emsx_data()
        yield rx.toast("Orders refreshed", position="bottom-right")

    @rx.event
    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    @rx.event
    def set_current_view(self, view: str):
        """Switch between orders and routes view."""
        self.current_view = view

    @rx.event
    def select_order(self, order_id: str):
        """Select an order for detailed view."""
        self.selected_order_id = order_id

    @rx.var(cache=True)
    def filtered_orders(self) -> list[EMSAOrderItem]:
        """Filtered orders based on search query."""
        if not self.current_search_query:
            return self.orders

        query = self.current_search_query.lower()
        return [
            item
            for item in self.orders
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
            or query in item.get("broker", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_routes(self) -> list[EMSAOrderItem]:
        """Filtered routes based on search query."""
        if not self.current_search_query:
            return self.routes

        query = self.current_search_query.lower()
        return [
            item
            for item in self.routes
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]

    @rx.var
    def active_orders_count(self) -> int:
        """Count of active (not filled) orders."""
        # TODO: Implement proper status filtering
        return len(self.orders)

    @rx.var
    def total_filled_amount(self) -> float:
        """Total filled amount across all orders."""
        # TODO: Implement proper amount aggregation
        return 0.0
