"""
PnL Change AG-Grid Component.

AG-Grid based implementation for PnL change table, using standardized grid factory.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.pnl.pnl_state import PnLState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class PnLChangeGridState(rx.State):
    """State for PnL Change grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        """Update search text."""
        self.search_text = value

    def clear_search(self):
        """Clear search text."""
        self.search_text = ""


# =============================================================================
# CELL STYLES
# =============================================================================

# Value style - green for positive, red for negative
_VALUE_STYLE = rx.Var(
    """(params) => {
        const val = String(params.value || '');
        const isNegative = val.startsWith('-') || val.startsWith('(');
        return {
            color: isNegative ? '#dc2626' : '#059669',
            fontWeight: '700',
            fontFamily: 'monospace'
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the PnL change grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
            enable_row_group=True,
            tooltip_field="trade_date",
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            enable_row_group=True,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            enable_row_group=True,
            tooltip_field="ticker",
            pinned="left",  # Keep ticker visible while scrolling
        ),
        ag_grid.column_def(
            field="pnl_ytd",
            header_name="PnL YTD",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="pnl_chg_1d",
            header_name="PnL Chg 1D",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="pnl_chg_1w",
            header_name="PnL Chg 1W",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="pnl_chg_1m",
            header_name="PnL Chg 1M",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1d",
            header_name="PnL Chg% 1D",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="avg",
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1w",
            header_name="PnL Chg% 1W",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="avg",
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1m",
            header_name="PnL Chg% 1M",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="avg",
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "pnl_change_grid_state"


def pnl_change_ag_grid() -> rx.Component:
    """
    PnL Change AG-Grid component.

    Displays PnL change data with:
    - Quick filter search across all columns
    - Excel export button
    - Full grid state persistence (columns + filters + sort)
    - Status bar with row counts
    """
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        # Grid state persistence script (auto-restores on page load)
        rx.script(grid_state_script(_STORAGE_KEY, "pnl_change_grid")),
        # Toolbar with grouped buttons (Export | Layout)
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="pnl_change",
            search_value=PnLChangeGridState.search_text,
            on_search_change=PnLChangeGridState.set_search,
            on_search_clear=PnLChangeGridState.clear_search,
            grid_id="pnl_change_grid",
            show_compact_toggle=True,
        ),
        # Grid with row grouping support
        create_standard_grid(
            grid_id="pnl_change_grid",
            row_data=PnLState.filtered_pnl_change,
            column_defs=_get_column_defs(),
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pnl_change"),
            default_csv_export_params=get_default_csv_export_params("pnl_change"),
            quick_filter_text=PnLChangeGridState.search_text,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )

