"""
Market Data State — Main composed state for the Market Data module.

Inherits from FX Data and Reference Data mixins.
"""

import reflex as rx
from starter_app.states.market_data.mixins.fx_data_mixin import FxDataMixin
from starter_app.states.market_data.mixins.reference_data_mixin import ReferenceDataMixin


class MarketDataState(
    FxDataMixin,
    ReferenceDataMixin,
    rx.State,
):
    """
    Main Market Data module state.
    Inherits from FX Data and Reference Data mixins.
    """

    active_market_data_subtab: str = "FX Data"

    @rx.event
    async def load_market_data_module_data(self):
        """Load data for the active subtab."""
        if self.active_market_data_subtab == "FX Data":
            self.load_fx_data()
        elif self.active_market_data_subtab == "Reference Data":
            self.load_reference_data()

    @rx.event
    def set_market_data_subtab(self, subtab: str):
        """Set the active market data subtab."""
        self.active_market_data_subtab = subtab
