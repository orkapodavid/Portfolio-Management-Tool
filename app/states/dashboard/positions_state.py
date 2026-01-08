"""
Positions State - Portfolio Dashboard Substate

Handles all position-related data and operations for the portfolio dashboard.

This follows Reflex best practices for state architecture:
- Focused responsibility (only position data)
- Service integration (uses PositionService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Flat state structure with focused substates

Created as part of portfolio_dashboard_state.py restructuring.
"""

import reflex as rx
from app.services import PositionService
from app.states.dashboard.types import (
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
)


class PositionsState(rx.State):
    """
    State management for position data across all asset types.

    Responsibilities:
    - Load stock positions
    - Load warrant positions
    - Load bond positions
    - Handle filtering and search for position views

    Best Practices Applied:
    1. Single Responsibility: Only handles position data
    2. Service Integration: Uses PositionService for data access
    3. Independent State: Doesn't inherit from other states
    4. Async Loading: Loads data asynchronously on demand
    """

    # Data storage
    stock_positions: list[StockPositionItem] = []
    warrant_positions: list[WarrantPositionItem] = []
    bond_positions: list[BondPositionItem] = []
    all_positions: list[PositionItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_position_type: str = "all"  # "all", "stocks", "warrants", "bonds"

    async def on_load(self):
        """
        Called when Positions view loads.

        Best Practice: Use on_load for initial data fetching.
        """
        await self.load_positions()

    async def load_positions(self):
        """
        Load all position data from PositionService.

        Service Integration Pattern:
        1. Set loading state
        2. Instantiate service
        3. Call service methods
        4. Update state with results
        5. Clear loading state
        """
        self.is_loading = True
        try:
            service = PositionService()

            # Load all position types
            # TODO: Replace with real service calls when PositionService is implemented
            self.stock_positions = await service.get_stock_positions()
            self.warrant_positions = await service.get_warrant_positions()
            self.bond_positions = await service.get_bond_positions()
            # self.all_positions = await service.get_all_positions()

        except Exception as e:
            import logging

            logging.exception(f"Error loading positions: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    @rx.event
    def set_position_type(self, position_type: str):
        """Switch between position types."""
        self.current_position_type = position_type

    @rx.var(cache=True)
    def filtered_stock_positions(self) -> list[StockPositionItem]:
        """Filtered stock positions based on search query."""
        if not self.current_search_query:
            return self.stock_positions

        query = self.current_search_query.lower()
        return [
            item
            for item in self.stock_positions
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_warrant_positions(self) -> list[WarrantPositionItem]:
        """Filtered warrant positions based on search query."""
        if not self.current_search_query:
            return self.warrant_positions

        query = self.current_search_query.lower()
        return [
            item
            for item in self.warrant_positions
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_bond_positions(self) -> list[BondPositionItem]:
        """Filtered bond positions based on search query."""
        if not self.current_search_query:
            return self.bond_positions

        query = self.current_search_query.lower()
        return [
            item
            for item in self.bond_positions
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var
    def total_positions_count(self) -> int:
        """Total number of positions across all types."""
        return (
            len(self.stock_positions)
            + len(self.warrant_positions)
            + len(self.bond_positions)
        )
