"""
Instruments Mixin - State functionality for Instruments data

This Mixin provides all instruments-related state variables, computed vars,
and event handlers.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import DatabaseService
from app.states.dashboard.types import (
    TickerDataItem,
    StockScreenerItem,
    SpecialTermItem,
    InstrumentDataItem,
    InstrumentTermItem,
)


class InstrumentsMixin(rx.State, mixin=True):
    """
    Mixin providing instruments data state and filtering.

    Data provided:
    - Ticker data
    - Stock screener
    - Special terms
    - Instrument data
    - Instrument terms
    """

    # Instruments data lists
    stock_screener: list[StockScreenerItem] = []
    special_terms: list[SpecialTermItem] = []
    instrument_data: list[InstrumentDataItem] = []
    instrument_terms: list[InstrumentTermItem] = []

    async def load_instruments_data(self):
        """Load all instruments data from DatabaseService."""
        try:
            service = DatabaseService()
            self.stock_screener = await service.get_stock_screener()
            self.special_terms = await service.get_special_terms()
            self.instrument_data = await service.get_instrument_data()
            self.instrument_terms = await service.get_instrument_terms()
        except Exception as e:
            import logging

            logging.exception(f"Error loading instruments data: {e}")
