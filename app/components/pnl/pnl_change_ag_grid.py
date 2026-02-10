"""
PnL Change AG-Grid Component.

AG-Grid based implementation for PnL change table, using standardized grid factory.
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
                    value=PnLState.pnl_change_position_date,
                    on_change=PnLState.set_pnl_change_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border border-gray-100 rounded-lg backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "pnl_change_grid_state"
_GRID_ID = "pnl_change_grid"


def pnl_change_ag_grid() -> rx.Component:
    """
    PnL Change AG-Grid component.

    Displays PnL change data with:
    - Position date selector (defaults to today, auto-reloads on change)
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
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        # Toolbar with grouped buttons (Export | Layout)
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="pnl_change",
            search_value=PnLChangeGridState.search_text,
            on_search_change=PnLChangeGridState.set_search,
            on_search_clear=PnLChangeGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=PnLState.pnl_change_last_updated,
            auto_refresh=PnLState.pnl_change_auto_refresh,
            on_auto_refresh_toggle=PnLState.toggle_pnl_change_auto_refresh,
            # Refresh button
            show_refresh=True,
            on_refresh=PnLState.force_refresh_pnl_change,
            is_loading=PnLState.is_loading_pnl_change,
        ),
        # Position date selector bar
        _position_date_bar(),
        # Grid with row grouping support
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PnLState.filtered_pnl_change,
            column_defs=_get_column_defs(),
            row_id_key="ticker",
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pnl_change"),
            default_csv_export_params=get_default_csv_export_params("pnl_change"),
            quick_filter_text=PnLChangeGridState.search_text,
            loading=PnLState.is_loading_pnl_change,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=PnLState.start_pnl_change_auto_refresh,
    )
