"""
Reset Dates AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class ResetDatesGridState(rx.State):
    """State for Reset Dates grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            pinned="left",
            tooltip_field="ticker",
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="first_reset",
            header_name="First Reset Date",
            filter=AGFilters.date,
            min_width=130,
        ),
        ag_grid.column_def(
            field="expiry",
            header_name="Expiry Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="latest_reset",
            header_name="Latest Reset Date",
            filter=AGFilters.date,
            min_width=130,
        ),
        ag_grid.column_def(
            field="reset_up_down",
            header_name="Reset Up/Down",
            filter="agSetColumnFilter",
            min_width=120,
        ),
        ag_grid.column_def(
            field="market_price",
            header_name="Market Price",
            filter=AGFilters.number,
            min_width=110,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "reset_dates_grid_state"
_GRID_ID = "reset_dates_grid"


def reset_dates_ag_grid() -> rx.Component:
    """Reset Dates AG-Grid component with full toolbar support."""
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
            page_name="reset_dates",
            search_value=ResetDatesGridState.search_text,
            on_search_change=ResetDatesGridState.set_search,
            on_search_clear=ResetDatesGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.filtered_reset_dates,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("reset_dates"),
            default_csv_export_params=get_default_csv_export_params("reset_dates"),
            quick_filter_text=ResetDatesGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
