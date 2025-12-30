import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState
from app.components.pnl import (
    pnl_change_table,
    pnl_full_table,
    pnl_summary_table,
    pnl_currency_table,
)
from app.components.positions import (
    positions_table,
    stock_position_table,
    warrant_position_table,
    bond_position_table,
    trade_summary_table,
)
from app.components.compliance import (
    restricted_list_table,
    undertakings_table,
    beneficial_ownership_table,
    monthly_exercise_limit_table,
)
from app.components.portfolio_tools import (
    pay_to_hold_table,
    short_ecl_table,
    stock_borrow_table,
    po_settlement_table,
    deal_indication_table,
    reset_dates_table,
    coming_resets_table,
    cb_installments_table,
    excess_amount_table,
)
from app.components.reconciliation import (
    pps_recon_table,
    settlement_recon_table,
    failed_trades_table,
    pnl_recon_table,
    risk_input_recon_table,
)
from app.components.operations import (
    daily_procedure_check_table,
    operation_process_table,
)
from app.components.market_data import (
    market_data_table,
    fx_data_table,
    historical_data_table,
    trading_calendar_table,
    market_hours_table,
    event_calendar_table,
    event_stream_view,
    reverse_inquiry_table,
)
from app.components.instruments import (
    ticker_data_table,
    stock_screener_view,
    special_term_table,
    instrument_data_table,
    instrument_term_table,
)
from app.components.risk import (
    delta_change_table,
    risk_measures_table,
    risk_inputs_table,
    pricer_warrant_view,
    pricer_bond_view,
)
from app.components.emsa import emsa_order_table, emsa_route_table


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
    price_fmt = rx.cond(item["is_positive"], f"${item['price']}", f"$({item['price']})")
    mkt_val_fmt = rx.cond(
        item["is_positive"], f"${item['mkt_value']}", f"$({item['mkt_value']})"
    )
    pnl_fmt = rx.cond(
        item["is_positive"], f"${item['daily_pnl']}", f"$({item['daily_pnl']})"
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
            price_fmt,
            class_name="px-3 py-2 text-[10px] font-mono font-bold text-gray-700 text-right border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            mkt_val_fmt,
            class_name="px-3 py-2 text-[10px] font-black font-mono text-gray-900 text-right border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            pnl_fmt,
            class_name=f"px-3 py-2 text-[10px] font-black font-mono {pnl_color} text-right border-b border-gray-200 align-middle",
        ),
        rx.el.td(
            rx.el.div(
                rx.match(
                    item["status"],
                    (
                        "Active",
                        rx.el.span(
                            "Active",
                            class_name="px-2 py-0.5 rounded-full text-[8px] font-black uppercase tracking-wider bg-emerald-100 text-[#059669] border border-emerald-200 shadow-sm",
                        ),
                    ),
                    (
                        "Hedged",
                        rx.el.span(
                            "Hedged",
                            class_name="px-2 py-0.5 rounded-full text-[8px] font-black uppercase tracking-wider bg-blue-100 text-[#2563EB] border border-blue-200 shadow-sm",
                        ),
                    ),
                    (
                        "Review",
                        rx.el.span(
                            "Review",
                            class_name="px-2 py-0.5 rounded-full text-[8px] font-black uppercase tracking-wider bg-orange-100 text-[#C2410C] border border-orange-200 shadow-sm",
                        ),
                    ),
                    rx.el.span(
                        item["status"],
                        class_name="px-2 py-0.5 rounded-full text-[8px] font-black uppercase tracking-wider bg-gray-100 text-gray-600 border border-gray-200",
                    ),
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


def generate_menu_item(label: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: PortfolioDashboardState.handle_generate(label),
        class_name="block w-full text-left px-4 py-2 text-[10px] font-bold text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors",
    )


def workspace_controls() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.icon("zap", size=12),
                        rx.el.span("Generate", class_name="ml-1.5"),
                        rx.icon("chevron-down", size=10, class_name="ml-1 opacity-70"),
                        class_name="flex items-center",
                    ),
                    on_click=PortfolioDashboardState.toggle_generate_menu,
                    class_name="px-3 h-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-[10px] font-black uppercase tracking-widest rounded hover:shadow-md transition-all flex items-center shadow-sm",
                ),
                rx.cond(
                    PortfolioDashboardState.is_generate_menu_open,
                    rx.el.div(
                        rx.el.div(
                            class_name="fixed inset-0 z-40",
                            on_click=PortfolioDashboardState.toggle_generate_menu,
                        ),
                        rx.el.div(
                            generate_menu_item("Generate PnL Change"),
                            generate_menu_item("Generate PnL Summary"),
                            generate_menu_item("Generate PnL Currency"),
                            class_name="absolute top-full left-0 mt-1 w-48 bg-white rounded-md shadow-lg border border-gray-100 py-1 z-50 animate-in fade-in slide-in-from-top-1 duration-100",
                        ),
                    ),
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.el.div(
                    rx.icon("download", size=12),
                    rx.el.span("Export", class_name="ml-1.5"),
                    class_name="flex items-center",
                ),
                class_name="px-3 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold uppercase tracking-widest rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm flex items-center",
            ),
            rx.el.button(
                rx.icon(
                    "refresh-cw",
                    size=12,
                    class_name=rx.cond(
                        PortfolioDashboardState.is_loading, "animate-spin", ""
                    ),
                ),
                on_click=PortfolioDashboardState.refresh_prices,
                class_name="h-6 w-6 flex items-center justify-center bg-white border border-gray-200 text-gray-600 rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm",
            ),
            rx.el.div(
                rx.icon("search", size=12, class_name="text-gray-400 mr-1.5"),
                rx.el.input(
                    placeholder="Search data...",
                    on_change=PortfolioDashboardState.set_current_search,
                    class_name="bg-transparent text-[10px] font-bold outline-none w-full text-gray-700",
                ),
                class_name="flex items-center bg-white border border-gray-200 rounded px-2 h-6 flex-1 max-w-[200px] shadow-sm ml-2",
            ),
            rx.el.div(
                rx.el.input(
                    type="date",
                    on_change=PortfolioDashboardState.set_current_date,
                    class_name="bg-white border border-gray-200 rounded px-2 h-6 text-[10px] font-bold text-gray-600 outline-none shadow-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center gap-2 flex-1",
        ),
        class_name="flex items-center justify-between px-3 py-1.5 bg-[#F9F9F9] border-b border-gray-200 shrink-0 h-[40px]",
    )


def contextual_workspace() -> rx.Component:
    """The main workspace area (Region 3) with maximized table height."""
    content = rx.match(
        PortfolioDashboardState.active_module,
        (
            "PnL",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("PnL Change", pnl_change_table()),
                ("PnL Full", pnl_full_table()),
                ("PnL Summary", pnl_summary_table()),
                ("PnL Currency", pnl_currency_table()),
                mock_data_table(),
            ),
        ),
        (
            "Positions",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Positions", positions_table()),
                ("Stock Position", stock_position_table()),
                ("Warrant Position", warrant_position_table()),
                ("Bond Positions", bond_position_table()),
                ("Trade Summary (War/Bond)", trade_summary_table()),
                mock_data_table(),
            ),
        ),
        (
            "Compliance",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Restricted List", restricted_list_table()),
                ("Undertakings", undertakings_table()),
                ("Beneficial Ownership", beneficial_ownership_table()),
                ("Monthly Exercise Limit", monthly_exercise_limit_table()),
                mock_data_table(),
            ),
        ),
        (
            "Portfolio Tools",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Pay-To-Hold", pay_to_hold_table()),
                ("Short ECL", short_ecl_table()),
                ("Stock Borrow", stock_borrow_table()),
                ("PO Settlement", po_settlement_table()),
                ("Deal Indication", deal_indication_table()),
                ("Reset Dates", reset_dates_table()),
                ("Coming Resets", coming_resets_table()),
                ("CB Installments", cb_installments_table()),
                ("Excess Amount", excess_amount_table()),
                mock_data_table(),
            ),
        ),
        (
            "Recon",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("PPS Recon", pps_recon_table()),
                ("Settlement Recon", settlement_recon_table()),
                ("Failed Trades", failed_trades_table()),
                ("PnL Recon", pnl_recon_table()),
                ("Risk Input Recon", risk_input_recon_table()),
                mock_data_table(),
            ),
        ),
        (
            "Operations",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Daily Procedure Check", daily_procedure_check_table()),
                ("Operation Process", operation_process_table()),
                mock_data_table(),
            ),
        ),
        (
            "Market Data",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Market Data", market_data_table()),
                ("FX Data", fx_data_table()),
                ("Historical Data", historical_data_table()),
                ("Trading Calendar", trading_calendar_table()),
                ("Market Hours", market_hours_table()),
                mock_data_table(),
            ),
        ),
        (
            "Events",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Event Calendar", event_calendar_table()),
                ("Event Stream", event_stream_view()),
                ("Reverse Inquiry", reverse_inquiry_table()),
                mock_data_table(),
            ),
        ),
        (
            "Instruments",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Ticker Data", ticker_data_table()),
                ("Stock Screener", stock_screener_view()),
                ("Special Term", special_term_table()),
                ("Instrument Data", instrument_data_table()),
                ("Instrument Term", instrument_term_table()),
                mock_data_table(),
            ),
        ),
        (
            "Risk",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("Delta Change", delta_change_table()),
                ("Risk Measures", risk_measures_table()),
                ("Risk Inputs", risk_inputs_table()),
                ("Pricer Warrant", pricer_warrant_view()),
                ("Pricer Bond", pricer_bond_view()),
                mock_data_table(),
            ),
        ),
        (
            "Orders",
            rx.match(
                PortfolioDashboardState.active_subtab,
                ("EMSX Order", emsa_order_table()),
                ("EMSX Route", emsa_route_table()),
                mock_data_table(),
            ),
        ),
        mock_data_table(),
    )
    return rx.el.div(
        rx.el.div(
            rx.foreach(PortfolioDashboardState.current_subtabs, sub_tab),
            class_name="flex flex-row items-center bg-white border-b border-gray-200 px-2 pt-0.5 overflow-hidden shrink-0 h-[28px] w-full max-w-full flex-nowrap",
        ),
        rx.el.div(
            workspace_controls(),
            rx.el.div(
                content,
                class_name="flex-1 flex flex-col min-h-0 overflow-hidden bg-white",
            ),
            class_name="flex flex-col flex-1 min-h-0 h-full",
        ),
        class_name="flex flex-col flex-1 h-full min-h-0 bg-white border-r border-gray-200",
    )