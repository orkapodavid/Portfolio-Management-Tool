import asyncio

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

    async def load_pnl_currency_data(self):
        """Load P&L Currency data from PnLService."""
        self.is_loading_pnl_currency = True
        self.pnl_currency_error = ""
        try:
            service = PnLService()
            self.pnl_currency_list = await service.get_currency_pnl()
        except Exception as e:
            self.pnl_currency_error = str(e)
            import logging

            logging.exception(f"Error loading P&L currency data: {e}")
        finally:
            self.is_loading_pnl_currency = False
            from datetime import datetime

            self.pnl_currency_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
        from datetime import datetime

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
