import asyncio
from datetime import datetime

import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLCurrencyItem


class PnLCurrencyMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Currency data state and filtering.
    """

    # P&L Currency data
    pnl_currency_list: list[PnLCurrencyItem] = []
    is_loading_pnl_currency: bool = False
    pnl_currency_error: str = ""
    pnl_currency_last_updated: str = "—"
    pnl_currency_auto_refresh: bool = True

    # Filters
    pnl_currency_search: str = ""

    # Position date — defaults to today
    pnl_currency_position_date: str = ""

    def _ensure_pnl_currency_date(self) -> str:
        """Return position_date or today if empty."""
        if not self.pnl_currency_position_date:
            self.pnl_currency_position_date = datetime.now().strftime("%Y-%m-%d")
        return self.pnl_currency_position_date

    async def load_pnl_currency_data(self):
        """Load P&L Currency data from PnLService."""
        self.is_loading_pnl_currency = True
        self.pnl_currency_error = ""
        try:
            pos_date = self._ensure_pnl_currency_date()
            service = PnLService()
            self.pnl_currency_list = await service.get_pnl_by_currency(pos_date)
        except Exception as e:
            self.pnl_currency_error = str(e)
            import logging

            logging.exception(f"Error loading P&L currency data: {e}")
        finally:
            self.is_loading_pnl_currency = False
            self.pnl_currency_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    async def set_pnl_currency_position_date(self, value: str):
        """Set position date and reload data."""
        self.pnl_currency_position_date = value
        await self.load_pnl_currency_data()

    async def force_refresh_pnl_currency(self):
        """Force refresh PnL currency data with loading overlay."""
        if self.is_loading_pnl_currency:
            return  # Debounce
        self.is_loading_pnl_currency = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            pos_date = self._ensure_pnl_currency_date()
            service = PnLService()
            self.pnl_currency_list = await service.get_pnl_by_currency(pos_date)
            self.pnl_currency_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing PnL currency: {e}")
        finally:
            self.is_loading_pnl_currency = False

    @rx.event(background=True)
    async def start_pnl_currency_auto_refresh(self):
        """Background task for PnL Currency auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.pnl_currency_auto_refresh:
                    break
                self.simulate_pnl_currency_update()
            await asyncio.sleep(2)

    def toggle_pnl_currency_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.pnl_currency_auto_refresh = value
        if value:
            return type(self).start_pnl_currency_auto_refresh

    def simulate_pnl_currency_update(self):
        """Simulated delta update for demo - random PnL fluctuations."""
        if not self.pnl_currency_auto_refresh or len(self.pnl_currency_list) < 1:
            return

        import random

        # Create a new list to trigger change detection
        new_list = list(self.pnl_currency_list)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small FX rate changes
            if "fx_rate" in new_row and new_row["fx_rate"]:
                try:
                    val = float(str(new_row["fx_rate"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.999, 1.001), 4)
                    new_row["fx_rate"] = f"{new_val:.4f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.pnl_currency_list = new_list
        self.pnl_currency_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_pnl_currency_search(self, query: str):
        self.pnl_currency_search = query

    @rx.var(cache=True)
    def filtered_pnl_currency(self) -> list[PnLCurrencyItem]:
        data = self.pnl_currency_list
        if self.pnl_currency_search:
            query = self.pnl_currency_search.lower()
            data = [item for item in data if query in item.get("currency", "").lower()]
        return data
