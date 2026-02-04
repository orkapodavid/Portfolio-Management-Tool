"""
Coming Resets AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class ComingResetsGridState(rx.State):
    """State for Coming Resets grid quick filter."""

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
            field="detail_id",
            header_name="Detail ID",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="account",
            header_name="Account",
            filter="agSetColumnFilter",
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
            field="announce_date",
            header_name="Announcement Date",
            filter=AGFilters.date,
            min_width=140,
        ),
        ag_grid.column_def(
            field="closing_date",
            header_name="Closing Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="cal_days",
            header_name="Cal Days Since Announced",
            filter=AGFilters.number,
            min_width=180,
        ),
        ag_grid.column_def(
            field="biz_days",
            header_name="Biz Days Since Announced",
            filter=AGFilters.number,
            min_width=180,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "coming_resets_grid_state"
_GRID_ID = "coming_resets_grid"


def coming_resets_ag_grid() -> rx.Component:
    """Coming Resets AG-Grid component with full toolbar support."""
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
            page_name="coming_resets",
            search_value=ComingResetsGridState.search_text,
            on_search_change=ComingResetsGridState.set_search,
            on_search_clear=ComingResetsGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.filtered_coming_resets,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("coming_resets"),
            default_csv_export_params=get_default_csv_export_params("coming_resets"),
            quick_filter_text=ComingResetsGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
