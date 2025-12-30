import reflex as rx
from app.components.shared.sidebar import sidebar
from app.components.shared.mobile_nav import mobile_nav
from app.states.user.settings_state import SettingsState


def setting_toggle(
    label: str, description: str, checked: bool, on_change: rx.EventHandler
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(label, class_name="text-sm font-bold text-gray-900"),
            rx.el.p(description, class_name="text-xs text-gray-500 mt-0.5"),
            class_name="flex flex-col pr-8",
        ),
        rx.switch(
            checked=checked,
            on_change=on_change,
            color_scheme="indigo",
            class_name="scale-90",
        ),
        class_name="flex items-center justify-between py-4 border-b border-gray-50 last:border-0",
    )


def section_header(title: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, size=20, class_name="text-indigo-600"),
        rx.el.h3(title, class_name="text-lg font-bold text-gray-900"),
        class_name="flex items-center gap-3 mb-6",
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Settings"),
        rx.el.main(
            mobile_nav(current_page="Settings"),
            rx.el.div(
                rx.el.h1(
                    "Settings", class_name="text-2xl font-bold text-gray-900 mb-1"
                ),
                rx.el.p(
                    "Manage your application preferences and account security.",
                    class_name="text-gray-500 text-sm mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            section_header("Account & Security", "shield-check"),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.label(
                                        "Email Address",
                                        class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-2",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            "alex.morgan@example.com",
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.button(
                                            "Change",
                                            class_name="text-xs font-bold text-indigo-600 hover:text-indigo-700",
                                        ),
                                        class_name="flex items-center justify-between p-3 bg-gray-50 rounded-xl",
                                    ),
                                    class_name="mb-6",
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Password",
                                        class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-2",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            "••••••••••••",
                                            class_name="text-sm font-medium text-gray-900",
                                        ),
                                        rx.el.button(
                                            "Update",
                                            class_name="text-xs font-bold text-indigo-600 hover:text-indigo-700",
                                        ),
                                        class_name="flex items-center justify-between p-3 bg-gray-50 rounded-xl",
                                    ),
                                    class_name="mb-6",
                                ),
                                rx.el.div(
                                    rx.el.h4(
                                        "Two-Factor Authentication",
                                        class_name="text-sm font-bold text-gray-900 mb-2",
                                    ),
                                    rx.el.button(
                                        rx.el.div(
                                            rx.icon(
                                                "smartphone",
                                                size=16,
                                                class_name="text-emerald-600",
                                            ),
                                            rx.el.span(
                                                "Enabled",
                                                class_name="text-xs font-bold text-emerald-700",
                                            ),
                                            class_name="flex items-center gap-2",
                                        ),
                                        class_name="w-full flex items-center justify-center p-3 bg-emerald-50 border border-emerald-100 rounded-xl hover:bg-emerald-100 transition-colors",
                                    ),
                                ),
                                class_name="p-6 bg-white rounded-3xl border border-gray-100 shadow-sm",
                            ),
                            class_name="mb-8",
                        ),
                        rx.el.div(
                            section_header("App Preferences", "slack"),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.label(
                                        "Currency",
                                        class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-2",
                                    ),
                                    rx.el.select(
                                        rx.el.option("USD - US Dollar", value="USD"),
                                        rx.el.option("EUR - Euro", value="EUR"),
                                        rx.el.option(
                                            "GBP - British Pound", value="GBP"
                                        ),
                                        default_value=SettingsState.currency,
                                        on_change=SettingsState.set_currency,
                                        class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none text-sm font-medium bg-white appearance-none",
                                    ),
                                    class_name="mb-6",
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Language",
                                        class_name="block text-xs font-bold text-gray-500 uppercase tracking-wide mb-2",
                                    ),
                                    rx.el.select(
                                        rx.el.option("English (US)", value="English"),
                                        rx.el.option("Spanish", value="Spanish"),
                                        rx.el.option("French", value="French"),
                                        default_value=SettingsState.language,
                                        on_change=SettingsState.set_language,
                                        class_name="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none text-sm font-medium bg-white appearance-none",
                                    ),
                                    class_name="mb-6",
                                ),
                                setting_toggle(
                                    "Dark Mode",
                                    "Use dark theme across the application",
                                    SettingsState.theme_mode == "dark",
                                    SettingsState.toggle_theme,
                                ),
                                class_name="p-6 bg-white rounded-3xl border border-gray-100 shadow-sm",
                            ),
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.div(
                            section_header("Notifications", "bell"),
                            rx.el.div(
                                setting_toggle(
                                    "Email Notifications",
                                    "Receive daily summaries and important alerts",
                                    SettingsState.email_notifications,
                                    lambda v: SettingsState.update_notification(
                                        "email", v
                                    ),
                                ),
                                setting_toggle(
                                    "Push Notifications",
                                    "Real-time alerts for price changes and trades",
                                    SettingsState.push_notifications,
                                    lambda v: SettingsState.update_notification(
                                        "push", v
                                    ),
                                ),
                                setting_toggle(
                                    "SMS Alerts",
                                    "Get urgent security alerts via text message",
                                    SettingsState.sms_notifications,
                                    lambda v: SettingsState.update_notification(
                                        "sms", v
                                    ),
                                ),
                                setting_toggle(
                                    "Marketing Emails",
                                    "Receive product updates and offers",
                                    SettingsState.marketing_emails,
                                    lambda v: SettingsState.update_notification(
                                        "marketing", v
                                    ),
                                ),
                                class_name="p-6 bg-white rounded-3xl border border-gray-100 shadow-sm",
                            ),
                            class_name="mb-8",
                        ),
                        rx.el.div(
                            section_header("Privacy & Data", "lock"),
                            rx.el.div(
                                setting_toggle(
                                    "Public Profile",
                                    "Allow others to find your profile",
                                    SettingsState.profile_public,
                                    lambda v: SettingsState.update_privacy("public", v),
                                ),
                                setting_toggle(
                                    "Show Holdings",
                                    "Make your investment portfolio visible",
                                    SettingsState.show_holdings,
                                    lambda v: SettingsState.update_privacy(
                                        "holdings", v
                                    ),
                                ),
                                setting_toggle(
                                    "Data Collection",
                                    "Allow usage data collection for improvements",
                                    SettingsState.allow_data_collection,
                                    lambda v: SettingsState.update_privacy("data", v),
                                ),
                                rx.el.div(
                                    rx.el.button(
                                        rx.icon("download", size=16, class_name="mr-2"),
                                        "Export My Data",
                                        on_click=SettingsState.export_data,
                                        class_name="w-full flex items-center justify-center px-4 py-2.5 mt-4 text-sm font-bold text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-xl transition-colors border border-gray-200",
                                    ),
                                    class_name="pt-2",
                                ),
                                class_name="p-6 bg-white rounded-3xl border border-gray-100 shadow-sm",
                            ),
                            class_name="mb-8",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3(
                                        "Delete Account",
                                        class_name="text-sm font-bold text-red-600",
                                    ),
                                    rx.el.p(
                                        "Permanently delete your account and all data.",
                                        class_name="text-xs text-gray-500 mt-1",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                rx.el.button(
                                    "Delete",
                                    on_click=SettingsState.delete_account,
                                    class_name="px-4 py-2 text-xs font-bold text-white bg-red-600 hover:bg-red-700 rounded-lg shadow-sm transition-colors",
                                ),
                                class_name="flex items-center justify-between p-6 bg-red-50/50 rounded-3xl border border-red-100",
                            )
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-y-auto p-4 md:p-8",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900",
    )