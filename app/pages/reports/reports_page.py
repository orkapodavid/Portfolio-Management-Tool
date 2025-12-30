import reflex as rx
from app.components.shared.sidebar import sidebar
from app.components.shared.mobile_nav import mobile_nav
from app.states.reports.reports_state import ReportsState
from app.components.portfolio.report_charts import (
    performance_chart,
    allocation_report,
    summary_stats,
)


def reports_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Reports"),
        rx.el.main(
            mobile_nav(current_page="Reports"),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Performance Reports",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Detailed analysis of your portfolio performance and health.",
                            class_name="text-gray-500 text-sm mt-1",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(
                                ReportsState.ranges,
                                lambda r: rx.el.button(
                                    r,
                                    on_click=lambda: ReportsState.set_range(r),
                                    class_name=rx.cond(
                                        ReportsState.selected_range == r,
                                        "px-3 py-1.5 text-xs font-semibold bg-white text-indigo-600 rounded-lg shadow-sm border border-gray-200",
                                        "px-3 py-1.5 text-xs font-semibold text-gray-500 hover:text-gray-900 transition-colors",
                                    ),
                                ),
                            ),
                            class_name="p-1 bg-gray-100 rounded-xl flex items-center gap-1",
                        ),
                        rx.el.button(
                            rx.icon("download", size=16, class_name="mr-2"),
                            "Export PDF",
                            on_click=ReportsState.export_report,
                            class_name="flex items-center bg-indigo-600 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200",
                        ),
                        class_name="flex flex-col md:flex-row items-center gap-4",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                ),
                summary_stats(),
                rx.el.div(
                    performance_chart(),
                    allocation_report(),
                    class_name="flex flex-col gap-6",
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-y-auto p-4 md:p-8",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900",
    )