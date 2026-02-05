"""
EMSX State - Module-specific state for EMSX/Orders data

Handles all EMSX/orders-related data:
- EMSX Orders (via EMSAOrderMixin)
- EMSX Routes (via EMSARouteMixin)

Architecture follows the mixin pattern for per-tab state management.
"""

import reflex as rx

from app.states.emsx.mixins import EMSAOrderMixin, EMSARouteMixin


class EMSXState(EMSAOrderMixin, EMSARouteMixin, rx.State):
    """
    Main EMSX module state.
    Inherits from all EMSX subtab mixins to provide unified interface.

    Each mixin handles:
    - Data loading and storage
    - Auto-refresh (ticking) pattern
    - Force refresh with loading overlay
    - Filtering based on search query
    """

    # Module-level UI state
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
        # Start auto-refresh if enabled
        if self.emsa_order_auto_refresh:
            return type(self).start_emsa_order_auto_refresh
        if self.emsa_route_auto_refresh:
            return type(self).start_emsa_route_auto_refresh

    async def load_emsa_data(self):
        """Load all EMSA data (orders and routes) from both mixins."""
        await self.load_emsa_orders()
        await self.load_emsa_routes()

    # =========================================================================
    # UI State Methods
    # =========================================================================

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
