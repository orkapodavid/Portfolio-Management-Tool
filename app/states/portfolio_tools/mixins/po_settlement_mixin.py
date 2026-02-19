"""
PO Settlement Mixin - Tab-specific state for PO Settlement data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.states.portfolio_tools.types import POSettlementItem
import logging
import random
from app.services import services

class POSettlementMixin(rx.State, mixin=True):
    """
    Mixin providing PO Settlement data state with auto-refresh.
    """

    # PO Settlement data
    po_settlement: list[POSettlementItem] = []
    is_loading_po_settlement: bool = False
    po_settlement_last_updated: str = "—"
    po_settlement_auto_refresh: bool = True
    po_settlement_position_date: str = datetime.now().strftime("%Y-%m-%d")

    async def set_po_settlement_position_date(self, value: str):
        """Set position date and reload data."""
        self.po_settlement_position_date = value
        yield
        await self.load_po_settlement_data()

    async def load_po_settlement_data(self):
        """Load PO Settlement data from PortfolioToolsService."""
        self.is_loading_po_settlement = True
        try:
            self.po_settlement = await services.portfolio_tools.get_po_settlement(self.po_settlement_position_date)
            self.po_settlement_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading PO settlement data: {e}")
        finally:
            self.is_loading_po_settlement = False

    @rx.event(background=True)
    async def start_po_settlement_auto_refresh(self):
        """Background task for PO Settlement auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.po_settlement_auto_refresh:
                    break
                self.simulate_po_settlement_update()
            await asyncio.sleep(2)

    def toggle_po_settlement_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.po_settlement_auto_refresh = value
        if value:
            return type(self).start_po_settlement_auto_refresh

    def simulate_po_settlement_update(self):
        """Simulated delta update for demo - random price changes."""
        if not self.po_settlement_auto_refresh or len(self.po_settlement) < 1:
            return

        new_list = list(self.po_settlement)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate last_price changes
            if "last_price" in new_row and new_row["last_price"]:
                try:
                    val = float(str(new_row["last_price"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.995, 1.005), 2)
                    new_row["last_price"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.po_settlement = new_list
        self.po_settlement_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_po_settlement(self):
        """Force refresh PO settlement data with loading overlay."""
        if self.is_loading_po_settlement:
            return
        self.is_loading_po_settlement = True
        yield
        await asyncio.sleep(0.3)
        try:
            self.po_settlement = await services.portfolio_tools.get_po_settlement(self.po_settlement_position_date)
            self.po_settlement_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_po_settlement = False
