"""
Stock Borrow AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class StockBorrowGridState(rx.State):
    """State for Stock Borrow grid quick filter."""

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
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="jpm_req",
            header_name="JPM Request Locate",
            filter=AGFilters.number,
            min_width=140,
        ),
        ag_grid.column_def(
            field="jpm_firm",
            header_name="JPM Firm Locate",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="borrow_rate",
            header_name="Borrow Rate",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="bofa_req",
            header_name="BofA Request Locate",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="bofa_firm",
            header_name="BofA Firm Locate",
            filter=AGFilters.number,
            min_width=140,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "stock_borrow_grid_state"
_GRID_ID = "stock_borrow_grid"


def stock_borrow_ag_grid() -> rx.Component:
    """Stock Borrow AG-Grid component with full toolbar support."""
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
            page_name="stock_borrow",
            search_value=StockBorrowGridState.search_text,
            on_search_change=StockBorrowGridState.set_search,
            on_search_clear=StockBorrowGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=PortfolioToolsState.stock_borrow_last_updated,
            show_refresh=True,
            on_refresh=PortfolioToolsState.force_refresh_stock_borrow,
            is_loading=PortfolioToolsState.is_loading_stock_borrow,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.stock_borrow,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=PortfolioToolsState.is_loading_stock_borrow,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("stock_borrow"),
            default_csv_export_params=get_default_csv_export_params("stock_borrow"),
            quick_filter_text=StockBorrowGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
