"""
PnL Full AG-Grid Component.

AG-Grid based implementation for PnL full table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.pnl.pnl_state import PnLState
from app.components.shared.ag_grid_config import create_standard_grid


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
    """Return column definitions for the PnL full grid."""
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
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="pnl_ytd",
            header_name="PnL YTD",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_1d",
            header_name="PnL Chg 1D",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_1w",
            header_name="PnL Chg 1W",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_1m",
            header_name="PnL Chg 1M",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1d",
            header_name="PnL Chg% 1D",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1w",
            header_name="PnL Chg% 1W",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1m",
            header_name="PnL Chg% 1M",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for column state persistence
_STORAGE_KEY = "pnl_full_column_state"


def pnl_full_ag_grid() -> rx.Component:
    """
    PnL Full AG-Grid component.

    Displays full PnL data with Tier 1 + Tier 2 enhancements:
    - Excel export button
    - Column state persistence (auto-save + restore/reset)
    - Status bar with row counts and aggregation
    - Range selection
    - Floating filters
    - Cell flash for real-time updates
    """
    from app.components.shared.ag_grid_config import (
        export_button,
        column_state_buttons,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        # Toolbar
        rx.hstack(
            export_button(page_name="pnl_full"),
            column_state_buttons(
                _STORAGE_KEY, show_save=True
            ),  # Manual save since auto-save not supported
            justify="end",
            width="100%",
            padding_bottom="2",
            gap="4",
        ),
        # Grid
        create_standard_grid(
            grid_id="pnl_full_grid",
            row_data=PnLState.filtered_pnl_full,
            column_defs=_get_column_defs(),
            enable_cell_flash=True,  # Tier 2: Real-time grid
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("pnl_full"),
            default_csv_export_params=get_default_csv_export_params("pnl_full"),
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
