import reflex as rx
from app.states.portfolio_dashboard_state import PortfolioDashboardState


def sub_tab(name: str) -> rx.Component:
    """A sub-tab item with active state highlighting."""
    is_active = PortfolioDashboardState.active_subtab == name
    return rx.el.button(
        name,
        on_click=lambda: PortfolioDashboardState.set_subtab(name),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-xs font-bold text-gray-800 border-b-2 border-blue-600 bg-white transition-colors duration-150",
            "px-4 py-2 text-xs font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-colors duration-150 border-b-2 border-transparent",
        ),
    )


def workspace_controls() -> rx.Component:
    """Controls row above the data table (Date, Search, Refresh)."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Position Date:",
                    class_name="text-[10px] font-bold text-gray-500 uppercase mr-2 tracking-wide hidden sm:block",
                ),
                rx.el.input(
                    type="date",
                    on_change=PortfolioDashboardState.set_current_date,
                    class_name="bg-white border border-gray-300 rounded-md px-2 py-1 text-xs text-gray-700 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 shadow-sm",
                    default_value=PortfolioDashboardState.current_date_filter,
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    size=14,
                    class_name="text-gray-400 absolute left-2.5 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Filter results...",
                    on_change=PortfolioDashboardState.set_current_search,
                    class_name="pl-8 pr-3 py-1 bg-white border border-gray-300 rounded-md text-xs text-gray-700 w-48 sm:w-64 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 shadow-sm",
                    default_value=PortfolioDashboardState.current_search_query,
                ),
                class_name="relative",
            ),
            class_name="flex items-center gap-2 sm:gap-4 flex-wrap",
        ),
        rx.el.div(
            rx.el.span(
                "Auto-Refresh",
                class_name="text-[10px] font-bold text-gray-500 uppercase mr-2 tracking-wide hidden sm:block",
            ),
            rx.switch(
                checked=PortfolioDashboardState.current_auto_refresh,
                on_change=PortfolioDashboardState.toggle_auto_refresh,
                color_scheme="grass",
                size="1",
            ),
            class_name="flex items-center bg-white px-3 py-1 rounded-md border border-gray-200 shadow-sm",
        ),
        class_name="flex items-center justify-between px-4 py-2 bg-gray-50 border-b border-gray-200 shrink-0 flex-wrap gap-2",
    )


def table_header_cell(text: str, align: str = "left") -> rx.Component:
    """A standardized table header cell."""
    align_class = f"text-{align}"
    return rx.el.th(
        text,
        class_name=f"px-4 py-2 {align_class} text-[10px] font-bold text-gray-500 uppercase tracking-wider sticky top-0 bg-gray-50 border-b border-gray-200 z-10",
    )


def table_row(item: dict) -> rx.Component:
    """A data row for the placeholder table."""
    status_color = rx.cond(
        item["status"] == "Active",
        "bg-green-100 text-green-800",
        rx.cond(
            item["status"] == "Hedged",
            "bg-blue-100 text-blue-800",
            "bg-amber-100 text-amber-800",
        ),
    )
    pnl_color = rx.cond(item["is_positive"], "text-green-600", "text-red-600")
    reconciled_bg = rx.cond(item["is_reconciled"], "bg-green-500", "bg-red-500")
    reconciled_text = rx.cond(item["is_reconciled"], "Yes", "No")
    return rx.el.tr(
        rx.el.td(
            item["ticker"],
            class_name="px-4 py-2 text-xs font-bold text-gray-900 border-b border-gray-100",
        ),
        rx.el.td(
            item["description"],
            class_name="px-4 py-2 text-xs font-medium text-gray-600 border-b border-gray-100",
        ),
        rx.el.td(
            item["asset_class"],
            class_name="px-4 py-2 text-xs text-gray-500 border-b border-gray-100",
        ),
        rx.el.td(
            item["qty"],
            class_name="px-4 py-2 text-xs font-mono text-gray-700 text-right border-b border-gray-100",
        ),
        rx.el.td(
            item["price"],
            class_name="px-4 py-2 text-xs font-mono text-gray-700 text-right border-b border-gray-100",
        ),
        rx.el.td(
            item["mkt_value"],
            class_name="px-4 py-2 text-xs font-bold font-mono text-gray-900 text-right border-b border-gray-100",
        ),
        rx.el.td(
            item["daily_pnl"],
            class_name=f"px-4 py-2 text-xs font-bold font-mono {pnl_color} text-right border-b border-gray-100",
        ),
        rx.el.td(
            rx.el.span(
                item["status"],
                class_name=f"px-2 py-0.5 rounded-full text-[10px] font-bold {status_color}",
            ),
            class_name="px-4 py-2 text-center border-b border-gray-100",
        ),
        rx.el.td(
            rx.el.span(
                reconciled_text,
                class_name=f"px-3 py-1 rounded text-[10px] font-bold text-white {reconciled_bg}",
            ),
            class_name="px-4 py-2 text-center border-b border-gray-100",
        ),
        class_name="group transition-colors duration-75 hover:bg-[#FFF2CC] cursor-default",
    )


def mock_data_table() -> rx.Component:
    """A robust placeholder table component."""
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    table_header_cell("Ticker"),
                    table_header_cell("Description"),
                    table_header_cell("Class"),
                    table_header_cell("Quantity", "right"),
                    table_header_cell("Price", "right"),
                    table_header_cell("Mkt Value", "right"),
                    table_header_cell("Daily PnL", "right"),
                    table_header_cell("Status", "center"),
                    table_header_cell("Reconciled", "center"),
                )
            ),
            rx.el.tbody(rx.foreach(PortfolioDashboardState.mock_table_data, table_row)),
            class_name="w-full table-auto border-collapse",
        ),
        class_name="overflow-auto flex-1 w-full bg-white relative",
    )


def contextual_workspace() -> rx.Component:
    """The main workspace area (Region 3)."""
    active_page_name = rx.cond(
        PortfolioDashboardState.active_subtab != "",
        PortfolioDashboardState.active_subtab,
        PortfolioDashboardState.active_module,
    )
    return rx.el.div(
        rx.el.div(
            rx.foreach(PortfolioDashboardState.current_subtabs, sub_tab),
            class_name="flex items-center bg-white border-b border-gray-200 px-2 pt-1 overflow-x-auto shrink-0",
        ),
        rx.el.div(
            workspace_controls(),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        active_page_name,
                        class_name="text-lg font-bold text-gray-800 mb-4 px-6 pt-6",
                    ),
                    rx.el.div(
                        mock_data_table(),
                        class_name="flex-1 overflow-hidden border border-gray-200 rounded-lg mx-6 mb-4 shadow-sm bg-white flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.button(
                            f"Generate {active_page_name}",
                            on_click=lambda: PortfolioDashboardState.handle_generate(
                                active_page_name
                            ),
                            class_name="bg-blue-600 text-white px-8 py-2.5 rounded-md shadow hover:bg-blue-700 hover:shadow-lg transition-all duration-200 text-xs font-bold uppercase tracking-wide",
                        ),
                        class_name="flex justify-center pb-6 shrink-0",
                    ),
                    class_name="flex flex-col h-full overflow-hidden",
                ),
                class_name="flex-1 bg-white overflow-hidden flex flex-col",
            ),
            class_name="flex flex-col flex-1 min-h-0 overflow-hidden",
        ),
        class_name="flex flex-col flex-1 h-full min-h-0 bg-white overflow-hidden",
    )