import asyncio

import reflex as rx
from app.services import PositionService
from app.states.positions.types import BondPositionItem
import logging
import random

class BondPositionsMixin(rx.State, mixin=True):
    """
    Mixin providing Bond Positions data state.
    """

    bond_positions: list[BondPositionItem] = []
    is_loading_bond_positions: bool = False
    bond_positions_error: str = ""

    # Status bar state (per-tab, NOT shared!)
    bond_positions_last_updated: str = "—"
    bond_positions_auto_refresh: bool = True

    bond_positions_search: str = ""

    async def load_bond_positions_data(self):
        """Load bond positions data."""
        self.is_loading_bond_positions = True
        self.bond_positions_error = ""
        try:
            service = PositionService()
            self.bond_positions = await service.get_bond_positions()
        except Exception as e:
            self.bond_positions_error = str(e)

            logging.exception(f"Error loading bond positions: {e}")
        finally:
            self.is_loading_bond_positions = False
            from datetime import datetime

            self.bond_positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_bond_positions_auto_refresh(self):
        """Background task for Bond Positions auto-refresh (2s interval)."""
        # Load initial data if empty
        async with self:
            if len(self.bond_positions) == 0:
                await self.load_bond_positions_data()
        
        while True:
            async with self:
                if not self.bond_positions_auto_refresh:
                    break
                self.simulate_bond_positions_update()
            await asyncio.sleep(2)

    def toggle_bond_positions_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.bond_positions_auto_refresh = value
        if value:
            return type(self).start_bond_positions_auto_refresh

    def simulate_bond_positions_update(self):
        """Simulated update for demo - random fluctuations."""
        if not self.bond_positions_auto_refresh or len(self.bond_positions) < 1:
            return

        import re
        from datetime import datetime

        def parse_alphanumeric_id(val: str) -> tuple[str, int]:
            """Parse alphanumeric ID like 'BD004' into prefix and number."""
            match = re.match(r"([A-Za-z]*)(\d+)", str(val))
            if match:
                return match.group(1), int(match.group(2))
            return "", 0

        # Immutable update for cell flash
        new_list = list(self.bond_positions)
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            new_row = dict(new_list[idx])
            # Simulate detail_id changes (handle alphanumeric IDs)
            if "detail_id" in new_row and new_row["detail_id"]:
                prefix, num = parse_alphanumeric_id(new_row["detail_id"])
                new_num = max(0, num + random.randint(-1, 1))
                new_row["detail_id"] = f"{prefix}{new_num:03d}"
            new_list[idx] = new_row
        self.bond_positions = new_list
        self.bond_positions_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_bond_positions_search(self, query: str):
        self.bond_positions_search = query

    @rx.var(cache=True)
    def filtered_bond_positions(self) -> list[BondPositionItem]:
        data = self.bond_positions
        if self.bond_positions_search:
            query = self.bond_positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("underlying", "").lower()
            ]
        return data
