"""
Trading Calendar AG-Grid Component.

Migrated to use create_standard_grid factory with cell flash and full toolbar support.
Includes a FROM/TO date range filter bar.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    filter_date_range_bar,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class TradingCalendarGridState(rx.State):
    """State for Trading Calendar grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# CELL STYLES
# =============================================================================

# Market status style - green for open, red for closed
_MARKET_STATUS_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const isOpen = val.includes('open') || val === 'o' || val === '1';
        if (!val || val === '-') return {};
        return {
            backgroundColor: isOpen ? '#d1fae5' : '#fee2e2',
            color: isOpen ? '#065f46' : '#991b1b',
            padding: '2px 8px',
            borderRadius: '9999px',
            fontSize: '11px',
            fontWeight: '500',
            display: 'inline-block'
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the trading calendar grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=110,
            pinned="left",
        ),
        ag_grid.column_def(
            field="day_of_week",
            header_name="Day of Week",
            filter="agSetColumnFilter",
            min_width=110,
        ),
        ag_grid.column_def(
            field="usa",
            header_name="USA",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="hkg",
            header_name="HKG",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="jpn",
            header_name="JPN",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="aus",
            header_name="AUS",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="nzl",
            header_name="NZL",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="kor",
            header_name="KOR",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="chn",
            header_name="CHN",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="twn",
            header_name="TWN",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="ind",
            header_name="IND",
            filter="agSetColumnFilter",
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
    ]


# =============================================================================
# FILTER BAR — Date range pickers (uses shared filter_date_range_bar)
# =============================================================================


def _filter_bar() -> rx.Component:
    """Filter bar with FROM / TO date pickers."""
    return filter_date_range_bar(
        from_value=MarketDataState.trading_calendar_from_date,
        to_value=MarketDataState.trading_calendar_to_date,
        on_from_change=MarketDataState.set_trading_calendar_from_date,
        on_to_change=MarketDataState.set_trading_calendar_to_date,
        on_apply=MarketDataState.apply_trading_calendar_filters,
        has_active_filters=MarketDataState.trading_calendar_has_active_filters,
        on_clear=MarketDataState.clear_trading_calendar_filters,
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "trading_calendar_grid_state"
_GRID_ID = "trading_calendar_grid"


def trading_calendar_ag_grid() -> rx.Component:
    """Trading Calendar AG-Grid component with cell flash and full toolbar support."""
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
            page_name="trading_calendar",
            search_value=TradingCalendarGridState.search_text,
            on_search_change=TradingCalendarGridState.set_search,
            on_search_clear=TradingCalendarGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Force refresh button for static data (instead of auto-refresh toggle)
            show_refresh=True,
            on_refresh=MarketDataState.force_refresh_trading_calendar,
            is_loading=MarketDataState.is_loading_trading_calendar,
            # Status bar — timestamp from mixin
            last_updated=MarketDataState.trading_calendar_last_updated,
        ),
        # Filter bar — date range pickers
        _filter_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MarketDataState.trading_calendar,
            column_defs=_get_column_defs(),
            row_id_key="id",  # Unique row ID — enables delta updates
            enable_cell_flash=True,  # Enable for market data
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("trading_calendar"),
            default_csv_export_params=get_default_csv_export_params("trading_calendar"),
            quick_filter_text=TradingCalendarGridState.search_text,
            # Loading overlay for refresh feedback
            loading=MarketDataState.is_loading_trading_calendar,
            overlay_loading_template="<span class='ag-overlay-loading-center'>Refreshing data...</span>",
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=MarketDataState.load_trading_calendar,
    )

