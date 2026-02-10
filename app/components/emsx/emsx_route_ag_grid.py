"""
EMSX Route AG-Grid Component.

AG-Grid based implementation for EMSX route table, replacing legacy rx.el.table.
Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.emsx.emsx_state import EMSXState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class EMSXRouteGridState(rx.State):
    """State for EMSX Route grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        """Update search text."""
        self.search_text = value

    def clear_search(self):
        """Clear search text."""
        self.search_text = ""


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the EMSX route grid."""
    return [
        ag_grid.column_def(
            field="id",
            header_name="ID",
            filter=AGFilters.number,
            min_width=70,
            hide=True,  # Hidden unique identifier for row_id_key
        ),
        ag_grid.column_def(
            field="order_id",
            header_name="Order ID",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="route_id",
            header_name="Route ID",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="route_id",
            pinned="left",  # Keep visible while scrolling
        ),
        ag_grid.column_def(
            field="broker",
            header_name="Broker",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="broker",
        ),
        ag_grid.column_def(
            field="quantity",
            header_name="Quantity",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="filled_quantity",
            header_name="Filled Qty",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="avg_price",
            header_name="Avg Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter="agSetColumnFilter",  # Categorical column
            min_width=100,
        ),
    ]



# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "emsx_route_grid_state"
_GRID_ID = "emsx_route_grid"


def emsx_route_ag_grid() -> rx.Component:
    """
    EMSX Route AG-Grid component.

    Displays EMSX routes with sequence, ticker, broker information.
    Features:
    - Quick filter search across all columns
    - Excel export button
    - Full grid state persistence (columns + filters + sort)
    - Status bar with row counts
    - Compact mode toggle
    """
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        # Grid state persistence script (auto-restores on page load)
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        # Toolbar with grouped buttons (Export | Layout | Refresh)
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="emsx_route",
            search_value=EMSXRouteGridState.search_text,
            on_search_change=EMSXRouteGridState.set_search,
            on_search_clear=EMSXRouteGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Ticking pattern props
            last_updated=EMSXState.emsx_route_last_updated,
            show_refresh=True,
            on_refresh=EMSXState.force_refresh_emsx_routes,
            is_loading=EMSXState.is_loading_emsx_routes,
            auto_refresh=EMSXState.emsx_route_auto_refresh,
            on_auto_refresh_toggle=EMSXState.toggle_emsx_route_auto_refresh,
        ),
        # Grid with factory pattern
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=EMSXState.emsx_routes,
            column_defs=_get_column_defs(),
            row_id_key="id",  # Delta detection key (unique row ID)
            loading=EMSXState.is_loading_emsx_routes,  # Loading overlay
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            enable_cell_flash=True,  # Tier 2: Cell flash for ticking updates
            default_excel_export_params=get_default_export_params("emsx_route"),
            default_csv_export_params=get_default_csv_export_params("emsx_route"),
            quick_filter_text=EMSXRouteGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )