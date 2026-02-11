"""
Failed Trades AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.reconciliation.reconciliation_state import ReconciliationState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class FailedTradesGridState(rx.State):
    """State for Failed Trades grid quick filter."""

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
            field="report_date",
            header_name="Report Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="value_date",
            header_name="Value Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="settlement_date",
            header_name="Settlement Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="portfolio_code",
            header_name="Portfolio Code",
            filter="agSetColumnFilter",
            min_width=110,
        ),
        ag_grid.column_def(
            field="instrument_ref",
            header_name="Instrument Ref",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="instrument_name",
            header_name="Instrument Name",
            filter=AGFilters.text,
            min_width=130,
            tooltip_field="instrument_name",
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="isin",
            header_name="ISIN",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="sedol",
            header_name="SEDOL",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="broker",
            header_name="Broker",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="glass_reference",
            header_name="Glass Reference",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="trade_reference",
            header_name="Trade Reference",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="deal_type",
            header_name="Deal Type",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="q",
            header_name="Q",
            filter=AGFilters.number,
            min_width=60,
        ),
    ]


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span("POSITION DATE", class_name=FILTER_LABEL_CLASS),
                rx.el.input(
                    type="date",
                    value=ReconciliationState.failed_trades_position_date,
                    on_change=ReconciliationState.set_failed_trades_position_date,
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

_STORAGE_KEY = "failed_trades_grid_state"
_GRID_ID = "failed_trades_grid"


def failed_trades_ag_grid() -> rx.Component:
    """Failed Trades AG-Grid component with full toolbar support."""
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
            page_name="failed_trades",
            search_value=FailedTradesGridState.search_text,
            on_search_change=FailedTradesGridState.set_search,
            on_search_clear=FailedTradesGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Force refresh pattern
            show_refresh=True,
            on_refresh=ReconciliationState.force_refresh_failed_trades,
            is_loading=ReconciliationState.is_loading_failed_trades,
            last_updated=ReconciliationState.failed_trades_last_updated,
        ),
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=ReconciliationState.filtered_failed_trades,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("failed_trades"),
            default_csv_export_params=get_default_csv_export_params("failed_trades"),
            quick_filter_text=FailedTradesGridState.search_text,
            row_id_key="id",
            enable_cell_flash=True,
            loading=ReconciliationState.is_loading_failed_trades,
            overlay_loading_template="<span class='ag-overlay-loading-center'>Refreshing data...</span>",
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
