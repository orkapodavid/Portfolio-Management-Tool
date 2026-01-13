"""
Instrument State - Module-specific state for Instruments data

Handles all instrument-related data:
- Ticker Data (Reference Data)
- Stock Screener
- Special Terms
- Instrument Data
- Instrument Terms
"""

import reflex as rx
from app.services import DatabaseService
from app.states.types import (
    TickerDataItem,
    StockScreenerItem,
    SpecialTermItem,
    InstrumentDataItem,
    InstrumentTermItem,
)


class InstrumentState(rx.State):
    """
    State management for instruments data.
    """

    # Instruments data lists
    ticker_data: list[TickerDataItem] = []
    stock_screener: list[StockScreenerItem] = []
    special_terms: list[SpecialTermItem] = []
    instrument_data: list[InstrumentDataItem] = []
    instrument_terms: list[InstrumentTermItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "ticker"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Instruments view loads."""
        await self.load_instruments_data()

    async def load_instruments_data(self):
        """Load all instruments data from DatabaseService."""
        self.is_loading = True
        try:
            service = DatabaseService()
            self.ticker_data = await service.get_ticker_data()
            self.stock_screener = await service.get_stock_screener()
            self.special_terms = await service.get_special_terms()
            self.instrument_data = await service.get_instrument_data()
            self.instrument_terms = await service.get_instrument_terms()
        except Exception as e:
            import logging

            logging.exception(f"Error loading instruments data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

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

    @rx.var(cache=True)
    def filtered_ticker_data(self) -> list[TickerDataItem]:
        """Filtered ticker data based on search query."""
        if not self.current_search_query:
            return self.ticker_data

        query = self.current_search_query.lower()
        return [
            item
            for item in self.ticker_data
            if query in item.get("ticker", "").lower()
            or query in item.get("company", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_stock_screener(self) -> list[StockScreenerItem]:
        """Filtered stock screener based on search query."""
        if not self.current_search_query:
            return self.stock_screener

        query = self.current_search_query.lower()
        return [
            item
            for item in self.stock_screener
            if query in item.get("ticker", "").lower()
            or query in item.get("company", "").lower()
            or query in item.get("industry", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_special_terms(self) -> list[SpecialTermItem]:
        """Filtered special terms based on search query."""
        if not self.current_search_query:
            return self.special_terms

        query = self.current_search_query.lower()
        return [
            item
            for item in self.special_terms
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
            or query in item.get("deal_num", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_instrument_data(self) -> list[InstrumentDataItem]:
        """Filtered instrument data based on search query."""
        if not self.current_search_query:
            return self.instrument_data

        query = self.current_search_query.lower()
        return [
            item
            for item in self.instrument_data
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
            or query in item.get("underlying", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_instrument_terms(self) -> list[InstrumentTermItem]:
        """Filtered instrument terms based on search query."""
        if not self.current_search_query:
            return self.instrument_terms

        query = self.current_search_query.lower()
        return [
            item
            for item in self.instrument_terms
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
            or query in item.get("underlying", "").lower()
        ]
