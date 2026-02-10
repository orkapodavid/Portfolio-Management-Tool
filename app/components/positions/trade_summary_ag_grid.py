"""
Trade Summary AG-Grid Component.

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


class TradeSummaryGridState(rx.State):
    """State for Trade Summary grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the trade summary grid."""
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
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="account_id",
            header_name="Account ID",
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
            field="subtype",
            header_name="Subtype",
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
            field="closing_date",
            header_name="Closing Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="divisor",
            header_name="Divisor",
            filter=AGFilters.number,
            min_width=80,
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
                    value=PositionsState.trade_summary_position_date,
                    on_change=PositionsState.set_trade_summary_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border border-gray-100 rounded-lg backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "trade_summary_grid_state"
_GRID_ID = "trade_summary_grid"


def trade_summary_ag_grid() -> rx.Component:
    """
    Trade Summary AG-Grid component with full toolbar support.

    Displays trade summary data with:
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
            page_name="trade_summary",
            search_value=TradeSummaryGridState.search_text,
            on_search_change=TradeSummaryGridState.set_search,
            on_search_clear=TradeSummaryGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=PositionsState.trade_summary_last_updated,
            auto_refresh=PositionsState.trade_summary_auto_refresh,
            on_auto_refresh_toggle=PositionsState.toggle_trade_summary_auto_refresh,
            # Refresh button
            show_refresh=True,
            on_refresh=PositionsState.force_refresh_trade_summary,
            is_loading=PositionsState.is_loading_trade_summaries,
        ),
        # Position date selector bar
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PositionsState.filtered_trade_summaries,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("trade_summary"),
            default_csv_export_params=get_default_csv_export_params("trade_summary"),
            quick_filter_text=TradeSummaryGridState.search_text,
            row_id_key="id",
            enable_cell_flash=True,
            loading=PositionsState.is_loading_trade_summaries,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=PositionsState.start_trade_summary_auto_refresh,
    )
