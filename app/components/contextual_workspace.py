import reflex as rx
from app.states.portfolio_dashboard_state import PortfolioDashboardState
from app.components.summary_cards import portfolio_summary


def sub_tab(name: str) -> rx.Component:
    """A sub-tab item with active state highlighting."""
    is_active = PortfolioDashboardState.active_subtab == name
    return rx.el.button(
        name,
        on_click=PortfolioDashboardState.set_subtab(name),
        class_name=rx.cond(
            is_active,
            "px-2 py-0 text-[10px] font-bold text-gray-800 border-b-2 border-blue-600 bg-white transition-colors duration-150 h-[28px]",
            "px-2 py-0 text-[10px] font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-colors duration-150 border-b-2 border-transparent h-[28px]",
        ),
    )


def workspace_controls() -> rx.Component:
    """Merged controls row with summary cards."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Date:",
                    class_name="text-[10px] font-bold text-gray-500 uppercase mr-2 tracking-wide",
                ),
                rx.el.input(
                    type="date",
                    on_change=PortfolioDashboardState.set_current_date,
                    class_name="bg-white border border-gray-300 rounded px-2 py-0 text-[10px] text-gray-700 focus:outline-none focus:border-blue-500 shadow-sm h-6",
                    default_value=PortfolioDashboardState.current_date_filter,
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    size=12,
                    class_name="text-gray-400 absolute left-2 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Filter...",
                    on_change=PortfolioDashboardState.set_current_search,
                    class_name="pl-7 pr-2 py-0 bg-white border border-gray-300 rounded text-[10px] text-gray-700 w-32 focus:outline-none focus:border-blue-500 shadow-sm h-6",
                    default_value=PortfolioDashboardState.current_search_query,
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.span(
                    "Refresh",
                    class_name="text-[10px] font-bold text-gray-500 uppercase mr-2 tracking-wide",
                ),
                rx.switch(
                    checked=PortfolioDashboardState.current_auto_refresh,
                    on_change=PortfolioDashboardState.toggle_auto_refresh,
                    color_scheme="grass",
                    size="1",
                ),
                class_name="flex items-center bg-white px-2 py-0 rounded border border-gray-200 shadow-sm h-6",
            ),
            class_name="flex items-center gap-2",
        ),
        portfolio_summary(),
        class_name="flex items-center justify-between px-2 py-0.5 bg-gray-50 border-b border-gray-200 shrink-0 h-[36px]",
    )


def table_header_cell(text: str, align: str = "left") -> rx.Component:
    """A standardized table header cell with compact padding."""
    align_class = f"text-{align}"
    return rx.el.th(
        text,
        class_name=f"px-2 py-0.5 {align_class} text-[9px] font-bold text-gray-500 uppercase tracking-wider sticky top-0 bg-gray-50 border-b border-gray-200 z-10",
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
            class_name="px-2 py-0 text-[9px] font-bold text-gray-900 border-b border-gray-100",
        ),
        rx.el.td(
            item["description"],
            class_name="px-2 py-0 text-[9px] font-medium text-gray-600 border-b border-gray-100 truncate max-w-[120px]",
        ),
        rx.el.td(
            item["asset_class"],
            class_name="px-2 py-0 text-[9px] text-gray-500 border-b border-gray-100",
        ),
        rx.el.td(
            item["qty"],
            class_name="px-2 py-0 text-[9px] font-mono text-gray-700 text-right border-b border-gray-100",
        ),
        rx.el.td(
            item["price"],
            class_name="px-2 py-0 text-[9px] font-mono text-gray-700 text-right border-b border-gray-100",
        ),
        rx.el.td(
            item["mkt_value"],
            class_name="px-2 py-0 text-[9px] font-bold font-mono text-gray-900 text-right border-b border-gray-100",
        ),
        rx.el.td(
            item["daily_pnl"],
            class_name=f"px-2 py-0 text-[9px] font-bold font-mono {pnl_color} text-right border-b border-gray-100",
        ),
        rx.el.td(
            rx.el.span(
                item["status"],
                class_name=f"px-1 py-0 rounded text-[7px] font-bold {status_color}",
            ),
            class_name="px-2 py-0 text-center border-b border-gray-100",
        ),
        rx.el.td(
            rx.el.span(
                reconciled_text,
                class_name=f"px-1 py-0 rounded text-[7px] font-bold text-white {reconciled_bg}",
            ),
            class_name="px-2 py-0 text-center border-b border-gray-100",
        ),
        class_name="group transition-colors duration-75 hover:bg-[#FFF2CC] cursor-default h-[20px]",
    )


def mock_data_table() -> rx.Component:
    """A robust placeholder table component with compact rows and vertical scroll."""
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    table_header_cell("Ticker"),
                    table_header_cell("Description"),
                    table_header_cell("Class"),
                    table_header_cell("Qty", "right"),
                    table_header_cell("Price", "right"),
                    table_header_cell("Mkt Val", "right"),
                    table_header_cell("PnL", "right"),
                    table_header_cell("Status", "center"),
                    table_header_cell("Rec", "center"),
                )
            ),
            rx.el.tbody(rx.foreach(PortfolioDashboardState.mock_table_data, table_row)),
            class_name="w-full table-auto border-collapse",
        ),
        type="always",
        scrollbars="vertical",
        class_name="flex-1 w-full h-full bg-white relative",
    )


def contextual_workspace() -> rx.Component:
    """The main workspace area (Region 3) with maximized table height."""
    active_page_name = rx.cond(
        PortfolioDashboardState.active_subtab != "",
        PortfolioDashboardState.active_subtab,
        PortfolioDashboardState.active_module,
    )
    return rx.el.div(
        rx.el.div(
            rx.foreach(PortfolioDashboardState.current_subtabs, sub_tab),
            class_name="flex items-center bg-white border-b border-gray-200 px-2 pt-0.5 overflow-x-auto shrink-0 h-[28px] no-scrollbar",
        ),
        rx.el.div(
            workspace_controls(),
            rx.el.div(
                mock_data_table(),
                class_name="flex-1 flex flex-col min-h-0 overflow-hidden bg-white",
            ),
            rx.el.div(
                rx.el.button(
                    f"Generate {active_page_name}",
                    on_click=PortfolioDashboardState.handle_generate(active_page_name),
                    class_name="bg-[#2563EB] text-white px-6 h-[32px] rounded shadow-sm hover:bg-blue-700 hover:shadow-md transition-all duration-200 text-[10px] font-bold uppercase tracking-widest flex items-center justify-center",
                ),
                class_name="flex justify-center shrink-0 bg-white border-t border-gray-200 h-[40px] items-center py-1 mt-auto",
            ),
            class_name="flex flex-col flex-1 min-h-0 h-full",
        ),
        class_name="flex flex-col flex-1 h-full min-h-0 bg-white border-r border-gray-200",
    )