import asyncio
from datetime import datetime

import reflex as rx
from app.services import PositionService
from app.states.positions.types import TradeSummaryItem


class TradeSummaryMixin(rx.State, mixin=True):
    """
    Mixin providing Trade Summary data state.
    """

    trade_summaries: list[TradeSummaryItem] = []
    is_loading_trade_summaries: bool = False
    trade_summary_error: str = ""

    # Status bar state (per-tab, NOT shared!)
    trade_summary_last_updated: str = "—"
    trade_summary_auto_refresh: bool = True

    trade_summary_search: str = ""

    # Position date — defaults to today
    trade_summary_position_date: str = ""

    def _ensure_trade_summary_date(self) -> str:
        """Return position_date or today if empty."""
        if not self.trade_summary_position_date:
            self.trade_summary_position_date = datetime.now().strftime("%Y-%m-%d")
        return self.trade_summary_position_date

    async def load_trade_summary_data(self):
        """Load trade summary data."""
        self.is_loading_trade_summaries = True
        self.trade_summary_error = ""
        try:
            pos_date = self._ensure_trade_summary_date()
            service = PositionService()
            self.trade_summaries = await service.get_trade_summary(
                start_date=pos_date, end_date=pos_date
            )
        except Exception as e:
            self.trade_summary_error = str(e)
            import logging

            logging.exception(f"Error loading trade summary: {e}")
        finally:
            self.is_loading_trade_summaries = False
            self.trade_summary_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    async def set_trade_summary_position_date(self, value: str):
        """Set position date and reload data."""
        self.trade_summary_position_date = value
        await self.load_trade_summary_data()

    async def force_refresh_trade_summary(self):
        """Force refresh trade summary data with loading overlay."""
        if self.is_loading_trade_summaries:
            return  # Debounce
        self.is_loading_trade_summaries = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            pos_date = self._ensure_trade_summary_date()
            service = PositionService()
            self.trade_summaries = await service.get_trade_summary(
                start_date=pos_date, end_date=pos_date
            )
            self.trade_summary_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing trade summary: {e}")
        finally:
            self.is_loading_trade_summaries = False

    @rx.event(background=True)
    async def start_trade_summary_auto_refresh(self):
        """Background task for Trade Summary auto-refresh (2s interval)."""
        # Load initial data if empty
        async with self:
            if len(self.trade_summaries) == 0:
                await self.load_trade_summary_data()

        while True:
            async with self:
                if not self.trade_summary_auto_refresh:
                    break
                self.simulate_trade_summary_update()
            await asyncio.sleep(2)

    def toggle_trade_summary_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.trade_summary_auto_refresh = value
        if value:
            return type(self).start_trade_summary_auto_refresh

    def simulate_trade_summary_update(self):
        """Simulated update for demo - random fluctuations."""
        if not self.trade_summary_auto_refresh or len(self.trade_summaries) < 1:
            return

        import random

        # Immutable update for cell flash
        new_list = list(self.trade_summaries)
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            new_row = dict(new_list[idx])
            # Simulate divisor changes
            if "divisor" in new_row and new_row["divisor"]:
                try:
                    val = float(new_row["divisor"])
                    new_row["divisor"] = str(
                        round(val * random.uniform(0.99, 1.01), 4)
                    )
                except (ValueError, TypeError):
                    pass
            new_list[idx] = new_row
        self.trade_summaries = new_list
        self.trade_summary_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_trade_summary_search(self, query: str):
        self.trade_summary_search = query

    @rx.var(cache=True)
    def filtered_trade_summaries(self) -> list[TradeSummaryItem]:
        data = self.trade_summaries
        if self.trade_summary_search:
            query = self.trade_summary_search.lower()
            data = [item for item in data if query in item.get("ticker", "").lower()]
        return data
