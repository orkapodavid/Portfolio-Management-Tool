import asyncio
from datetime import datetime

import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLChangeItem


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
            import logging

            logging.exception(f"Error loading P&L change data: {e}")
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
            import logging

            logging.exception(f"Error refreshing PnL change: {e}")
        finally:
            self.is_loading_pnl_change = False

    @rx.event(background=True)
    async def start_pnl_change_auto_refresh(self):
        """Background task for PnL Change auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.pnl_change_auto_refresh:
                    break
                self.simulate_pnl_change_update()
            await asyncio.sleep(2)

    def toggle_pnl_change_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.pnl_change_auto_refresh = value
        if value:
            return type(self).start_pnl_change_auto_refresh

    def simulate_pnl_change_update(self):
        """Simulated delta update for demo - random PnL fluctuations."""
        if not self.pnl_change_auto_refresh or len(self.pnl_change_list) < 1:
            return

        import random

        # Create a new list to trigger change detection
        new_list = list(self.pnl_change_list)

        # Update 1-5 random rows
        for _ in range(random.randint(1, min(5, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small PnL changes using correct field names from PnLRecord
            for field in ["pnl_chg_1d", "pnl_chg_1w", "pnl_chg_1m", "pnl_ytd"]:
                if field in new_row and new_row[field]:
                    try:
                        # Parse value (handle "$1,234" or "($456)" or "-$123" formats)
                        val_str = str(new_row[field])
                        is_negative = "(" in val_str or val_str.startswith("-")
                        val = float(val_str.replace("$", "").replace(",", "").replace("(", "").replace(")", "").replace("-", "").strip())
                        if is_negative:
                            val = -val
                        new_val = round(val * random.uniform(0.95, 1.05), 2)
                        # Format output
                        if new_val < 0:
                            new_row[field] = f"-${abs(new_val):,.2f}"
                        else:
                            new_row[field] = f"${new_val:,.2f}"
                    except (ValueError, TypeError):
                        pass

            # Also update percentage fields
            for field in ["pnl_chg_pct_1d", "pnl_chg_pct_1w", "pnl_chg_pct_1m"]:
                if field in new_row and new_row[field]:
                    try:
                        val_str = str(new_row[field])
                        val = float(val_str.replace("%", "").replace("+", ""))
                        new_val = round(val * random.uniform(0.9, 1.1), 2)
                        new_row[field] = f"{new_val:+.1f}%"
                    except (ValueError, TypeError):
                        pass

            new_list[idx] = new_row

        self.pnl_change_list = new_list
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

            def get_sort_key(item):
                val = item.get(self.pnl_change_sort_column, "")
                if isinstance(val, str):
                    cleaned = (
                        val.replace("$", "")
                        .replace(",", "")
                        .replace("%", "")
                        .replace("(", "-")
                        .replace(")", "")
                    )
                    try:
                        return float(cleaned)
                    except ValueError:
                        return val.lower()
                return val

            data = sorted(
                data,
                key=get_sort_key,
                reverse=(self.pnl_change_sort_direction == "desc"),
            )
        return data
