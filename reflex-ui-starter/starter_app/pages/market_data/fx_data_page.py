"""
Market Data FX Data Page — Thin wrapper around the FX data grid component.

Follows the PMT page pattern: module_layout(content=<grid_component>).
"""

import reflex as rx
from starter_app.states.ui.ui_state import UIState
from starter_app.components.shared.module_layout import module_layout
from starter_app.components.market_data.fx_data_ag_grid import fx_data_ag_grid


def fx_data_page() -> rx.Component:
    """Market Data FX Data page with currency pair AG Grid."""
    return module_layout(
        content=fx_data_ag_grid(),
        module_name="Market Data",
        subtab_name="FX Data",
        subtabs=UIState.MODULE_SUBTABS["Market Data"],
    )
