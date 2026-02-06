"""
Instrument State - Module-specific state for Instruments data

Composes all instrument-related tab mixins:
- Ticker Data (Reference Data)
- Stock Screener
- Special Terms
- Instrument Data
- Instrument Terms
"""

import reflex as rx
from app.states.instruments.mixins import (
    TickerDataMixin,
    StockScreenerMixin,
    SpecialTermsMixin,
    InstrumentDataMixin,
    InstrumentTermsMixin,
)


class InstrumentState(
    TickerDataMixin,
    StockScreenerMixin,
    SpecialTermsMixin,
    InstrumentDataMixin,
    InstrumentTermsMixin,
    rx.State,
):
    """
    State management for instruments data.
    Composes all instrument tab mixins for unified interface.
    """

    # UI state
    current_tab: str = "ticker"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Instruments view loads."""
        await self.load_instruments_data()

    async def load_instruments_data(self):
        """Load all instruments data from mixins."""
        await self.load_ticker_data()
        await self.load_stock_screener_data()
        await self.load_special_terms_data()
        await self.load_instrument_data()
        await self.load_instrument_terms_data()

    # =========================================================================
    # UI State Methods
    # =========================================================================

    def set_current_tab(self, tab: str):
        """Switch between instruments tabs."""
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
