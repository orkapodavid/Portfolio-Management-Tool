"""
Stock Screener AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class StockScreenerGridState(rx.State):
    """State for Stock Screener grid quick filter."""

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
            field="otl",
            header_name="OTL",
            filter=AGFilters.text,
            min_width=70,
        ),
        ag_grid.column_def(
            field="mkt_cap_37_pct",
            header_name="37% Market Cap",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="company",
            header_name="Company",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company",
        ),
        ag_grid.column_def(
            field="country",
            header_name="Country",
            filter="agSetColumnFilter",  # Categorical
            min_width=90,
        ),
        ag_grid.column_def(
            field="industry",
            header_name="Industry",
            filter="agSetColumnFilter",  # Categorical
            min_width=100,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="mkt_cap_loc",
            header_name="Market Cap (MM LOC)",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="mkt_cap_usd",
            header_name="Market Cap (MM USD)",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="adv_3m",
            header_name="ADV 3M",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="locate_qty_mm",
            header_name="Locate Qty (MM)",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="locate_f",
            header_name="Locate F",
            filter=AGFilters.text,
            min_width=90,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "stock_screener_grid_state"
_GRID_ID = "stock_screener_grid"


def stock_screener_ag_grid() -> rx.Component:
    """Stock Screener AG-Grid component with full toolbar support."""
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
            page_name="stock_screener",
            search_value=StockScreenerGridState.search_text,
            on_search_change=StockScreenerGridState.set_search,
            on_search_clear=StockScreenerGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=InstrumentState.filtered_stock_screener,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("stock_screener"),
            default_csv_export_params=get_default_csv_export_params("stock_screener"),
            quick_filter_text=StockScreenerGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
