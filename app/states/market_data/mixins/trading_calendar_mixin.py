import asyncio
from datetime import datetime

import reflex as rx
from app.states.market_data.types import TradingCalendarItem
import logging
from app.services import services

class TradingCalendarMixin(rx.State, mixin=True):
    """
    Mixin providing Trading Calendar state.

    On every filter change the service is queried with the current parameters.
    Results are cached at the service level since calendar data is immutable.
    """

    trading_calendar: list[TradingCalendarItem] = []
    is_loading_trading_calendar: bool = False
    trading_calendar_error: str = ""
    trading_calendar_last_updated: str = "—"

    # --- Filter state ---
    trading_calendar_from_date: str = ""
    trading_calendar_to_date: str = ""

    async def load_trading_calendar(self):
        """Load trading calendar using current filter params via the services.market_data."""
        self.is_loading_trading_calendar = True
        self.trading_calendar_error = ""
        try:
            self.trading_calendar = await services.market_data.get_trading_calendar(
                start_date=self.trading_calendar_from_date or None,
                end_date=self.trading_calendar_to_date or None,
            )
        except Exception as e:
            self.trading_calendar_error = str(e)

            logging.exception(f"Error loading trading calendar: {e}")
        finally:
            self.is_loading_trading_calendar = False
            self.trading_calendar_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    async def force_refresh_trading_calendar(self):
        """Force refresh - reloads data from service (all cells flash)."""
        self.is_loading_trading_calendar = True
        yield  # Send loading state to client
        await asyncio.sleep(1)  # Show loading overlay for 1s
        await self.load_trading_calendar()

    # --- Filter event handlers ---

    async def set_trading_calendar_from_date(self, value: str):
        """Set the from-date filter and re-query."""
        self.trading_calendar_from_date = value
        await self.load_trading_calendar()

    async def set_trading_calendar_to_date(self, value: str):
        """Set the to-date filter and re-query."""
        self.trading_calendar_to_date = value
        await self.load_trading_calendar()

    async def apply_trading_calendar_filters(self):
        """Explicitly re-query with current filters."""
        await self.load_trading_calendar()

    async def clear_trading_calendar_filters(self):
        """Reset all filters to defaults and re-query."""
        self.trading_calendar_from_date = ""
        self.trading_calendar_to_date = ""
        await self.load_trading_calendar()

    @rx.var(cache=True)
    def trading_calendar_has_active_filters(self) -> bool:
        """Whether any filters are currently active."""
        return bool(
            self.trading_calendar_from_date
            or self.trading_calendar_to_date
        )
