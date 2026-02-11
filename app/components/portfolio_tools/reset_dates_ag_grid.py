"""
Reset Dates AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
Includes filter bar with ticker, date range, frequency, month, day, and up/down dropdowns.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
    FILTER_BTN_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class ResetDatesGridState(rx.State):
    """State for Reset Dates grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# HELPER — styled select dropdown
# =============================================================================


def _select(value, on_change, options: list[str], width: str = "w-[140px]") -> rx.Component:
    """Render a styled <select> dropdown."""
    return rx.el.select(
        *[rx.el.option(opt, value=opt) for opt in options],
        value=value,
        on_change=on_change,
        class_name=f"{FILTER_INPUT_CLASS} {width}",
    )


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            pinned="left",
            sortable=True,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=140,
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
            field="sec_type",
            header_name="Sec Type",
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
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="first_reset",
            header_name="First Reset Date",
            filter=AGFilters.date,
            min_width=130,
        ),
        ag_grid.column_def(
            field="expiry",
            header_name="Expiry Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="latest_reset",
            header_name="Latest Reset Date",
            filter=AGFilters.date,
            min_width=130,
        ),
        ag_grid.column_def(
            field="reset_date",
            header_name="Reset Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="reset_up_down",
            header_name="Reset Up/Down",
            filter="agSetColumnFilter",
            min_width=120,
        ),
    ]


# =============================================================================
# FILTER BAR
# =============================================================================

_FREQUENCY_OPTIONS = ["semiannually", "annually", "quarterly", "monthly"]
_MONTH_OPTIONS = [str(m) for m in range(1, 13)]
_DAY_OPTIONS = [str(d) for d in range(1, 32)]
_UP_DOWN_OPTIONS = ["up and down", "up", "down"]
_TICKER_OPTIONS = [
    "4592 JP_Series 1",
    "9984 JP_Series 2",
    "6758 JP_Series 1",
    "7203 JP_Series 1",
]


def _filter_bar() -> rx.Component:
    """Two-row filter bar matching the reference design."""
    return rx.el.div(
        # ── Row 1: Select Ticker ──
        rx.el.div(
            rx.el.div(
                rx.icon("tag", size=14, class_name="text-gray-400"),
                rx.el.span("SELECT TICKER", class_name=FILTER_LABEL_CLASS),
                _select(
                    value=PortfolioToolsState.reset_dates_ticker,
                    on_change=PortfolioToolsState.set_reset_dates_ticker,
                    options=_TICKER_OPTIONS,
                    width="w-[180px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center gap-4 w-full",
        ),
        # ── Row 2: Date range + Frequency + Month + Day + Up/Down ──
        rx.el.div(
            # Start/End Date
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span("START/END DATE", class_name=FILTER_LABEL_CLASS),
                rx.el.input(
                    type="date",
                    value=PortfolioToolsState.reset_dates_start_date,
                    on_change=PortfolioToolsState.set_reset_dates_start_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[140px]",
                ),
                rx.el.span("TO", class_name="text-[10px] text-gray-400 font-medium"),
                rx.el.input(
                    type="date",
                    value=PortfolioToolsState.reset_dates_end_date,
                    on_change=PortfolioToolsState.set_reset_dates_end_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[140px]",
                ),
                class_name="flex items-center gap-2",
            ),
            # Reset Frequency
            rx.el.div(
                rx.el.span("RESET FREQ", class_name=FILTER_LABEL_CLASS),
                _select(
                    value=PortfolioToolsState.reset_dates_frequency,
                    on_change=PortfolioToolsState.set_reset_dates_frequency,
                    options=_FREQUENCY_OPTIONS,
                    width="w-[130px]",
                ),
                class_name="flex items-center gap-2",
            ),
            # Reset Month
            rx.el.div(
                rx.el.span("RESET MONTH", class_name=FILTER_LABEL_CLASS),
                _select(
                    value=PortfolioToolsState.reset_dates_month,
                    on_change=PortfolioToolsState.set_reset_dates_month,
                    options=_MONTH_OPTIONS,
                    width="w-[60px]",
                ),
                class_name="flex items-center gap-2",
            ),
            # Reset on Day
            rx.el.div(
                rx.el.span("RESET ON DAY", class_name=FILTER_LABEL_CLASS),
                _select(
                    value=PortfolioToolsState.reset_dates_day,
                    on_change=PortfolioToolsState.set_reset_dates_day,
                    options=_DAY_OPTIONS,
                    width="w-[60px]",
                ),
                class_name="flex items-center gap-2",
            ),
            # Reset Up/Down
            rx.el.div(
                rx.el.span("UP/DOWN", class_name=FILTER_LABEL_CLASS),
                _select(
                    value=PortfolioToolsState.reset_dates_up_down,
                    on_change=PortfolioToolsState.set_reset_dates_up_down,
                    options=_UP_DOWN_OPTIONS,
                    width="w-[120px]",
                ),
                class_name="flex items-center gap-2",
            ),
            # Apply button
            rx.el.button(
                rx.icon("search", size=12),
                rx.el.span("Apply"),
                on_click=PortfolioToolsState.apply_reset_dates_filters,
                class_name=(
                    f"{FILTER_BTN_CLASS} bg-gradient-to-r from-blue-600 to-indigo-600 "
                    "text-white hover:shadow-md"
                ),
            ),
            class_name="flex items-center gap-4 flex-wrap w-full",
        ),
        class_name=(
            "w-full px-3 py-2 flex flex-col gap-2 "
            "bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border-b border-gray-100 backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "reset_dates_grid_state"
_GRID_ID = "reset_dates_grid"


def reset_dates_ag_grid() -> rx.Component:
    """Reset Dates AG-Grid component with full toolbar support."""
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
            page_name="reset_dates",
            search_value=ResetDatesGridState.search_text,
            on_search_change=ResetDatesGridState.set_search,
            on_search_clear=ResetDatesGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=PortfolioToolsState.reset_dates_last_updated,
            show_refresh=True,
            on_refresh=PortfolioToolsState.force_refresh_reset_dates,
            is_loading=PortfolioToolsState.is_loading_reset_dates,
        ),
        _filter_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=PortfolioToolsState.reset_dates,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=PortfolioToolsState.is_loading_reset_dates,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("reset_dates"),
            default_csv_export_params=get_default_csv_export_params("reset_dates"),
            quick_filter_text=ResetDatesGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
