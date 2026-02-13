"""
Dashboard Analytics Page — Thin wrapper around the market data grid component.

Follows the PMT page pattern: module_layout(content=<grid_component>).
"""

import reflex as rx
from starter_app.states.ui.ui_state import UIState
from starter_app.components.shared.module_layout import module_layout
from starter_app.components.dashboard.market_data_ag_grid import market_data_ag_grid


def analytics_page() -> rx.Component:
    """Dashboard Analytics page with market data AG Grid."""
    return module_layout(
        content=market_data_ag_grid(),
        module_name="Dashboard",
        subtab_name="Analytics",
        subtabs=UIState.MODULE_SUBTABS["Dashboard"],
    )
