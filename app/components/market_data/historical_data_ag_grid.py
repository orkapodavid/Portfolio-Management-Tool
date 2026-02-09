"""
Historical Data AG-Grid Component.

Migrated to use create_standard_grid factory with cell flash and full toolbar support.
Includes filter bar with multi-select ticker popover and date range pickers.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    filter_date_range_bar,
    FILTER_BTN_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class HistoricalDataGridState(rx.State):
    """State for Historical Data grid quick filter only."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# CELL STYLES
# =============================================================================

# Ticker style - blue link
_TICKER_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

# Change % style - green for positive, red for negative
_CHANGE_STYLE = rx.Var(
    """(params) => {
        const val = parseFloat(params.value);
        if (isNaN(val)) return {};
        return {
            color: val >= 0 ? '#059669' : '#dc2626',
            fontWeight: '500'
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the historical data grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=110,
            pinned="left",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_TICKER_STYLE,
            tooltip_field="ticker",
        ),
        ag_grid.column_def(
            field="vwap_price",
            header_name="vWAP Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="last_volume",
            header_name="Last Volume",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="chg_1d_pct",
            header_name="1D Change %",
            filter=AGFilters.number,
            min_width=110,
            cell_style=_CHANGE_STYLE,
        ),
        ag_grid.column_def(
            field="created_by",
            header_name="Created By",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="created_time",
            header_name="Created Time",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="updated_by",
            header_name="Updated By",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="update",
            header_name="Update",
            filter=AGFilters.text,
            min_width=120,
        ),
    ]


# =============================================================================
# FILTER BAR — Ticker multi-select popover + Date range pickers
# =============================================================================


def _ticker_checkbox(ticker: rx.Var[str]) -> rx.Component:
    """Render a single ticker checkbox inside the popover."""
    return rx.el.label(
        rx.el.input(
            type="checkbox",
            checked=MarketDataState.historical_selected_tickers.contains(ticker),
            on_change=lambda _val: MarketDataState.toggle_historical_ticker(ticker),
            class_name="accent-blue-600 mr-2 cursor-pointer",
        ),
        rx.el.span(ticker, class_name="text-[12px] font-medium text-gray-700"),
        class_name="flex items-center px-2 py-1.5 rounded hover:bg-gray-50 cursor-pointer select-none",
    )


def _ticker_popover() -> rx.Component:
    """Multi-select ticker popover with checkboxes."""
    return rx.popover.root(
        rx.popover.trigger(
            rx.el.button(
                rx.icon("filter", size=12),
                rx.el.span("Tickers", class_name="ml-1"),
                rx.cond(
                    MarketDataState.historical_selected_ticker_count > 0,
                    rx.el.span(
                        MarketDataState.historical_selected_ticker_count,
                        class_name=(
                            "ml-1.5 bg-blue-600 text-white rounded-full "
                            "w-4 h-4 flex items-center justify-center text-[9px] font-bold"
                        ),
                    ),
                    rx.icon("chevron-down", size=10, class_name="ml-1 opacity-60"),
                ),
                class_name=(
                    f"{FILTER_BTN_CLASS} bg-white border border-gray-200 text-gray-600 "
                    "hover:bg-gray-50 hover:text-blue-600 hover:border-blue-300"
                ),
            ),
        ),
        rx.popover.content(
            rx.el.div(
                # Header with Select All / Clear
                rx.el.div(
                    rx.el.span(
                        "Select Tickers",
                        class_name="text-[11px] font-bold text-gray-800",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "All",
                            on_click=MarketDataState.select_all_historical_tickers,
                            class_name=(
                                "text-[10px] font-semibold text-blue-600 "
                                "hover:text-blue-800 cursor-pointer px-1"
                            ),
                        ),
                        rx.el.span("·", class_name="text-gray-300 mx-0.5"),
                        rx.el.button(
                            "Clear",
                            on_click=MarketDataState.clear_historical_tickers,
                            class_name=(
                                "text-[10px] font-semibold text-gray-400 "
                                "hover:text-red-500 cursor-pointer px-1"
                            ),
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex items-center justify-between px-2 py-2 border-b border-gray-100",
                ),
                # Ticker checkboxes
                rx.el.div(
                    rx.foreach(
                        MarketDataState.historical_available_tickers,
                        _ticker_checkbox,
                    ),
                    class_name="py-1 max-h-[240px] overflow-y-auto",
                ),
                class_name="w-[180px]",
            ),
            side="bottom",
            align="start",
        ),
    )


def _filter_bar() -> rx.Component:
    """Filter bar with ticker multi-select and date range pickers."""
    return filter_date_range_bar(
        from_value=MarketDataState.historical_from_date,
        to_value=MarketDataState.historical_to_date,
        on_from_change=MarketDataState.set_historical_from_date,
        on_to_change=MarketDataState.set_historical_to_date,
        on_apply=MarketDataState.apply_historical_filters,
        has_active_filters=MarketDataState.historical_has_active_filters,
        on_clear=MarketDataState.clear_historical_filters,
        extra_left_content=_ticker_popover(),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "historical_data_grid_state"
_GRID_ID = "historical_data_grid"


def historical_data_ag_grid() -> rx.Component:
    """Historical Data AG-Grid component with cell flash and full toolbar support."""
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
            page_name="historical_data",
            search_value=HistoricalDataGridState.search_text,
            on_search_change=HistoricalDataGridState.set_search,
            on_search_clear=HistoricalDataGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar — timestamp from mixin, toggle from mixin
            last_updated=MarketDataState.historical_data_last_updated,
            auto_refresh=MarketDataState.historical_auto_refresh,
            on_auto_refresh_toggle=MarketDataState.toggle_historical_auto_refresh,
        ),
        # Filter bar — ticker multi-select + date range
        _filter_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MarketDataState.filtered_historical_data,
            column_defs=_get_column_defs(),
            row_id_key="id",  # Unique row ID — enables delta updates
            enable_cell_flash=True,  # Enable for market data
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("historical_data"),
            default_csv_export_params=get_default_csv_export_params("historical_data"),
            quick_filter_text=HistoricalDataGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=MarketDataState.start_historical_auto_refresh,
    )
