"""
CB Installments AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class CbInstallmentsGridState(rx.State):
    """State for CB Installments grid quick filter."""

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
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="installment_date",
            header_name="Installment Date",
            filter=AGFilters.date,
            min_width=130,
        ),
        ag_grid.column_def(
            field="total_amount",
            header_name="Total Amount",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="outstanding",
            header_name="Outstanding Amount",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="redeemed",
            header_name="Redeemed Amount",
            filter=AGFilters.number,
            min_width=140,
        ),
        ag_grid.column_def(
            field="deferred",
            header_name="Deferred Amount",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="converted",
            header_name="Converted Amount",
            filter=AGFilters.number,
            min_width=140,
        ),
        ag_grid.column_def(
            field="installment_amount",
            header_name="Installment Amount",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="period",
            header_name="Period",
            filter="agSetColumnFilter",
            min_width=80,
        ),
    ]


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar — full-width background."""
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
                    value=PortfolioToolsState.cb_installments_position_date,
                    on_change=PortfolioToolsState.set_cb_installments_position_date,
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

_STORAGE_KEY = "cb_installments_grid_state"
_GRID_ID = "cb_installments_grid"


def cb_installments_ag_grid() -> rx.Component:
    """CB Installments AG-Grid component with full toolbar support."""
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
            page_name="cb_installments",
            search_value=CbInstallmentsGridState.search_text,
            on_search_change=CbInstallmentsGridState.set_search,
            on_search_clear=CbInstallmentsGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=PortfolioToolsState.cb_installments_last_updated,
            show_refresh=True,
            on_refresh=PortfolioToolsState.force_refresh_cb_installments,
            is_loading=PortfolioToolsState.is_loading_cb_installments,
        ),
        # Position date selector bar
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.cb_installments,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=PortfolioToolsState.is_loading_cb_installments,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("cb_installments"),
            default_csv_export_params=get_default_csv_export_params("cb_installments"),
            quick_filter_text=CbInstallmentsGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
