"""
Stock Position AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.positions.positions_state import PositionsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class StockPositionGridState(rx.State):
    """State for Stock Position grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the stock position grid."""
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
            field="deal_num",
            header_name="Deal Num",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="detail_id",
            header_name="Detail ID",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="sec_id",
            header_name="SecID",
            filter=AGFilters.text,
            min_width=90,
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
            field="account_id",
            header_name="Account ID",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="pos_loc",
            header_name="Pos Loc",
            filter="agSetColumnFilter",
            min_width=130,
        ),
        ag_grid.column_def(
            field="notional",
            header_name="Notional",
            filter=AGFilters.number,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "stock_position_grid_state"
_GRID_ID = "stock_position_grid"


def stock_position_ag_grid() -> rx.Component:
    """Stock Position AG-Grid component with full toolbar support."""
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
            page_name="stock_position",
            search_value=StockPositionGridState.search_text,
            on_search_change=StockPositionGridState.set_search,
            on_search_clear=StockPositionGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=PositionsState.stock_positions_last_updated,
            auto_refresh=PositionsState.stock_positions_auto_refresh,
            on_auto_refresh_toggle=PositionsState.toggle_stock_positions_auto_refresh,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PositionsState.filtered_stock_positions,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("stock_position"),
            default_csv_export_params=get_default_csv_export_params("stock_position"),
            quick_filter_text=StockPositionGridState.search_text,
            row_id_key="id",
            enable_cell_flash=True,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=PositionsState.start_stock_positions_auto_refresh,
    )
