"""
PnL Summary AG-Grid Component.

AG-Grid based implementation for PnL summary table, using standardized grid factory.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.pnl.pnl_state import PnLState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class PnLSummaryGridState(rx.State):
    """State for PnL Summary grid quick filter."""

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
    """Return column definitions for the PnL summary grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            filter=AGFilters.text,
            min_width=90,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="price_t_1",
            header_name="Price (T-1)",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="price_change",
            header_name="Price Change",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="fx_rate",
            header_name="FX Rate",
            filter=AGFilters.text,
            min_width=90,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="fx_rate_t_1",
            header_name="FX Rate (T-1)",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="fx_rate_change",
            header_name="FX Rate Change",
            filter=AGFilters.text,
            min_width=120,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="dtl",
            header_name="DTL",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="last_volume",
            header_name="Last Volume",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="adv_3m",
            header_name="ADV 3M",
            filter=AGFilters.text,
            min_width=90,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "pnl_summary_grid_state"


def pnl_summary_ag_grid() -> rx.Component:
    """
    PnL Summary AG-Grid component.

    Displays PnL summary data with:
    - Quick filter search across all columns
    - Excel export button
    - Full grid state persistence
    - Status bar with row counts
    """
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        rx.script(grid_state_script(_STORAGE_KEY)),
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="pnl_summary",
            search_value=PnLSummaryGridState.search_text,
            on_search_change=PnLSummaryGridState.set_search,
            on_search_clear=PnLSummaryGridState.clear_search,
            grid_id="pnl_summary_grid",
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id="pnl_summary_grid",
            row_data=PnLState.filtered_pnl_summary,
            column_defs=_get_column_defs(),
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pnl_summary"),
            default_csv_export_params=get_default_csv_export_params("pnl_summary"),
            quick_filter_text=PnLSummaryGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )

