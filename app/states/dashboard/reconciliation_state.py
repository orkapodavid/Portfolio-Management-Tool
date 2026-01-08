"""
Reconciliation State - Portfolio Dashboard Substate

Handles all reconciliation and settlement data for the portfolio dashboard.

This follows Reflex best practices for state architecture:
- Focused responsibility (only reconciliation data)
- Service integration (uses DatabaseService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Flat state structure with focused substates

Created as part of portfolio_dashboard_state.py restructuring.
"""

import reflex as rx
from app.services import DatabaseService


# Note: TypedDict definitions for reconciliation items would go in types.py
# For now, using dict type until types are migrated


class ReconciliationState(rx.State):
    """
    State management for reconciliation and settlement data.

    Responsibilities:
    - Load PPS reconciliation data
    - Load settlement reconciliation data
    - Load failed trade data
    - Handle filtering and search for reconciliation views

    Best Practices Applied:
    1. Single Responsibility: Only handles reconciliation data
    2. Service Integration: Uses DatabaseService for data access
    3. Independent State: Doesn't inherit from other states
    4. Async Loading: Loads data asynchronously on demand
    """

    # Data storage
    pps_recon: list[dict] = []  # PPS reconciliation data
    settlement_recon: list[dict] = []  # Settlement reconciliation data
    failed_trades: list[dict] = []  # Failed trade data

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "pps"  # "pps", "settlement", "failed"
    show_reconciled_only: bool = False

    async def on_load(self):
        """
        Called when Reconciliation view loads.

        Best Practice: Use on_load for initial data fetching.
        """
        await self.load_reconciliation_data()

    async def load_reconciliation_data(self):
        """
        Load reconciliation data from DatabaseService.

        Service Integration Pattern:
        1. Set loading state
        2. Instantiate service
        3. Call service methods
        4. Update state with results
        5. Clear loading state
        """
        self.is_loading = True
        try:
            service = DatabaseService()

            # Load reconciliation data from database
            # TODO: Implement actual database queries
            # self.pps_recon = await service.execute_query(
            #     "SELECT * FROM pps_reconciliation WHERE trade_date = CURRENT_DATE"
            # )
            # self.settlement_recon = await service.execute_query(
            #     "SELECT * FROM settlement_reconciliation WHERE status != 'settled'"
            # )
            # self.failed_trades = await service.execute_query(
            #     "SELECT * FROM failed_trades WHERE status = 'failed'"
            # )

            # For now, using empty lists (replaced by real queries above)
            self.pps_recon = []
            self.settlement_recon = []
            self.failed_trades = []

        except Exception as e:
            import logging

            logging.exception(f"Error loading reconciliation data: {e}")
        finally:
            self.is_loading = False

    @rx.event
    async def refresh_reconciliation(self):
        """Refresh reconciliation data."""
        await self.load_reconciliation_data()
        yield rx.toast("Reconciliation data refreshed", position="bottom-right")

    @rx.event
    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    @rx.event
    def set_current_tab(self, tab: str):
        """Switch between reconciliation tabs."""
        self.current_tab = tab

    @rx.event
    def toggle_reconciled_filter(self):
        """Toggle filter to show only reconciled/unreconciled items."""
        self.show_reconciled_only = not self.show_reconciled_only

    @rx.var(cache=True)
    def filtered_pps_recon(self) -> list[dict]:
        """Filtered PPS reconciliation based on search query."""
        data = self.pps_recon

        # Apply reconciled filter if enabled
        if self.show_reconciled_only:
            data = [item for item in data if item.get("is_reconciled", False)]

        # Apply search query
        if not self.current_search_query:
            return data

        query = self.current_search_query.lower()
        return [
            item
            for item in data
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_settlement_recon(self) -> list[dict]:
        """Filtered settlement reconciliation based on search query."""
        data = self.settlement_recon

        if not self.current_search_query:
            return data

        query = self.current_search_query.lower()
        return [
            item
            for item in data
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_failed_trades(self) -> list[dict]:
        """Filtered failed trades based on search query."""
        if not self.current_search_query:
            return self.failed_trades

        query = self.current_search_query.lower()
        return [
            item
            for item in self.failed_trades
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
            or query in item.get("broker", "").lower()
        ]

    @rx.var
    def unreconciled_count(self) -> int:
        """Count of unreconciled items."""
        # TODO: Implement proper reconciliation status check
        return len(self.pps_recon) + len(self.settlement_recon)

    @rx.var
    def failed_trades_count(self) -> int:
        """Count of failed trades."""
        return len(self.failed_trades)
