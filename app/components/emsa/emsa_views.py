import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState
from app.states.dashboard.portfolio_dashboard_types import EMSAOrderItem


def header_cell(text: str, align: str = "left") -> rx.Component:
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 text-{align} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap",
    )


def text_cell(val: str) -> rx.Component:
    return rx.el.td(
        val,
        class_name="px-3 py-2 text-[10px] font-medium text-gray-700 border-b border-gray-200 align-middle whitespace-nowrap",
    )


def emsa_row(item: EMSAOrderItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["sequence"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["broker"]),
        text_cell(item["pos_loc"]),
        text_cell(item["side"]),
        text_cell(item["status"]),
        text_cell(item["emsa_amount"]),
        text_cell(item["emsa_routed"]),
        text_cell(item["emsa_working"]),
        text_cell(item["emsa_filled"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def emsa_order_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Sequence"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Broker"),
                    header_cell("Pos Loc"),
                    header_cell("Side"),
                    header_cell("Status"),
                    header_cell("EMSA Amount"),
                    header_cell("EMSA Routed"),
                    header_cell("EMSA Working"),
                    header_cell("EMSA Filled"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_emsa_orders, emsa_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def emsa_route_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Sequence"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Broker"),
                    header_cell("Pos Loc"),
                    header_cell("Side"),
                    header_cell("Status"),
                    header_cell("EMSA Amount"),
                    header_cell("EMSA Routed"),
                    header_cell("EMSA Working"),
                    header_cell("EMSA Filled"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_emsa_routes, emsa_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )