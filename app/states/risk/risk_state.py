"""
Risk State - Module-specific state for Risk data

Handles all risk-related data and calculations.

This follows Reflex best practices for state architecture:
- Focused responsibility (only risk metrics)
- Service integration (uses RiskService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)
"""

import reflex as rx
from app.services import RiskService
from app.states.risk.types import (
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
    """

    # Data storage
    delta_changes: list[DeltaChangeItem] = []
    risk_measures: list[RiskMeasureItem] = []
    risk_inputs: list[RiskInputItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "delta"  # "delta", "measures", "inputs"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Risk view loads."""
        await self.load_risk_data()

    async def load_risk_data(self):
        """Load all risk data from RiskService."""
        self.is_loading = True
        try:
            service = RiskService()
            self.delta_changes = await service.get_delta_changes()
            self.risk_measures = await service.get_risk_measures()
            self.risk_inputs = await service.get_risk_inputs()
        except Exception as e:
            import logging

            logging.exception(f"Error loading risk data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    def set_current_tab(self, tab: str):
        """Switch between risk tabs."""
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
