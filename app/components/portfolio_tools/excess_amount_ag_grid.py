"""
Excess Amount AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class ExcessAmountGridState(rx.State):
    """State for Excess Amount grid quick filter."""

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
            field="warrants",
            header_name="Warrants",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="excess_amount",
            header_name="Excess Amount",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="threshold",
            header_name="Excess Amount Threshold",
            filter=AGFilters.number,
            min_width=170,
        ),
        ag_grid.column_def(
            field="cb_redeem",
            header_name="CB Redeem/Converted Amt",
            filter=AGFilters.number,
            min_width=180,
        ),
        ag_grid.column_def(
            field="redeem",
            header_name="Redeem/Converted Amt",
            filter=AGFilters.number,
            min_width=160,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "excess_amount_grid_state"
_GRID_ID = "excess_amount_grid"


def excess_amount_ag_grid() -> rx.Component:
    """Excess Amount AG-Grid component with full toolbar support."""
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
            page_name="excess_amount",
            search_value=ExcessAmountGridState.search_text,
            on_search_change=ExcessAmountGridState.set_search,
            on_search_clear=ExcessAmountGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.filtered_excess_amount,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("excess_amount"),
            default_csv_export_params=get_default_csv_export_params("excess_amount"),
            quick_filter_text=ExcessAmountGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
