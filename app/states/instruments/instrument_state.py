"""
Instrument State - Module-specific state for Instruments data

Handles all instrument-related data:
- Ticker Data (Reference Data)
- Stock Screener
- Special Terms
- Instrument Data
- Instrument Terms
"""

import asyncio
from datetime import datetime

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

    # Ticker Data loading state
    is_loading_ticker_data: bool = False
    ticker_data_last_updated: str = "—"

    # Stock Screener loading state
    is_loading_stock_screener: bool = False
    stock_screener_last_updated: str = "—"

    # Special Terms loading state
    is_loading_special_terms: bool = False
    special_terms_last_updated: str = "—"

    # Instrument Data loading state
    is_loading_instrument_data: bool = False
    instrument_data_last_updated: str = "—"

    # Instrument Terms loading state
    is_loading_instrument_terms: bool = False
    instrument_terms_last_updated: str = "—"

    # UI state
    is_loading: bool = False
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            service = DatabaseService()
            self.ticker_data = await service.get_ticker_data()
            self.ticker_data_last_updated = timestamp

            self.stock_screener = await service.get_stock_screener()
            self.stock_screener_last_updated = timestamp

            self.special_terms = await service.get_special_terms()
            self.special_terms_last_updated = timestamp

            self.instrument_data = await service.get_instrument_data()
            self.instrument_data_last_updated = timestamp

            self.instrument_terms = await service.get_instrument_terms()
            self.instrument_terms_last_updated = timestamp
        except Exception as e:
            import logging

            logging.exception(f"Error loading instruments data: {e}")
        finally:
            self.is_loading = False

    # =========================================================================
    # Ticker Data
    # =========================================================================

    async def force_refresh_ticker_data(self):
        """Force refresh ticker data with loading overlay."""
        if self.is_loading_ticker_data:
            return
        self.is_loading_ticker_data = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.ticker_data = await service.get_ticker_data()
            self.ticker_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing ticker data: {e}")
        finally:
            self.is_loading_ticker_data = False

    # =========================================================================
    # Stock Screener
    # =========================================================================

    async def force_refresh_stock_screener(self):
        """Force refresh stock screener data with loading overlay."""
        if self.is_loading_stock_screener:
            return
        self.is_loading_stock_screener = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.stock_screener = await service.get_stock_screener()
            self.stock_screener_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing stock screener: {e}")
        finally:
            self.is_loading_stock_screener = False

    # =========================================================================
    # Special Terms
    # =========================================================================

    async def force_refresh_special_terms(self):
        """Force refresh special terms data with loading overlay."""
        if self.is_loading_special_terms:
            return
        self.is_loading_special_terms = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.special_terms = await service.get_special_terms()
            self.special_terms_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing special terms: {e}")
        finally:
            self.is_loading_special_terms = False

    # =========================================================================
    # Instrument Data
    # =========================================================================

    async def force_refresh_instrument_data(self):
        """Force refresh instrument data with loading overlay."""
        if self.is_loading_instrument_data:
            return
        self.is_loading_instrument_data = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.instrument_data = await service.get_instrument_data()
            self.instrument_data_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing instrument data: {e}")
        finally:
            self.is_loading_instrument_data = False

    # =========================================================================
    # Instrument Terms
    # =========================================================================

    async def force_refresh_instrument_terms(self):
        """Force refresh instrument terms data with loading overlay."""
        if self.is_loading_instrument_terms:
            return
        self.is_loading_instrument_terms = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.instrument_terms = await service.get_instrument_terms()
            self.instrument_terms_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing instrument terms: {e}")
        finally:
            self.is_loading_instrument_terms = False

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
