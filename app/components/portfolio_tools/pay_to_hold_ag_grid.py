"""
Pay To Hold AG-Grid Component.

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


class PayToHoldGridState(rx.State):
    """State for Pay To Hold grid quick filter."""

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
            field="currency",
            header_name="Currency",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="counter_party",
            header_name="Counter Party",
            filter="agSetColumnFilter",
            min_width=120,
        ),
        ag_grid.column_def(
            field="side",
            header_name="Side",
            filter="agSetColumnFilter",
            min_width=70,
        ),
        ag_grid.column_def(
            field="sl_rate",
            header_name="SL Rate",
            filter=AGFilters.number,
            min_width=80,
        ),
        ag_grid.column_def(
            field="pth_amount_sod",
            header_name="PTH Amount SOD",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="pth_amount",
            header_name="PTH Amount",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="emsx_order",
            header_name="EMSX ORDER AMOUNT",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="emsx_remark",
            header_name="EMSX Order Remark",
            filter=AGFilters.text,
            min_width=140,
            tooltip_field="emsx_remark",
        ),
        ag_grid.column_def(
            field="emsx_working",
            header_name="EMSX Working",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="emsx_order_col",
            header_name="EMSX ORDER CONFIRMED",
            filter=AGFilters.number,
            min_width=160,
        ),
        ag_grid.column_def(
            field="emsx_filled",
            header_name="EMSX ORDER FILLED",
            filter=AGFilters.number,
            min_width=150,
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
                    value=PortfolioToolsState.pay_to_hold_position_date,
                    on_change=PortfolioToolsState.set_pay_to_hold_position_date,
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

_STORAGE_KEY = "pay_to_hold_grid_state"
_GRID_ID = "pay_to_hold_grid"


def pay_to_hold_ag_grid() -> rx.Component:
    """Pay To Hold AG-Grid component with full toolbar support."""
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
            page_name="pay_to_hold",
            search_value=PayToHoldGridState.search_text,
            on_search_change=PayToHoldGridState.set_search,
            on_search_clear=PayToHoldGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=PortfolioToolsState.pay_to_hold_last_updated,
            show_refresh=True,
            on_refresh=PortfolioToolsState.force_refresh_pay_to_hold,
            is_loading=PortfolioToolsState.is_loading_pay_to_hold,
        ),
        # Position date selector bar
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.pay_to_hold,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=PortfolioToolsState.is_loading_pay_to_hold,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pay_to_hold"),
            default_csv_export_params=get_default_csv_export_params("pay_to_hold"),
            quick_filter_text=PayToHoldGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
