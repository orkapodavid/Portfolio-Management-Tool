"""
Positions AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
Includes a position date selector that triggers database reload.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.positions.positions_state import PositionsState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    filter_date_input,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class PositionsGridState(rx.State):
    """State for Positions grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the positions grid."""
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
            field="account_id",
            header_name="Account ID",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="pos_loc",
            header_name="Pos Loc",
            filter="agSetColumnFilter",
            min_width=80,
        ),
        ag_grid.column_def(
            field="notional",
            header_name="Notional",
            filter=AGFilters.number,
            min_width=120,
        ),
    ]


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar — triggers data reload on change."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span(
                    "POSITION DATE",
                    class_name=FILTER_LABEL_CLASS,
                ),
                rx.el.input(
                    type="date",
                    value=PositionsState.positions_position_date,
                    on_change=PositionsState.set_positions_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "w-full px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border-b border-gray-100 backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "positions_grid_state"
_GRID_ID = "positions_grid"


def positions_ag_grid() -> rx.Component:
    """
    Positions AG-Grid component with full toolbar support.

    Displays positions data with:
    - Position date selector (defaults to today, auto-reloads on change)
    - Quick filter search across all columns
    - Excel export button
    - Full grid state persistence (columns + filters + sort)
    - Status bar with row counts
    - Compact mode toggle
    """
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
            page_name="positions",
            search_value=PositionsGridState.search_text,
            on_search_change=PositionsGridState.set_search,
            on_search_clear=PositionsGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=PositionsState.positions_last_updated,
            auto_refresh=PositionsState.positions_auto_refresh,
            on_auto_refresh_toggle=PositionsState.toggle_positions_auto_refresh,
            # Refresh button
            show_refresh=True,
            on_refresh=PositionsState.force_refresh_positions,
            is_loading=PositionsState.is_loading_positions,
        ),
        # Position date selector bar
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PositionsState.filtered_positions,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("positions"),
            default_csv_export_params=get_default_csv_export_params("positions"),
            quick_filter_text=PositionsGridState.search_text,
            row_id_key="ticker",
            enable_cell_flash=True,
            loading=PositionsState.is_loading_positions,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=PositionsState.start_positions_auto_refresh,
    )
