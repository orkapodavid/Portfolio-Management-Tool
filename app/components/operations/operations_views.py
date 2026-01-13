import reflex as rx
from app.states.operations.operations_state import OperationsState
from app.states.operations.types import (
    DailyProcedureItem,
    OperationProcessItem,
)


def header_cell(text: str, align: str = "left", column_key: str = "") -> rx.Component:
    align_class = rx.match(
        align, ("right", "text-right"), ("center", "text-center"), "text-left"
    )
    sort_icon = rx.cond(
        OperationsState.sort_column == column_key,
        rx.cond(
            OperationsState.sort_direction == "asc",
            rx.icon("arrow-up", size=10, class_name="ml-1 text-blue-600"),
            rx.icon("arrow-down", size=10, class_name="ml-1 text-blue-600"),
        ),
        rx.icon(
            "arrow-up-down",
            size=10,
            class_name="ml-1 text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity",
        ),
    )
    return rx.el.th(
        rx.el.div(
            text,
            rx.cond(column_key != "", sort_icon, rx.fragment()),
            class_name=f"flex items-center {rx.match(align, ('right', 'justify-end'), ('center', 'justify-center'), 'justify-start')}",
        ),
        on_click=lambda: rx.cond(
            column_key, OperationsState.toggle_sort(column_key), None
        ),
        class_name=f"px-3 py-3 {align_class} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap cursor-pointer hover:bg-gray-200 transition-colors group select-none",
    )


def text_cell(
    val: str, align: str = "left", bold: bool = False, clickable: bool = False
) -> rx.Component:
    base_class = f"px-3 py-2 text-[10px] text-gray-700 text-{align} border-b border-gray-200 align-middle whitespace-nowrap"
    if bold:
        base_class += " font-bold"
    if clickable:
        return rx.el.td(
            rx.el.a(val, class_name="text-blue-600 hover:underline cursor-pointer"),
            class_name=base_class,
        )
    return rx.el.td(val, class_name=base_class)


def status_badge(status: str) -> rx.Component:
    """Colored badge for status fields with auto-detection and accessibility icons."""
    colors = rx.match(
        status.lower(),
        ("success", "bg-green-100 text-green-700 border-green-300"),
        ("filled", "bg-green-100 text-green-700 border-green-300"),
        ("active", "bg-green-100 text-green-700 border-green-300"),
        ("failed", "bg-red-100 text-red-700 border-red-300"),
        ("error", "bg-red-100 text-red-700 border-red-300"),
        ("inactive", "bg-gray-100 text-gray-700 border-gray-300"),
        ("running", "bg-amber-100 text-amber-700 border-amber-300"),
        ("warning", "bg-amber-100 text-amber-700 border-amber-300"),
        "bg-blue-100 text-blue-700 border-blue-300",
    )
    icon_name = rx.match(
        status.lower(),
        ("success", "check-circle"),
        ("filled", "check-circle"),
        ("active", "play-circle"),
        ("failed", "x-circle"),
        ("error", "alert-circle"),
        ("warning", "alert-triangle"),
        ("running", "loader"),
        "info",
    )
    return rx.el.span(
        rx.icon(icon_name, size=10, class_name="mr-1 shrink-0"),
        status,
        class_name=f"inline-flex items-center px-2 py-0.5 rounded-full text-[9px] font-bold border {colors} uppercase tracking-tight shadow-sm",
    )


def daily_proc_row(item: DailyProcedureItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["check_date"]),
        text_cell(item["host_run_date"], clickable=False),
        text_cell(item["scheduled_time"]),
        text_cell(item["procedure_name"]),
        rx.el.td(
            status_badge(item["status"]),
            class_name="px-3 py-2 border-b border-gray-200 align-middle whitespace-nowrap",
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
                    header_cell("Procedure Name", column_key="procedure_name"),
                    header_cell("Status", column_key="status"),
                    header_cell("Error Message"),
                    header_cell("Frequency"),
                    header_cell("Scheduled Day"),
                    header_cell("Created By"),
                    header_cell("Created Time"),
                )
            ),
            rx.el.tbody(
                rx.foreach(OperationsState.filtered_daily_procedures, daily_proc_row)
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
                    header_cell("Process", column_key="process"),
                    header_cell("Status", column_key="status"),
                    header_cell("Last Run Time"),
                )
            ),
            rx.el.tbody(
                rx.foreach(OperationsState.filtered_operation_processes, ops_proc_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
