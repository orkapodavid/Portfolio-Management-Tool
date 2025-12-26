import reflex as rx
from app.states.watchlist_state import WatchlistState, StockAlert


def alert_item(alert: StockAlert) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(alert["symbol"], class_name="font-bold text-gray-900"),
                rx.el.span(
                    f"{alert['condition']} ${alert['target_price']}",
                    class_name="text-sm text-gray-500 ml-2",
                ),
                class_name="flex items-center",
            ),
            rx.el.span(alert["created_at"], class_name="text-xs text-gray-400 mt-1"),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(
                    "bell",
                    size=16,
                    class_name=rx.cond(
                        alert["active"], "text-indigo-600", "text-gray-300"
                    ),
                ),
                on_click=lambda: WatchlistState.toggle_alert_active(alert["id"]),
                class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                title="Toggle Active",
            ),
            rx.el.button(
                rx.icon(
                    "trash-2", size=16, class_name="text-gray-400 hover:text-red-500"
                ),
                on_click=lambda: WatchlistState.delete_alert(alert["id"]),
                class_name="p-2 hover:bg-red-50 rounded-full transition-colors",
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-center justify-between p-4 border-b border-gray-100 last:border-0 hover:bg-gray-50 transition-colors",
    )


def create_alert_modal() -> rx.Component:
    return rx.cond(
        WatchlistState.is_alert_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/50 transition-opacity z-50",
                on_click=WatchlistState.close_alert_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        f"Set Alert for {WatchlistState.alert_symbol}",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("x", size=20, class_name="text-gray-400"),
                        on_click=WatchlistState.close_alert_modal,
                        class_name="p-1 hover:bg-gray-100 rounded-full transition-colors",
                    ),
                    class_name="flex items-center justify-between mb-6",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Condition",
                            class_name="block text-sm font-medium text-gray-700 mb-2",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Price Above",
                                type="button",
                                on_click=lambda: WatchlistState.set_alert_condition(
                                    "Above"
                                ),
                                class_name=rx.cond(
                                    WatchlistState.alert_condition == "Above",
                                    "flex-1 py-2 text-sm font-semibold bg-indigo-100 text-indigo-700 rounded-lg transition-colors border border-indigo-200",
                                    "flex-1 py-2 text-sm font-semibold text-gray-500 hover:bg-gray-50 rounded-lg transition-colors border border-gray-200",
                                ),
                            ),
                            rx.el.button(
                                "Price Below",
                                type="button",
                                on_click=lambda: WatchlistState.set_alert_condition(
                                    "Below"
                                ),
                                class_name=rx.cond(
                                    WatchlistState.alert_condition == "Below",
                                    "flex-1 py-2 text-sm font-semibold bg-indigo-100 text-indigo-700 rounded-lg transition-colors border border-indigo-200",
                                    "flex-1 py-2 text-sm font-semibold text-gray-500 hover:bg-gray-50 rounded-lg transition-colors border border-gray-200",
                                ),
                            ),
                            class_name="flex gap-3 mb-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Target Price ($)",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="price",
                            type="number",
                            step="0.01",
                            default_value=WatchlistState.alert_target_price.to_string(),
                            class_name="w-full px-4 py-2 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all",
                            required=True,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=WatchlistState.close_alert_modal,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-xl transition-colors",
                        ),
                        rx.el.button(
                            "Create Alert",
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-lg shadow-indigo-200 transition-all",
                        ),
                        class_name="flex items-center justify-end gap-3",
                    ),
                    on_submit=WatchlistState.save_alert,
                    reset_on_submit=True,
                ),
                class_name="bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 relative z-50 animate-in fade-in zoom-in duration-200",
            ),
            class_name="fixed inset-0 z-[60] flex items-center justify-center p-4",
        ),
    )


def alerts_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Active Alerts",
                class_name="text-xl font-bold text-gray-900 tracking-tight",
            ),
            rx.el.div(
                rx.el.span(
                    WatchlistState.alerts.length(),
                    class_name="bg-indigo-100 text-indigo-700 text-xs font-bold px-2.5 py-1 rounded-full",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between mb-6 px-6 pt-6",
        ),
        rx.el.div(
            rx.cond(
                WatchlistState.alerts.length() > 0,
                rx.foreach(WatchlistState.alerts, alert_item),
                rx.el.div(
                    rx.el.div(
                        rx.icon("bell-off", class_name="text-gray-300 mb-2", size=32),
                        rx.el.p(
                            "No active alerts",
                            class_name="text-sm font-medium text-gray-500",
                        ),
                        class_name="flex flex-col items-center justify-center py-12",
                    )
                ),
            ),
            class_name="max-h-[300px] overflow-y-auto",
        ),
        create_alert_modal(),
        class_name="bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden h-fit",
    )