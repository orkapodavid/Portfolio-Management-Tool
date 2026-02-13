"""
Market Data Reference Data Page — Thin wrapper around the reference data grid component.

Follows the PMT page pattern: module_layout(content=<grid_component>).
"""

import reflex as rx
from starter_app.states.ui.ui_state import UIState
from starter_app.components.shared.module_layout import module_layout
from starter_app.components.market_data.reference_data_ag_grid import reference_data_ag_grid


def reference_data_page() -> rx.Component:
    """Market Data Reference Data page with instrument reference AG Grid."""
    return module_layout(
        content=reference_data_ag_grid(),
        module_name="Market Data",
        subtab_name="Reference Data",
        subtabs=UIState.MODULE_SUBTABS["Market Data"],
    )
