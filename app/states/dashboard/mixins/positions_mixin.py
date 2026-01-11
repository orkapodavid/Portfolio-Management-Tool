"""
Positions Mixin - State functionality for position data

This Mixin provides all position-related state variables, computed vars,
and event handlers. It integrates with PositionService for data access.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import PositionService
from app.states.dashboard.types import (
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
    TradeSummaryItem,
)


class PositionsMixin(rx.State, mixin=True):
    """
    Mixin providing position data state and filtering.

    Data provided:
    - Stock positions
    - Warrant positions
    - Bond positions
    - Trade summaries
    """

    # Position data lists
    positions: list[PositionItem] = []
    stock_positions: list[StockPositionItem] = []
    warrant_positions: list[WarrantPositionItem] = []
    bond_positions: list[BondPositionItem] = []
    trade_summaries: list[TradeSummaryItem] = []

    async def load_positions_data(self):
        """Load all position data from PositionService."""
        try:
            service = PositionService()
            self.stock_positions = await service.get_stock_positions()
            self.warrant_positions = await service.get_warrant_positions()
            self.bond_positions = await service.get_bond_positions()
        except Exception as e:
            import logging

            logging.exception(f"Error loading positions: {e}")

    def _filter_by_ticker(self, items: list[dict], search_query: str) -> list[dict]:
        """Helper to filter items by ticker or company name."""
        if not search_query:
            return items
        query = search_query.lower()
        return [
            item
            for item in items
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]
