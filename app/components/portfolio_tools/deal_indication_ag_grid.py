"""
Deal Indication AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class DealIndicationGridState(rx.State):
    """State for Deal Indication grid quick filter."""

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
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="identification",
            header_name="Identification",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="deal_type",
            header_name="Deal Type",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="agent",
            header_name="Agent",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="captain",
            header_name="Deal Captain",
            filter="agSetColumnFilter",
            min_width=110,
        ),
        ag_grid.column_def(
            field="indication_date",
            header_name="Indication Date",
            filter=AGFilters.date,
            min_width=120,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="market_cap_loc",
            header_name="Market Cap LOC",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="gross_proceed_loc",
            header_name="Gross Proceed LOC",
            filter=AGFilters.number,
            min_width=140,
        ),
        ag_grid.column_def(
            field="indication_amount",
            header_name="Indication Amount",
            filter=AGFilters.number,
            min_width=140,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "deal_indication_grid_state"
_GRID_ID = "deal_indication_grid"


def deal_indication_ag_grid() -> rx.Component:
    """Deal Indication AG-Grid component with full toolbar support."""
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
            page_name="deal_indication",
            search_value=DealIndicationGridState.search_text,
            on_search_change=DealIndicationGridState.set_search,
            on_search_clear=DealIndicationGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.filtered_deal_indication,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("deal_indication"),
            default_csv_export_params=get_default_csv_export_params("deal_indication"),
            quick_filter_text=DealIndicationGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
