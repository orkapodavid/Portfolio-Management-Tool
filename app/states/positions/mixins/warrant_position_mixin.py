import asyncio

import reflex as rx
from app.services import PositionService
from app.states.positions.types import WarrantPositionItem


class WarrantPositionMixin(rx.State, mixin=True):
    """
    Mixin providing Warrant Position data state.
    """

    warrant_positions: list[WarrantPositionItem] = []
    is_loading_warrant_positions: bool = False
    warrant_positions_error: str = ""

    # Status bar state (per-tab, NOT shared!)
    warrant_positions_last_updated: str = "—"
    warrant_positions_auto_refresh: bool = True

    warrant_positions_search: str = ""

    async def load_warrant_positions_data(self):
        """Load warrant positions data."""
        self.is_loading_warrant_positions = True
        self.warrant_positions_error = ""
        try:
            service = PositionService()
            self.warrant_positions = await service.get_warrant_positions()
        except Exception as e:
            self.warrant_positions_error = str(e)
            import logging

            logging.exception(f"Error loading warrant positions: {e}")
        finally:
            self.is_loading_warrant_positions = False
            from datetime import datetime

            self.warrant_positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_warrant_positions_auto_refresh(self):
        """Background task for Warrant Positions auto-refresh (2s interval)."""
        # Load initial data if empty
        async with self:
            if len(self.warrant_positions) == 0:
                await self.load_warrant_positions_data()
        
        while True:
            async with self:
                if not self.warrant_positions_auto_refresh:
                    break
                self.simulate_warrant_positions_update()
            await asyncio.sleep(2)

    def toggle_warrant_positions_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.warrant_positions_auto_refresh = value
        if value:
            return type(self).start_warrant_positions_auto_refresh

    def simulate_warrant_positions_update(self):
        """Simulated update for demo - random fluctuations."""
        if not self.warrant_positions_auto_refresh or len(self.warrant_positions) < 1:
            return

        import random
        import re
        from datetime import datetime

        def parse_alphanumeric_id(val: str) -> tuple[str, int]:
            """Parse alphanumeric ID like 'WD004' into prefix and number."""
            match = re.match(r"([A-Za-z]*)(\d+)", str(val))
            if match:
                return match.group(1), int(match.group(2))
            return "", 0

        # Immutable update for cell flash
        new_list = list(self.warrant_positions)
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            new_row = dict(new_list[idx])
            # Simulate detail_id changes (handle alphanumeric IDs)
            if "detail_id" in new_row and new_row["detail_id"]:
                prefix, num = parse_alphanumeric_id(new_row["detail_id"])
                new_num = max(0, num + random.randint(-1, 1))
                new_row["detail_id"] = f"{prefix}{new_num:03d}"
            new_list[idx] = new_row
        self.warrant_positions = new_list
        self.warrant_positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_warrant_positions_search(self, query: str):
        self.warrant_positions_search = query

    @rx.var(cache=True)
    def filtered_warrant_positions(self) -> list[WarrantPositionItem]:
        data = self.warrant_positions
        if self.warrant_positions_search:
            query = self.warrant_positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("underlying", "").lower()
            ]
        return data
