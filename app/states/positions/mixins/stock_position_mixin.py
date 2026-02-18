import asyncio

import reflex as rx
from app.services import PositionService
from app.states.positions.types import StockPositionItem
import logging
import random

class StockPositionMixin(rx.State, mixin=True):
    """
    Mixin providing Stock Position data state.
    """

    stock_positions: list[StockPositionItem] = []
    is_loading_stock_positions: bool = False
    stock_positions_error: str = ""

    # Status bar state (per-tab, NOT shared!)
    stock_positions_last_updated: str = "—"
    stock_positions_auto_refresh: bool = True

    stock_positions_search: str = ""

    async def load_stock_positions_data(self):
        """Load stock positions data."""
        self.is_loading_stock_positions = True
        self.stock_positions_error = ""
        try:
            service = PositionService()
            self.stock_positions = await service.get_stock_positions()
        except Exception as e:
            self.stock_positions_error = str(e)

            logging.exception(f"Error loading stock positions: {e}")
        finally:
            self.is_loading_stock_positions = False
            from datetime import datetime

            self.stock_positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_stock_positions_auto_refresh(self):
        """Background task for Stock Positions auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.stock_positions_auto_refresh:
                    break
                self.simulate_stock_positions_update()
            await asyncio.sleep(2)

    def toggle_stock_positions_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.stock_positions_auto_refresh = value
        if value:
            return type(self).start_stock_positions_auto_refresh

    def simulate_stock_positions_update(self):
        """Simulated update for demo - random fluctuations."""
        if not self.stock_positions_auto_refresh or len(self.stock_positions) < 1:
            return

        from datetime import datetime

        # Immutable update for cell flash
        new_list = list(self.stock_positions)
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            new_row = dict(new_list[idx])
            # Simulate notional field changes
            if "notional" in new_row and new_row["notional"]:
                try:
                    val = float(new_row["notional"].replace(",", "").replace("$", ""))
                    new_row["notional"] = f"${val * random.uniform(0.99, 1.01):,.2f}"
                except (ValueError, TypeError):
                    pass
            new_list[idx] = new_row
        self.stock_positions = new_list
        self.stock_positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_stock_positions_search(self, query: str):
        self.stock_positions_search = query

    @rx.var(cache=True)
    def filtered_stock_positions(self) -> list[StockPositionItem]:
        data = self.stock_positions
        if self.stock_positions_search:
            query = self.stock_positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("company_name", "").lower()
            ]
        return data
