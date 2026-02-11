import asyncio
import logging
from datetime import datetime

import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLChangeItem
from app.utils.simulation import simulate_financial_tick
from app.utils.sort_utils import financial_sort_key

logger = logging.getLogger(__name__)


class PnLChangeMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Change data state and filtering.
    """

    # P&L Change data
    pnl_change_list: list[PnLChangeItem] = []
    is_loading_pnl_change: bool = False
    pnl_change_error: str = ""
    pnl_change_last_updated: str = "—"
    pnl_change_auto_refresh: bool = True

    # Filters
    pnl_change_search: str = ""
    pnl_change_sort_column: str = ""
    pnl_change_sort_direction: str = "asc"

    # Position date — defaults to today
    pnl_change_position_date: str = ""

    def _ensure_pnl_change_date(self) -> str:
        """Return position_date or today if empty."""
        if not self.pnl_change_position_date:
            self.pnl_change_position_date = datetime.now().strftime("%Y-%m-%d")
        return self.pnl_change_position_date

    async def load_pnl_change_data(self):
        """Load P&L Change data from PnLService."""
        self.is_loading_pnl_change = True
        self.pnl_change_error = ""
        try:
            pos_date = self._ensure_pnl_change_date()
            service = PnLService()
            self.pnl_change_list = await service.get_pnl_changes(pos_date)
        except Exception as e:
            self.pnl_change_error = str(e)
            logger.exception(f"Error loading P&L change data: {e}")
        finally:
            self.is_loading_pnl_change = False
            self.pnl_change_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def set_pnl_change_position_date(self, value: str):
        """Set position date and reload data."""
        self.pnl_change_position_date = value
        await self.load_pnl_change_data()

    async def force_refresh_pnl_change(self):
        """Force refresh PnL change data with loading overlay."""
        if self.is_loading_pnl_change:
            return  # Debounce
        self.is_loading_pnl_change = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            pos_date = self._ensure_pnl_change_date()
            service = PnLService()
            self.pnl_change_list = await service.get_pnl_changes(pos_date)
            self.pnl_change_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.exception(f"Error refreshing PnL change: {e}")
        finally:
            self.is_loading_pnl_change = False

    @rx.event(background=True)
    async def start_pnl_change_auto_refresh(self):
        """Background task for PnL Change auto-refresh (2s interval).

        Uses while-True with guard clause. Max ~1 hour before auto-stop.
        """
        for _ in range(1800):  # Safety: max ~1 hour at 2s intervals
            async with self:
                if not self.pnl_change_auto_refresh:
                    return
                self.simulate_pnl_change_update()
            await asyncio.sleep(2)

    def toggle_pnl_change_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.pnl_change_auto_refresh = value
        if value:
            return type(self).start_pnl_change_auto_refresh

    def simulate_pnl_change_update(self):
        """Apply simulated tick using shared utility."""
        if not self.pnl_change_auto_refresh or not self.pnl_change_list:
            return
        self.pnl_change_list = simulate_financial_tick(
            rows=self.pnl_change_list,
            value_fields=["pnl_chg_1d", "pnl_chg_1w", "pnl_chg_1m", "pnl_ytd"],
            pct_fields=["pnl_chg_pct_1d", "pnl_chg_pct_1w", "pnl_chg_pct_1m"],
        )
        self.pnl_change_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_pnl_change_search(self, query: str):
        self.pnl_change_search = query

    def sort_pnl_change(self, column: str):
        if self.pnl_change_sort_column == column:
            self.pnl_change_sort_direction = (
                "desc" if self.pnl_change_sort_direction == "asc" else "asc"
            )
        else:
            self.pnl_change_sort_column = column
            self.pnl_change_sort_direction = "asc"

    @rx.var(cache=True)
    def filtered_pnl_change(self) -> list[PnLChangeItem]:
        data = self.pnl_change_list
        # Filter
        if self.pnl_change_search:
            query = self.pnl_change_search.lower()
            data = [item for item in data if query in item.get("ticker", "").lower()]

        # Sort
        if self.pnl_change_sort_column:
            col = self.pnl_change_sort_column
            data = sorted(
                data,
                key=lambda item: financial_sort_key(item.get(col, "")),
                reverse=(self.pnl_change_sort_direction == "desc"),
            )
        return data
