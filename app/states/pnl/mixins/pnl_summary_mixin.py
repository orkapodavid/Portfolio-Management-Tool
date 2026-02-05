import asyncio

import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLSummaryItem


class PnLSummaryMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Summary data state and filtering.
    """

    # P&L Summary data
    pnl_summary_list: list[PnLSummaryItem] = []
    is_loading_pnl_summary: bool = False
    pnl_summary_error: str = ""
    pnl_summary_last_updated: str = "—"
    pnl_summary_auto_refresh: bool = True

    # Filters
    pnl_summary_search: str = ""
    pnl_summary_sort_column: str = ""
    pnl_summary_sort_direction: str = "asc"

    async def load_pnl_summary_data(self):
        """Load P&L Summary data from PnLService."""
        self.is_loading_pnl_summary = True
        self.pnl_summary_error = ""
        try:
            service = PnLService()
            self.pnl_summary_list = await service.get_pnl_summary()
        except Exception as e:
            self.pnl_summary_error = str(e)
            import logging

            logging.exception(f"Error loading P&L summary data: {e}")
        finally:
            self.is_loading_pnl_summary = False
            from datetime import datetime

            self.pnl_summary_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_pnl_summary_auto_refresh(self):
        """Background task for PnL Summary auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.pnl_summary_auto_refresh:
                    break
                self.simulate_pnl_summary_update()
            await asyncio.sleep(2)

    def toggle_pnl_summary_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.pnl_summary_auto_refresh = value
        if value:
            return type(self).start_pnl_summary_auto_refresh

    def simulate_pnl_summary_update(self):
        """Simulated delta update for demo - random price fluctuations."""
        if not self.pnl_summary_auto_refresh or len(self.pnl_summary_list) < 1:
            return

        import random
        from datetime import datetime

        # Create a new list to trigger change detection
        new_list = list(self.pnl_summary_list)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small price changes - update 'price' field
            if "price" in new_row and new_row["price"]:
                try:
                    # Parse the formatted string (e.g., "2,876.50")
                    val = float(str(new_row["price"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.995, 1.005), 2)
                    # Format with commas for display
                    new_row["price"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            # Also update fx_rate for more visible changes
            if "fx_rate" in new_row and new_row["fx_rate"]:
                try:
                    val = float(str(new_row["fx_rate"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.9999, 1.0001), 4)
                    new_row["fx_rate"] = f"{new_val:.4f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.pnl_summary_list = new_list
        self.pnl_summary_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_pnl_summary_search(self, query: str):
        self.pnl_summary_search = query

    def sort_pnl_summary(self, column: str):
        if self.pnl_summary_sort_column == column:
            self.pnl_summary_sort_direction = (
                "desc" if self.pnl_summary_sort_direction == "asc" else "asc"
            )
        else:
            self.pnl_summary_sort_column = column
            self.pnl_summary_sort_direction = "asc"

    @rx.var(cache=True)
    def filtered_pnl_summary(self) -> list[PnLSummaryItem]:
        data = self.pnl_summary_list
        if self.pnl_summary_search:
            query = self.pnl_summary_search.lower()
            data = [
                item for item in data if query in item.get("underlying", "").lower()
            ]
        return data
