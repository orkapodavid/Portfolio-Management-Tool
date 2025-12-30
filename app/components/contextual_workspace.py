import reflex as rx
from app.states.portfolio_dashboard_state import PortfolioDashboardState


def table_header_cell(text: str, align: str = "left") -> rx.Component:
    """A standardized table header cell with enhanced separation and dark background."""
    align_class = rx.match(
        align, ("right", "text-right"), ("center", "text-center"), "text-left"
    )
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 {align_class} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 align-middle whitespace-nowrap h-[44px]",
    )


def table_row(item: dict) -> rx.Component:
    """An optimized, high-density data row with row selection and financial formatting."""
    from app.constants import POSITIVE_GREEN, NEGATIVE_RED, ROW_HIGHLIGHT

    table_row_height = "40px"
    is_selected = PortfolioDashboardState.selected_row_id == item["id"]
    pnl_color = rx.cond(
        item["is_positive"], f"text-[{POSITIVE_GREEN}]", f"text-[{NEGATIVE_RED}]"
    )
    return rx.el.tr(
        rx.el.td(
            item["ticker"],
            class_name="px-3 py-2 text-[10px] font-black text-gray-900 border-b border-gray-200 text-left align-middle",
        ),
        rx.el.td(
            item["description"],
            class_name="px-3 py-2 text-[10px] font-bold text-gray-600 border-b border-gray-200 truncate max-w-[140px] text-left align-middle",
        ),
        rx.el.td(
            item["asset_class"],
            class_name="px-3 py-2 text-[10px] font-medium text-gray-500 border-b border-gray-200 text-left align-middle",
        ),
        rx.el.td(
            item["qty"],
            class_name="px-3 py-2 text-[10px] font-mono font-bold text-gray-700 text-right border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            f"${item['price']}",
            class_name="px-3 py-2 text-[10px] font-mono font-bold text-gray-700 text-right border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            f"${item['mkt_value']}",
            class_name="px-3 py-2 text-[10px] font-black font-mono text-gray-900 text-right border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            f"${item['daily_pnl']}",
            class_name=f"px-3 py-2 text-[10px] font-black font-mono {pnl_color} text-right border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    item["status"],
                    class_name="px-1.5 py-0.5 rounded-[2px] text-[8px] font-black uppercase tracking-tighter bg-gray-100 text-gray-600",
                ),
                class_name="flex items-center justify-center",
            ),
            class_name="px-3 py-2 text-center border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            rx.cond(
                item["is_reconciled"],
                rx.el.div(
                    rx.icon("check", size=12, class_name=f"text-[{POSITIVE_GREEN}]"),
                    rx.el.span(
                        "REC", class_name="text-[8px] font-bold text-emerald-600 ml-1"
                    ),
                    class_name="flex items-center justify-center",
                ),
                rx.el.div(
                    rx.icon("x", size=12, class_name=f"text-[{NEGATIVE_RED}]"),
                    rx.el.span(
                        "VAR", class_name="text-[8px] font-bold text-red-600 ml-1"
                    ),
                    class_name="flex items-center justify-center",
                ),
            ),
            class_name="px-3 py-2 text-center border-b border-gray-200 align-middle",
        ),
        on_click=lambda: PortfolioDashboardState.set_selected_row(item["id"]),
        class_name=rx.cond(
            is_selected,
            f"bg-[{ROW_HIGHLIGHT}]",
            "odd:bg-white even:bg-gray-50 hover:bg-gray-100",
        )
        + f" cursor-pointer h-[{table_row_height}] min-h-[40px] transition-colors duration-75",
    )


def pagination_controls() -> rx.Component:
    """Pagination controls for the data table."""
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "Rows:",
                class_name="text-[10px] font-bold text-gray-500 uppercase tracking-tight mr-2",
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        PortfolioDashboardState.page_size_options,
                        lambda x: rx.el.option(x.to_string(), value=x.to_string()),
                    ),
                    value=PortfolioDashboardState.page_size.to_string(),
                    on_change=PortfolioDashboardState.set_page_size,
                    class_name="text-[10px] font-bold border-gray-300 rounded px-1.5 py-0 h-6 bg-white appearance-none pr-6 outline-none focus:border-blue-500 shadow-sm transition-all",
                ),
                rx.icon(
                    "chevron-down",
                    size=10,
                    class_name="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none",
                ),
                class_name="relative",
            ),
            class_name="flex items-center",
        ),
        rx.el.span(
            f"Page {PortfolioDashboardState.current_page} of {PortfolioDashboardState.total_pages} ({PortfolioDashboardState.total_items} items)",
            class_name="text-[10px] text-gray-500 font-medium",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", size=14),
                on_click=PortfolioDashboardState.prev_page,
                disabled=PortfolioDashboardState.current_page == 1,
                class_name="p-1 rounded hover:bg-gray-200 disabled:opacity-30 disabled:hover:bg-transparent transition-colors",
            ),
            rx.el.button(
                rx.icon("chevron-right", size=14),
                on_click=PortfolioDashboardState.next_page,
                disabled=PortfolioDashboardState.current_page
                == PortfolioDashboardState.total_pages,
                class_name="p-1 rounded hover:bg-gray-200 disabled:opacity-30 disabled:hover:bg-transparent transition-colors",
            ),
            class_name="flex gap-1",
        ),
        class_name="flex items-center justify-between px-3 py-1 border-t border-gray-200 bg-gray-50 shrink-0 h-[32px]",
    )


def mock_data_table() -> rx.Component:
    """An optimized data table with sticky headers, responsive scrolling and pagination."""
    return rx.el.div(
        rx.cond(
            PortfolioDashboardState.is_loading,
            rx.el.div(
                rx.el.div(
                    class_name="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"
                ),
                class_name="absolute inset-0 flex items-center justify-center bg-white/50 z-20",
            ),
        ),
        rx.scroll_area(
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
                        class_name="bg-[#E5E7EB] sticky top-0 z-30 shadow-[0_2px_4px_rgba(0,0,0,0.1)] h-[44px] min-h-[44px]",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(PortfolioDashboardState.paginated_table_data, table_row)
                ),
                class_name="w-full min-w-[800px] table-auto border-separate border-spacing-0",
            ),
            type="hover",
            scrollbars="both",
            class_name="flex-1 w-full bg-white contain-strict",
        ),
        pagination_controls(),
        class_name="flex-1 w-full h-full bg-white relative overflow-hidden flex flex-col",
    )


def sub_tab(name: str) -> rx.Component:
    is_active = PortfolioDashboardState.active_subtab == name
    return rx.el.button(
        name,
        on_click=lambda: PortfolioDashboardState.set_subtab(name),
        class_name=rx.cond(
            is_active,
            "px-3 h-full text-[9px] font-black text-blue-600 border-b-2 border-blue-600 uppercase tracking-tighter whitespace-nowrap",
            "px-3 h-full text-[9px] font-bold text-gray-400 border-b-2 border-transparent hover:text-gray-600 uppercase tracking-tighter whitespace-nowrap",
        ),
    )


def workspace_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("search", size=12, class_name="text-gray-400 mr-1.5"),
                rx.el.input(
                    placeholder="Search tickers...",
                    on_change=PortfolioDashboardState.set_current_search,
                    class_name="bg-transparent text-[10px] font-bold outline-none w-full text-gray-700",
                ),
                class_name="flex items-center bg-gray-100 border border-gray-200 rounded px-2 h-6 flex-1 max-w-[200px]",
            ),
            rx.el.div(
                rx.el.input(
                    type="date",
                    on_change=PortfolioDashboardState.set_current_date,
                    class_name="bg-gray-100 border border-gray-200 rounded px-2 h-6 text-[10px] font-bold text-gray-600 outline-none",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center gap-3 flex-1",
        ),
        rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.icon("zap", size=10),
                    rx.el.span("Generate", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                on_click=lambda: PortfolioDashboardState.handle_generate(
                    PortfolioDashboardState.active_subtab
                ),
                class_name="px-3 h-6 bg-blue-600 text-white text-[10px] font-black uppercase tracking-widest rounded hover:bg-blue-700 transition-colors",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-center justify-between px-3 py-1 bg-[#F9F9F9] border-b border-gray-200 shrink-0 h-[36px]",
    )


def contextual_workspace() -> rx.Component:
    """The main workspace area (Region 3) with maximized table height."""
    return rx.el.div(
        rx.el.div(
            rx.foreach(PortfolioDashboardState.current_subtabs, sub_tab),
            class_name="flex flex-row items-center bg-white border-b border-gray-200 px-2 pt-0.5 overflow-hidden shrink-0 h-[28px] w-full max-w-full flex-nowrap",
        ),
        rx.el.div(
            workspace_controls(),
            rx.el.div(
                mock_data_table(),
                class_name="flex-1 flex flex-col min-h-0 overflow-hidden bg-white",
            ),
            class_name="flex flex-col flex-1 min-h-0 h-full",
        ),
        class_name="flex flex-col flex-1 h-full min-h-0 bg-white border-r border-gray-200",
    )