import reflex as rx
from app.states.portfolio_dashboard_state import (
    PortfolioDashboardState,
    DailyProcedureItem,
    OperationProcessItem,
)


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


def daily_proc_row(item: DailyProcedureItem) -> rx.Component:
    status_color = rx.match(
        item["status"],
        ("Success", "text-green-600 font-bold"),
        ("Failed", "text-red-600 font-bold"),
        ("Running", "text-amber-600 font-bold"),
        "text-gray-700",
    )
    return rx.el.tr(
        text_cell(item["check_date"]),
        text_cell(item["host_run_date"]),
        text_cell(item["scheduled_time"]),
        text_cell(item["procedure_name"]),
        rx.el.td(
            item["status"],
            class_name=f"px-3 py-2 text-[10px] {status_color} border-b border-gray-200 align-middle whitespace-nowrap",
        ),
        text_cell(item["error_message"]),
        text_cell(item["frequency"]),
        text_cell(item["scheduled_day"]),
        text_cell(item["created_by"]),
        text_cell(item["created_time"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def daily_procedure_check_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Check Date"),
                    header_cell("Host Run Date"),
                    header_cell("Scheduled Time"),
                    header_cell("Procedure Name"),
                    header_cell("Status"),
                    header_cell("Error Message"),
                    header_cell("Frequency"),
                    header_cell("Scheduled Day"),
                    header_cell("Created By"),
                    header_cell("Created Time"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_daily_procedures, daily_proc_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def ops_proc_row(item: OperationProcessItem) -> rx.Component:
    status_color = rx.match(
        item["status"],
        ("Active", "text-green-600 font-bold"),
        ("Inactive", "text-gray-400 font-medium"),
        ("Running", "text-amber-600 font-bold"),
        ("Error", "text-red-600 font-bold"),
        "text-gray-700",
    )
    return rx.el.tr(
        text_cell(item["process"]),
        rx.el.td(
            item["status"],
            class_name=f"px-3 py-2 text-[10px] {status_color} border-b border-gray-200 align-middle whitespace-nowrap",
        ),
        text_cell(item["last_run_time"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def operation_process_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Process"),
                    header_cell("Status"),
                    header_cell("Last Run Time"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_operation_processes, ops_proc_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )