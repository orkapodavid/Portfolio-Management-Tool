"""
P&L State - Portfolio Dashboard Substate

Handles all P&L (Profit & Loss) related data and operations for the portfolio dashboard.

This is an example of proper Reflex state architecture following best practices:
- Focused responsibility (only P&L data)
- Service integration (uses PnLService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Flat state structure with focused substates

Created as part of portfolio_dashboard_state.py restructuring.
"""

import reflex as rx
from app.services import PnLService
from app.states.dashboard.types import (
    PnLChangeItem,
    PnLSummaryItem,
    PnLCurrencyItem,
)


class PnLState(rx.State):
    """
    State management for P&L (Profit & Loss) data.

    Responsibilities:
    - Load P&L change data (YTD, 1D, 1W, 1M)
    - Load P&L summary data
    - Load currency P&L data
    - Handle filtering and search for P&L views

    Best Practices Applied:
    1. Single Responsibility: Only handles P&L data
    2. Service Integration: Uses PnLService for data access
    3. Independent State: Doesn't inherit from other states
    4. Async Loading: Loads data asynchronously on demand
    """

    # Data storage
    pnl_change_list: list[PnLChangeItem] = []
    pnl_summary_list: list[PnLSummaryItem] = []
    pnl_currency_list: list[PnLCurrencyItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "changes"  # "changes", "summary", "currency"

    async def on_load(self):
        """
        Called when P&L view loads.

        Best Practice: Use on_load for initial data fetching.
        This ensures data is loaded only when the user navigates to this view.
        """
        await self.load_pnl_data()

    async def load_pnl_data(self):
        """
        Load all P&L data from PnLService.

        Service Integration Pattern:
        1. Set loading state
        2. Instantiate service
        3. Call service methods
        4. Update state with results
        5. Clear loading state
        """
        self.is_loading = True
        try:
            service = PnLService()

            # Load all P&L data types
            # TODO: These currently return mock data - replace with real DB queries
            self.pnl_change_list = await service.get_pnl_changes()
            self.pnl_summary_list = await service.get_pnl_summary()
            self.pnl_currency_list = await service.get_currency_pnl()

        except Exception as e:
            import logging

            logging.exception(f"Error loading P&L data: {e}")
            # Keep empty lists on error
        finally:
            self.is_loading = False

    @rx.event
    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    @rx.event
    def set_current_tab(self, tab: str):
        """Switch between P&L tabs."""
        self.current_tab = tab

    @rx.var(cache=True)
    def filtered_pnl_changes(self) -> list[PnLChangeItem]:
        """
        Filtered P&L changes based on search query.

        Computed Var Best Practice:
        - Use cache=True for expensive computations
        - Place computed vars in leaf states (not parent states)
        - Keep computation logic simple
        """
        if not self.current_search_query:
            return self.pnl_change_list

        query = self.current_search_query.lower()
        return [
            item
            for item in self.pnl_change_list
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_pnl_summary(self) -> list[PnLSummaryItem]:
        """Filtered P&L summary based on search query."""
        if not self.current_search_query:
            return self.pnl_summary_list

        query = self.current_search_query.lower()
        return [
            item
            for item in self.pnl_summary_list
            if query in item.get("underlying", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_pnl_currency(self) -> list[PnLCurrencyItem]:
        """Filtered currency P&L based on search query."""
        if not self.current_search_query:
            return self.pnl_currency_list

        query = self.current_search_query.lower()
        return [
            item
            for item in self.pnl_currency_list
            if query in item.get("currency", "").lower()
        ]

    @rx.var
    def total_ytd_pnl(self) -> float:
        """
        Calculate total YTD P&L across all positions.

        Note: This is a simplified example. Real implementation would
        parse the string values and sum them properly.
        """
        # TODO: Implement proper YTD calculation
        return 0.0


# Example of how to use this state in a component:
"""
from app.states.dashboard.pnl_state import PnLState

def pnl_view():
    return rx.cond(
        PnLState.is_loading,
        rx.spinner(),
        rx.vstack(
            # Search input
            rx.input(
                value=PnLState.current_search_query,
                on_change=PnLState.set_search_query,
                placeholder="Search P&L..."
            ),
            
            # Tab selector
            rx.tabs(
                rx.tab("Changes", on_click=lambda: PnLState.set_current_tab("changes")),
                rx.tab("Summary", on_click=lambda: PnLState.set_current_tab("summary")),
                rx.tab("Currency", on_click=lambda: PnLState.set_current_tab("currency")),
            ),
            
            # Data table (example for changes tab)
            rx.cond(
                PnLState.current_tab == "changes",
                rx.data_table(data=PnLState.filtered_pnl_changes),
                rx.cond(
                    PnLState.current_tab == "summary",
                    rx.data_table(data=PnLState.filtered_pnl_summary),
                    rx.data_table(data=PnLState.filtered_pnl_currency)
                )
            )
        )
    )
"""
