"""
PnL Currency AG-Grid Component.

AG-Grid based implementation for PnL currency table, using standardized grid factory.
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


class PnLCurrencyGridState(rx.State):
    """State for PnL Currency grid quick filter."""

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
    """Return column definitions for the PnL currency grid."""
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
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
            enable_row_group=True,
            tooltip_field="currency",
            pinned="left",  # Keep currency visible while scrolling
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
            field="ccy_exposure",
            header_name="CCY Exposure",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="usd_exposure",
            header_name="USD Exposure",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="pos_ccy_expo",
            header_name="POS CCY Expo",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="ccy_hedged_pnl",
            header_name="CCY Hedged PnL",
            filter=AGFilters.text,
            min_width=120,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="pos_ccy_pnl",
            header_name="POS CCY PnL",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
            enable_row_group=True,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="net_ccy",
            header_name="Net CC",
            filter=AGFilters.text,
            min_width=90,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pos_c_truncated",
            header_name="POS C (truncated)",
            filter=AGFilters.text,
            min_width=130,
            cell_style=_VALUE_STYLE,
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
                    value=PnLState.pnl_currency_position_date,
                    on_change=PnLState.set_pnl_currency_position_date,
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
_STORAGE_KEY = "pnl_currency_grid_state"
_GRID_ID = "pnl_currency_grid"


def pnl_currency_ag_grid() -> rx.Component:
    """
    PnL Currency AG-Grid component.

    Displays PnL currency data with:
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
            page_name="pnl_currency",
            search_value=PnLCurrencyGridState.search_text,
            on_search_change=PnLCurrencyGridState.set_search,
            on_search_clear=PnLCurrencyGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=PnLState.pnl_currency_last_updated,
            auto_refresh=PnLState.pnl_currency_auto_refresh,
            on_auto_refresh_toggle=PnLState.toggle_pnl_currency_auto_refresh,
            # Refresh button
            show_refresh=True,
            on_refresh=PnLState.force_refresh_pnl_currency,
            is_loading=PnLState.is_loading_pnl_currency,
        ),
        # Position date selector bar
        _position_date_bar(),
        # Grid with row grouping support
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PnLState.filtered_pnl_currency,
            column_defs=_get_column_defs(),
            row_id_key="currency",
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pnl_currency"),
            default_csv_export_params=get_default_csv_export_params("pnl_currency"),
            quick_filter_text=PnLCurrencyGridState.search_text,
            loading=PnLState.is_loading_pnl_currency,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=PnLState.start_pnl_currency_auto_refresh,
    )
