"""
Risk State - Module-specific state for Risk data

Composes all Risk mixins to provide unified interface.
Following the PnL pattern with mixin-per-tab architecture.
"""

import reflex as rx
from app.states.risk.mixins.delta_change_mixin import DeltaChangeMixin
from app.states.risk.mixins.risk_measures_mixin import RiskMeasuresMixin
from app.states.risk.mixins.risk_inputs_mixin import RiskInputsMixin


class RiskState(
    DeltaChangeMixin,
    RiskMeasuresMixin,
    RiskInputsMixin,
    rx.State,
):
    """
    Main Risk module state.
    Inherits from all Risk tab mixins to provide unified interface.
    """

    # Module-level state
    current_tab: str = "delta"  # "delta", "measures", "inputs"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Risk view loads."""
        await self.load_risk_data()

    async def load_risk_data(self):
        """Load all risk data from RiskService (backward compatible).
        
        This loads data for all tabs - used by on_load handlers in routes.
        """
        await self.load_delta_change_data()
        await self.load_risk_measures_data()
        await self.load_risk_inputs_data()

    async def load_risk_module_data(self):
        """Load data for the active tab only."""
        if self.current_tab == "delta":
            await self.load_delta_change_data()
        elif self.current_tab == "measures":
            await self.load_risk_measures_data()
        elif self.current_tab == "inputs":
            await self.load_risk_inputs_data()

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

