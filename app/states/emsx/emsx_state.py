"""
EMSX State - Module-specific state for EMSX/Orders data

Handles all EMSX/orders-related data:
- EMSX Orders
- EMSX Routes
"""

import reflex as rx
from app.services import EMSXService
from app.states.types import EMSAOrderItem


class EMSXState(rx.State):
    """
    State management for EMSX/orders data.
    """

    # EMSA data lists
    emsa_orders: list[EMSAOrderItem] = []
    emsa_routes: list[dict] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "orders"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when EMSX view loads."""
        await self.load_emsa_data()

    async def load_emsa_data(self):
        """Load all EMSA data from EMSXService."""
        self.is_loading = True
        try:
            service = EMSXService()
            self.emsa_orders = await service.get_emsx_orders()
            self.emsa_routes = await service.get_emsx_routes()
        except Exception as e:
            import logging

            logging.exception(f"Error loading EMSX data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    def set_current_tab(self, tab: str):
        """Switch between EMSX tabs."""
        self.current_tab = tab

    def toggle_sort(self, column: str):
        """Toggle sort direction for a column."""
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"

    def set_selected_row(self, row_id: int):
        """Set selected row ID."""
        self.selected_row = row_id

    @rx.var(cache=True)
    def filtered_emsa_orders(self) -> list[EMSAOrderItem]:
        """Filtered EMSX orders based on search query."""
        if not self.current_search_query:
            return self.emsa_orders

        query = self.current_search_query.lower()
        return [
            item
            for item in self.emsa_orders
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
            or query in item.get("broker", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_emsa_routes(self) -> list[dict]:
        """Filtered EMSX routes based on search query."""
        if not self.current_search_query:
            return self.emsa_routes

        query = self.current_search_query.lower()
        # Routes likely share similar structure to orders for now (mock data often does)
        # Checking keys to be safe
        return [
            item
            for item in self.emsa_routes
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
            or query in item.get("broker", "").lower()
        ]
