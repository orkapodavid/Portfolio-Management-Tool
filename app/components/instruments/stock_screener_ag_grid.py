"""
Stock Screener AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
Includes row-level filter bars:
  - Range filters for DTL10, Market Cap (MM USD), $ADV 3M
  - Multiselect dropdown filter for Country
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
    FILTER_BTN_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class StockScreenerGridState(rx.State):
    """State for Stock Screener grid quick filter."""

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
            field="dtl10",
            header_name="DTL10",
            filter=AGFilters.number,
            min_width=80,
        ),
        ag_grid.column_def(
            field="company",
            header_name="Company",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company",
        ),
        ag_grid.column_def(
            field="country",
            header_name="Country",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="industry",
            header_name="Industry",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="mkt_cap_loc",
            header_name="Market Cap (MM LOC)",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="mkt_cap_usd",
            header_name="Market Cap (MM USD)",
            filter=AGFilters.number,
            min_width=150,
        ),
        ag_grid.column_def(
            field="adv_3m",
            header_name="ADV 3M",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="adv_3m_usd",
            header_name="$ADV 3M",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="locate_qty_mm",
            header_name="Locate Qty (MM)",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="locate_f",
            header_name="Locate F",
            filter=AGFilters.text,
            min_width=90,
        ),
    ]


# =============================================================================
# FILTER BAR COMPONENTS
# =============================================================================

_RANGE_INPUT_CLASS = (
    "h-7 w-[100px] px-2 text-[11px] bg-white border border-gray-200 rounded "
    "text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-400 "
    "focus:border-blue-400 transition-colors [appearance:textfield] "
    "[&::-webkit-outer-spin-button]:appearance-none "
    "[&::-webkit-inner-spin-button]:appearance-none"
)


def _range_filter(
    label: str,
    min_value: rx.Var[str],
    max_value: rx.Var[str],
    on_min_change,
    on_max_change,
    placeholder_min: str = "Min",
    placeholder_max: str = "Max",
) -> rx.Component:
    """A labelled min/max range filter group."""
    return rx.el.div(
        rx.el.span(label, class_name=FILTER_LABEL_CLASS),
        rx.el.input(
            type="number",
            value=min_value,
            placeholder=placeholder_min,
            on_change=on_min_change,
            class_name=_RANGE_INPUT_CLASS,
        ),
        rx.el.span("–", class_name="text-gray-400 text-[11px]"),
        rx.el.input(
            type="number",
            value=max_value,
            placeholder=placeholder_max,
            on_change=on_max_change,
            class_name=_RANGE_INPUT_CLASS,
        ),
        class_name="flex items-center gap-1.5",
    )


def _country_chip(country: str) -> rx.Component:
    """A toggleable country chip inside the dropdown."""
    is_selected = InstrumentState.screener_selected_countries.contains(country)
    return rx.el.button(
        country,
        on_click=InstrumentState.toggle_screener_country(country),
        class_name=rx.cond(
            is_selected,
            (
                "px-2.5 py-1 text-[11px] font-medium rounded-full cursor-pointer "
                "bg-blue-600 text-white border border-blue-600 transition-all"
            ),
            (
                "px-2.5 py-1 text-[11px] font-medium rounded-full cursor-pointer "
                "bg-white text-gray-600 border border-gray-200 hover:bg-gray-50 "
                "hover:border-gray-300 transition-all"
            ),
        ),
    )


def _country_multiselect() -> rx.Component:
    """Country multiselect dropdown using rx.popover for proper portal rendering."""
    count = InstrumentState.screener_selected_countries.length()

    return rx.popover.root(
        rx.popover.trigger(
            rx.el.button(
                rx.el.div(
                    rx.icon("globe", size=12, class_name="text-gray-400"),
                    rx.el.span("Country", class_name=FILTER_LABEL_CLASS),
                    rx.cond(
                        count > 0,
                        rx.el.span(
                            count.to(str),
                            class_name=(
                                "ml-1 px-1.5 py-0.5 text-[9px] font-bold bg-blue-600 "
                                "text-white rounded-full min-w-[16px] text-center"
                            ),
                        ),
                    ),
                    rx.icon("chevron-down", size=12, class_name="text-gray-400 ml-1"),
                    class_name="flex items-center gap-1.5",
                ),
                class_name=(
                    "h-7 px-2.5 bg-white border border-gray-200 rounded "
                    "hover:bg-gray-50 hover:border-gray-300 transition-all cursor-pointer "
                    "flex items-center"
                ),
            ),
        ),
        rx.popover.content(
            rx.el.div(
                rx.foreach(
                    InstrumentState.screener_available_countries,
                    _country_chip,
                ),
                class_name="flex flex-wrap gap-1.5 p-2",
            ),
            side="bottom",
            align="start",
            style={"min_width": "220px", "padding": "0"},
        ),
    )


def _screener_filter_bar() -> rx.Component:
    """Row-level filter bar with range filters and country multiselect.
    Pressing Enter in any input triggers Apply.
    """
    return rx.el.form(
        rx.el.div(
            # LEFT — Range filters + Country
            rx.el.div(
                # DTL10 range
                _range_filter(
                    "DTL10",
                    InstrumentState.screener_dtl10_min,
                    InstrumentState.screener_dtl10_max,
                    InstrumentState.set_screener_dtl10_min,
                    InstrumentState.set_screener_dtl10_max,
                    placeholder_min="0",
                    placeholder_max="30",
                ),
                # Divider
                rx.el.div(class_name="w-px h-5 bg-gray-200 mx-1"),
                # Market Cap range
                _range_filter(
                    "Mkt Cap (MM)",
                    InstrumentState.screener_mkt_cap_min,
                    InstrumentState.screener_mkt_cap_max,
                    InstrumentState.set_screener_mkt_cap_min,
                    InstrumentState.set_screener_mkt_cap_max,
                    placeholder_min="0",
                    placeholder_max="5000000",
                ),
                # Divider
                rx.el.div(class_name="w-px h-5 bg-gray-200 mx-1"),
                # $ADV 3M range
                _range_filter(
                    "$ADV 3M",
                    InstrumentState.screener_adv_3m_min,
                    InstrumentState.screener_adv_3m_max,
                    InstrumentState.set_screener_adv_3m_min,
                    InstrumentState.set_screener_adv_3m_max,
                    placeholder_min="0",
                    placeholder_max="100M",
                ),
                # Divider
                rx.el.div(class_name="w-px h-5 bg-gray-200 mx-1"),
                # Country multiselect
                _country_multiselect(),
                class_name="flex items-center gap-2",
            ),
            # RIGHT — Apply + Clear buttons
            rx.el.div(
                rx.el.button(
                    rx.icon("search", size=12),
                    rx.el.span("Apply"),
                    type="submit",
                    class_name=(
                        f"{FILTER_BTN_CLASS} bg-gradient-to-r from-blue-600 to-indigo-600 "
                        "text-white hover:shadow-md"
                    ),
                ),
                rx.cond(
                    InstrumentState.screener_filters_active,
                    rx.el.button(
                        rx.icon("x", size=12),
                        rx.el.span("Clear"),
                        type="button",
                        on_click=InstrumentState.clear_screener_filters,
                        class_name=(
                            f"{FILTER_BTN_CLASS} bg-white border border-gray-200 "
                            "text-gray-500 hover:text-red-500 hover:border-red-300"
                        ),
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        # Form submit handles both Enter key and Apply button click
        on_submit=lambda _: InstrumentState.apply_screener_filters(),
        class_name=(
            "w-full px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border border-gray-100 rounded-lg backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "stock_screener_grid_state"
_GRID_ID = "stock_screener_grid"


def stock_screener_ag_grid() -> rx.Component:
    """Stock Screener AG-Grid component with row-level filters."""
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
            page_name="stock_screener",
            search_value=StockScreenerGridState.search_text,
            on_search_change=StockScreenerGridState.set_search,
            on_search_clear=StockScreenerGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=InstrumentState.stock_screener_last_updated,
            show_refresh=True,
            on_refresh=InstrumentState.force_refresh_stock_screener,
            is_loading=InstrumentState.is_loading_stock_screener,
        ),
        # Row-level filter bar
        _screener_filter_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=InstrumentState.filtered_stock_screener,
            column_defs=_get_column_defs(),
            row_id_key="ticker",
            loading=InstrumentState.is_loading_stock_screener,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("stock_screener"),
            default_csv_export_params=get_default_csv_export_params("stock_screener"),
            quick_filter_text=StockScreenerGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
