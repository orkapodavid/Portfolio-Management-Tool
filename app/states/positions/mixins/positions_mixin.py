import asyncio

import reflex as rx
from app.services import PositionService
from app.states.positions.types import PositionItem


class PositionsMixin(rx.State, mixin=True):
    """
    Mixin providing general Positions data state.
    """

    positions: list[PositionItem] = []
    is_loading_positions: bool = False
    positions_error: str = ""

    # Status bar state (per-tab, NOT shared!)
    positions_last_updated: str = "—"
    positions_auto_refresh: bool = True

    positions_search: str = ""

    async def load_positions_data(self):
        """Load positions data."""
        self.is_loading_positions = True
        self.positions_error = ""
        try:
            service = PositionService()
            self.positions = await service.get_positions()
        except Exception as e:
            self.positions_error = str(e)
            import logging

            logging.exception(f"Error loading positions: {e}")
        finally:
            self.is_loading_positions = False
            from datetime import datetime

            self.positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_positions_auto_refresh(self):
        """Background task for Positions auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.positions_auto_refresh:
                    break
                self.simulate_positions_update()
            await asyncio.sleep(2)

    def toggle_positions_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.positions_auto_refresh = value
        if value:
            return type(self).start_positions_auto_refresh

    def simulate_positions_update(self):
        """Simulated update for demo - random position fluctuations."""
        if not self.positions_auto_refresh or len(self.positions) < 1:
            return

        import random
        import re
        from datetime import datetime

        def parse_currency(val) -> float:
            """Parse currency string like '$300,000.00' to float."""
            if val is None:
                return 0.0
            if isinstance(val, (int, float)):
                return float(val)
            # Remove currency symbols and commas
            cleaned = re.sub(r"[^\d.\-]", "", str(val))
            try:
                return float(cleaned) if cleaned else 0.0
            except ValueError:
                return 0.0

        # Immutable update for cell flash
        new_list = list(self.positions)
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            new_row = dict(new_list[idx])
            # Simulate numeric field changes (notional may be formatted)
            if "notional" in new_row and new_row["notional"] is not None:
                current = parse_currency(new_row["notional"])
                new_row["notional"] = current * (1 + random.uniform(-0.01, 0.01))
            new_list[idx] = new_row
        self.positions = new_list
        self.positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_positions_search(self, query: str):
        self.positions_search = query

    @rx.var(cache=True)
    def filtered_positions(self) -> list[PositionItem]:
        data = self.positions
        if self.positions_search:
            query = self.positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("description", "").lower()
            ]
        return data
