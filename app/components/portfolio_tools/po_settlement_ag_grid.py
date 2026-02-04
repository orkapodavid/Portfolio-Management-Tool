"""
PO Settlement AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class PoSettlementGridState(rx.State):
    """State for PO Settlement grid quick filter."""

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
            field="deal_num",
            header_name="Deal Num",
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
            field="structure",
            header_name="Structure",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="fx_rate",
            header_name="FX Rate",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="current_position",
            header_name="Current Position",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="shares_allocated",
            header_name="Shares Allocated",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="shares_swap",
            header_name="Shares in Swap",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="shares_hedged",
            header_name="Shares Hedged",
            filter=AGFilters.number,
            min_width=120,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "po_settlement_grid_state"
_GRID_ID = "po_settlement_grid"


def po_settlement_ag_grid() -> rx.Component:
    """PO Settlement AG-Grid component with full toolbar support."""
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
            page_name="po_settlement",
            search_value=PoSettlementGridState.search_text,
            on_search_change=PoSettlementGridState.set_search,
            on_search_clear=PoSettlementGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.filtered_po_settlement,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("po_settlement"),
            default_csv_export_params=get_default_csv_export_params("po_settlement"),
            quick_filter_text=PoSettlementGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
