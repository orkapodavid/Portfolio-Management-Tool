import asyncio
from datetime import datetime

import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLFullItem


class PnLFullMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Full data state and filtering.
    """

    # P&L Full data
    pnl_full_list: list[PnLFullItem] = []
    is_loading_pnl_full: bool = False
    pnl_full_error: str = ""
    pnl_full_last_updated: str = "—"
    pnl_full_auto_refresh: bool = True

    # Filters
    pnl_full_search: str = ""

    # Position date — defaults to today
    pnl_full_position_date: str = ""

    def _ensure_pnl_full_date(self) -> str:
        """Return position_date or today if empty."""
        if not self.pnl_full_position_date:
            self.pnl_full_position_date = datetime.now().strftime("%Y-%m-%d")
        return self.pnl_full_position_date

    async def load_pnl_full_data(self):
        """Load P&L Full data from PnLService."""
        self.is_loading_pnl_full = True
        self.pnl_full_error = ""
        try:
            pos_date = self._ensure_pnl_full_date()
            service = PnLService()
            self.pnl_full_list = await service.get_pnl_full(pos_date)
        except Exception as e:
            self.pnl_full_error = str(e)
            import logging

            logging.exception(f"Error loading P&L full data: {e}")
        finally:
            self.is_loading_pnl_full = False
            self.pnl_full_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def set_pnl_full_position_date(self, value: str):
        """Set position date and reload data."""
        self.pnl_full_position_date = value
        await self.load_pnl_full_data()

    async def force_refresh_pnl_full(self):
        """Force refresh PnL full data with loading overlay."""
        if self.is_loading_pnl_full:
            return  # Debounce
        self.is_loading_pnl_full = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            pos_date = self._ensure_pnl_full_date()
            service = PnLService()
            self.pnl_full_list = await service.get_pnl_full(pos_date)
            self.pnl_full_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing PnL full: {e}")
        finally:
            self.is_loading_pnl_full = False

    @rx.event(background=True)
    async def start_pnl_full_auto_refresh(self):
        """Background task for PnL Full auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.pnl_full_auto_refresh:
                    break
                self.simulate_pnl_full_update()
            await asyncio.sleep(2)

    def toggle_pnl_full_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.pnl_full_auto_refresh = value
        if value:
            return type(self).start_pnl_full_auto_refresh

    def simulate_pnl_full_update(self):
        """Simulated delta update for demo - random PnL fluctuations."""
        if not self.pnl_full_auto_refresh or len(self.pnl_full_list) < 1:
            return

        import random

        # Create a new list to trigger change detection
        new_list = list(self.pnl_full_list)

        # Update 1-5 random rows with PnL fluctuations
        for _ in range(random.randint(1, min(5, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small PnL changes on numeric fields
            for field in ["pnl_ytd", "pnl_chg_1d", "pnl_chg_1w", "pnl_chg_1m"]:
                if field in new_row and new_row[field]:
                    try:
                        # Parse value (handle "$1,234" or "($456)" formats)
                        val_str = str(new_row[field])
                        is_negative = "(" in val_str or val_str.startswith("-")
                        val = float(val_str.replace("$", "").replace(",", "").replace("(", "").replace(")", "").replace("-", ""))
                        if is_negative:
                            val = -val
                        new_val = round(val * random.uniform(0.97, 1.03), 2)
                        # Format output
                        if new_val < 0:
                            new_row[field] = f"(${abs(new_val):,.2f})"
                        else:
                            new_row[field] = f"${new_val:,.2f}"
                    except (ValueError, TypeError):
                        pass

            new_list[idx] = new_row

        self.pnl_full_list = new_list
        self.pnl_full_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_pnl_full_search(self, query: str):
        self.pnl_full_search = query

    @rx.var(cache=True)
    def filtered_pnl_full(self) -> list[PnLFullItem]:
        data = self.pnl_full_list
        if self.pnl_full_search:
            query = self.pnl_full_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("underlying", "").lower()
            ]
        return data
