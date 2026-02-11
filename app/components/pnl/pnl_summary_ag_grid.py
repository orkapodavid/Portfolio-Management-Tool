"""
PnL Summary AG-Grid Component.

AG-Grid based implementation for PnL summary table, using standardized grid factory.
Includes a position date selector that triggers database reload.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.pnl.pnl_state import PnLState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    filter_date_input,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


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
            pinned="left",  # Keep visible while scrolling
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
            enable_row_group=True,
            tooltip_field="currency",
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
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="adv_3m",
            header_name="ADV 3M",
            filter=AGFilters.text,
            min_width=90,
            enable_row_group=True,
            agg_func="avg",
        ),
    ]


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar — triggers data reload on change."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span(
                    "POSITION DATE",
                    class_name=FILTER_LABEL_CLASS,
                ),
                rx.el.input(
                    type="date",
                    value=PnLState.pnl_summary_position_date,
                    on_change=PnLState.set_pnl_summary_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "w-full px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border-b border-gray-100 backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "pnl_summary_grid_state"
_GRID_ID = "pnl_summary_grid"


def pnl_summary_ag_grid() -> rx.Component:
    """
    PnL Summary AG-Grid component.

    Displays PnL summary data with:
    - Position date selector (defaults to today, auto-reloads on change)
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
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="pnl_summary",
            search_value=PnLSummaryGridState.search_text,
            on_search_change=PnLSummaryGridState.set_search,
            on_search_clear=PnLSummaryGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=PnLState.pnl_summary_last_updated,
            auto_refresh=PnLState.pnl_summary_auto_refresh,
            on_auto_refresh_toggle=PnLState.toggle_pnl_summary_auto_refresh,
            # Refresh button
            show_refresh=True,
            on_refresh=PnLState.force_refresh_pnl_summary,
            is_loading=PnLState.is_loading_pnl_summary,
        ),
        # Position date selector bar
        _position_date_bar(),
        # Grid with row grouping support
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PnLState.filtered_pnl_summary,
            column_defs=_get_column_defs(),
            row_id_key="underlying",
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pnl_summary"),
            default_csv_export_params=get_default_csv_export_params("pnl_summary"),
            quick_filter_text=PnLSummaryGridState.search_text,
            loading=PnLState.is_loading_pnl_summary,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=PnLState.start_pnl_summary_auto_refresh,
    )
