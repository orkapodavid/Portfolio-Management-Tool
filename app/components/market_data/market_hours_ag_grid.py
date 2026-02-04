"""
Market Hours AG-Grid Component.

Migrated to use create_standard_grid factory with cell flash and full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class MarketHoursGridState(rx.State):
    """State for Market Hours grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# CELL STYLES
# =============================================================================

# Is Open style - badge
_IS_OPEN_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const isOpen = val === 'yes' || val === 'true' || val === '1' || val === 'open';
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
    """Return column definitions for the market hours grid."""
    return [
        ag_grid.column_def(
            field="market",
            header_name="Market",
            filter="agSetColumnFilter",
            min_width=100,
            pinned="left",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="ticker",
        ),
        ag_grid.column_def(
            field="session",
            header_name="Session",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="local_time",
            header_name="Local Time",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="session_period",
            header_name="Session Period",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="is_open",
            header_name="Is Open?",
            filter="agSetColumnFilter",
            min_width=100,
            cell_style=_IS_OPEN_STYLE,
        ),
        ag_grid.column_def(
            field="timezone",
            header_name="Timezone",
            filter="agSetColumnFilter",
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "market_hours_grid_state"
_GRID_ID = "market_hours_grid"


def market_hours_ag_grid() -> rx.Component:
    """Market Hours AG-Grid component with cell flash and full toolbar support."""
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
            page_name="market_hours",
            search_value=MarketHoursGridState.search_text,
            on_search_change=MarketHoursGridState.set_search,
            on_search_clear=MarketHoursGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MarketDataState.market_hours,
            column_defs=_get_column_defs(),
            enable_cell_flash=True,  # Enable for market data
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("market_hours"),
            default_csv_export_params=get_default_csv_export_params("market_hours"),
            quick_filter_text=MarketHoursGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
