"""
Risk State - Portfolio Dashboard Substate

Handles all risk-related data and calculations for the portfolio dashboard.

This follows Reflex best practices for state architecture:
- Focused responsibility (only risk metrics)
- Service integration (uses RiskService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Flat state structure with focused substates

Created as part of portfolio_dashboard_state.py restructuring.
"""

import reflex as rx
from app.services import RiskService
from app.states.dashboard.types import (
    DeltaChangeItem,
    RiskMeasureItem,
    RiskInputItem,
)


class RiskState(rx.State):
    """
    State management for risk metrics and calculations.

    Responsibilities:
    - Load delta change data
    - Load risk measures (Greeks, sensitivities)
    - Load risk input parameters
    - Handle filtering and search for risk views

    Best Practices Applied:
    1. Single Responsibility: Only handles risk data
    2. Service Integration: Uses RiskService for calculations
    3. Independent State: Doesn't inherit from other states
    4. Async Loading: Loads data asynchronously on demand
    """

    # Data storage
    delta_changes: list[DeltaChangeItem] = []
    risk_measures: list[RiskMeasureItem] = []
    risk_inputs: list[RiskInputItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "delta"  # "delta", "measures", "inputs"

    async def on_load(self):
        """
        Called when Risk view loads.

        Best Practice: Use on_load for initial data fetching.
        """
        await self.load_risk_data()

    async def load_risk_data(self):
        """
        Load all risk data from RiskService.

        Service Integration Pattern:
        1. Set loading state
        2. Instantiate service
        3. Call service methods
        4. Update state with results
        5. Clear loading state
        """
        self.is_loading = True
        try:
            service = RiskService()

            # Load all risk data types
            # TODO: Replace with real service calls when RiskService is implemented
            self.delta_changes = await service.get_delta_changes()
            self.risk_measures = await service.get_risk_measures()
            self.risk_inputs = await service.get_risk_inputs()

        except Exception as e:
            import logging

            logging.exception(f"Error loading risk data: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    @rx.event
    def set_current_tab(self, tab: str):
        """Switch between risk tabs."""
        self.current_tab = tab

    @rx.var(cache=True)
    def filtered_delta_changes(self) -> list[DeltaChangeItem]:
        """Filtered delta changes based on search query."""
        if not self.current_search_query:
            return self.delta_changes

        query = self.current_search_query.lower()
        return [
            item
            for item in self.delta_changes
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_risk_measures(self) -> list[RiskMeasureItem]:
        """Filtered risk measures based on search query."""
        if not self.current_search_query:
            return self.risk_measures

        query = self.current_search_query.lower()
        return [
            item
            for item in self.risk_measures
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_risk_inputs(self) -> list[RiskInputItem]:
        """Filtered risk inputs based on search query."""
        if not self.current_search_query:
            return self.risk_inputs

        query = self.current_search_query.lower()
        return [
            item
            for item in self.risk_inputs
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]

    @rx.var
    def total_delta(self) -> float:
        """
        Calculate total portfolio delta.

        Note: Simplified example - real implementation would parse values properly.
        """
        # TODO: Implement proper delta aggregation
        return 0.0
