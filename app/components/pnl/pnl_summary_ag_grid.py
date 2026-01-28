"""
PnL Summary AG-Grid Component.

AG-Grid based implementation for PnL summary table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.pnl.pnl_state import PnLState


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


def pnl_summary_ag_grid() -> rx.Component:
    """
    PnL Summary AG-Grid component.

    Displays PnL summary data with color-coded values.
    """
    return ag_grid(
        id="pnl_summary_grid",
        row_data=PnLState.filtered_pnl_summary,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="100%",
        width="100%",
    )
