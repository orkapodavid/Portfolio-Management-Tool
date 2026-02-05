"""
Short ECL AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class ShortEclGridState(rx.State):
    """State for Short ECL grid quick filter."""

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
            field="pos_loc",
            header_name="Pos Loc",
            filter="agSetColumnFilter",
            min_width=80,
        ),
        ag_grid.column_def(
            field="account",
            header_name="Account",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="short_position",
            header_name="Short Position",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="nosh",
            header_name="NOSH",
            filter=AGFilters.number,
            min_width=80,
        ),
        ag_grid.column_def(
            field="short_ownership",
            header_name="Short Ownership",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="last_volume",
            header_name="Last Volume",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="short_pos_truncated",
            header_name="ShortPos/Volume",
            filter=AGFilters.number,
            min_width=150,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "short_ecl_grid_state"
_GRID_ID = "short_ecl_grid"


def short_ecl_ag_grid() -> rx.Component:
    """Short ECL AG-Grid component with full toolbar support."""
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
            page_name="short_ecl",
            search_value=ShortEclGridState.search_text,
            on_search_change=ShortEclGridState.set_search,
            on_search_clear=ShortEclGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=PortfolioToolsState.short_ecl_last_updated,
            show_refresh=True,
            on_refresh=PortfolioToolsState.force_refresh_short_ecl,
            is_loading=PortfolioToolsState.is_loading_short_ecl,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.short_ecl,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=PortfolioToolsState.is_loading_short_ecl,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("short_ecl"),
            default_csv_export_params=get_default_csv_export_params("short_ecl"),
            quick_filter_text=ShortEclGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
