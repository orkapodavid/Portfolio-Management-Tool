import reflex as rx
from app.states.portfolio_dashboard_state import (
    PortfolioDashboardState,
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
    TradeSummaryItem,
)
from app.constants import POSITIVE_GREEN, NEGATIVE_RED


def header_cell(text: str, align: str = "right") -> rx.Component:
    align_class = rx.match(
        align, ("left", "text-left"), ("center", "text-center"), "text-right"
    )
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 {align_class} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-[0_2px_4px_rgba(0,0,0,0.1)] h-[44px]",
    )


def value_cell(
    val: str, is_positive: bool = True, align: str = "right"
) -> rx.Component:
    color = rx.cond(is_positive, f"text-[{POSITIVE_GREEN}]", f"text-[{NEGATIVE_RED}]")
    return rx.el.td(
        val,
        class_name=f"px-3 py-2 text-[10px] font-mono font-bold {color} text-{align} border-b border-gray-200 align-middle",
    )


def text_cell(val: str, align: str = "left", bold: bool = False) -> rx.Component:
    weight = rx.cond(bold, "font-black", "font-medium")
    return rx.el.td(
        val,
        class_name=f"px-3 py-2 text-[10px] {weight} text-gray-700 text-{align} border-b border-gray-200 align-middle",
    )


def positions_row(p: PositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["ticker"], bold=True),
        text_cell(p["qty"], align="right"),
        text_cell(p["mkt_value"], align="right"),
        text_cell(p["cost_basis"], align="right"),
        value_cell(p["unrealized_pnl"], is_positive=p["is_positive"]),
        value_cell(p["realized_pnl"], is_positive=True),
        text_cell(p["weight_pct"], align="right"),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def positions_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker", "left"),
                    header_cell("Qty"),
                    header_cell("Mkt Value"),
                    header_cell("Cost Basis"),
                    header_cell("Unrealized PnL"),
                    header_cell("Realized PnL"),
                    header_cell("Weight %"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_positions, positions_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def stock_position_row(p: StockPositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["ticker"], bold=True),
        text_cell(p["shares"], align="right"),
        text_cell(p["avg_cost"], align="right"),
        text_cell(p["current_price"], align="right"),
        text_cell(p["mkt_value"], align="right"),
        value_cell(p["daily_pnl"], is_positive=p["is_positive"]),
        text_cell(p["sector"], align="left"),
        text_cell(p["beta"], align="right"),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def stock_position_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker", "left"),
                    header_cell("Shares"),
                    header_cell("Avg Cost"),
                    header_cell("Price"),
                    header_cell("Mkt Value"),
                    header_cell("Daily PnL"),
                    header_cell("Sector", "left"),
                    header_cell("Beta"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_stock_positions, stock_position_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def warrant_position_row(p: WarrantPositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["underlying"], bold=True),
        text_cell(p["ticker"]),
        text_cell(p["strike"], align="right"),
        text_cell(p["expiry"], align="center"),
        text_cell(p["qty"], align="right"),
        text_cell(p["delta"], align="right"),
        text_cell(p["gamma"], align="right"),
        text_cell(p["theta"], align="right"),
        text_cell(p["intrinsic_value"], align="right"),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def warrant_position_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Underlying", "left"),
                    header_cell("Ticker", "left"),
                    header_cell("Strike"),
                    header_cell("Expiry", "center"),
                    header_cell("Qty"),
                    header_cell("Delta"),
                    header_cell("Gamma"),
                    header_cell("Theta"),
                    header_cell("Intrinsic"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_warrant_positions,
                    warrant_position_row,
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def bond_position_row(p: BondPositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["issuer"], bold=True),
        text_cell(p["coupon"], align="center"),
        text_cell(p["maturity"], align="center"),
        text_cell(p["face_value"], align="right"),
        text_cell(p["mkt_value"], align="right"),
        text_cell(p["yield_to_maturity"], align="right"),
        text_cell(p["duration"], align="right"),
        text_cell(p["rating"], align="center"),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def bond_position_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Issuer", "left"),
                    header_cell("Coupon", "center"),
                    header_cell("Maturity", "center"),
                    header_cell("Face Value"),
                    header_cell("Mkt Value"),
                    header_cell("YTM"),
                    header_cell("Duration"),
                    header_cell("Rating", "center"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_bond_positions, bond_position_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def trade_summary_row(p: TradeSummaryItem) -> rx.Component:
    status_bg = rx.match(
        p["status"],
        ("Settled", "bg-emerald-100 text-emerald-700"),
        "bg-amber-100 text-amber-700",
    )
    return rx.el.tr(
        text_cell(p["trade_date"]),
        text_cell(p["security_type"]),
        text_cell(p["ticker"], bold=True),
        text_cell(p["side"], align="center"),
        text_cell(p["qty"], align="right"),
        text_cell(p["price"], align="right"),
        text_cell(p["notional"], align="right"),
        rx.el.td(
            rx.el.span(
                p["status"],
                class_name=f"px-2 py-0.5 rounded-full text-[8px] font-black uppercase {status_bg} border border-black/5",
            ),
            class_name="px-3 py-2 text-center border-b border-gray-200 align-middle",
        ),
        text_cell(p["settlement_date"], align="center"),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def trade_summary_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", "left"),
                    header_cell("Type", "left"),
                    header_cell("Ticker", "left"),
                    header_cell("Side", "center"),
                    header_cell("Qty"),
                    header_cell("Price"),
                    header_cell("Notional"),
                    header_cell("Status", "center"),
                    header_cell("Settle Date", "center"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_trade_summaries, trade_summary_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )