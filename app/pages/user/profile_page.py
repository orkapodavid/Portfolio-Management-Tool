import reflex as rx
from app.components.shared.sidebar import sidebar
from app.components.shared.mobile_nav import mobile_nav
from app.states.user.profile_state import ProfileState, LinkedAccount


def info_field(label: str, value: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=18, class_name="text-gray-400"),
            rx.el.span(
                label,
                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
            ),
            class_name="flex items-center gap-2 mb-2",
        ),
        rx.el.p(value, class_name="text-gray-900 font-medium"),
        class_name="p-4 bg-gray-50 rounded-xl border border-gray-100",
    )


def edit_field(
    label: str, name: str, default_value: str, type: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-bold text-gray-700 mb-2"),
        rx.el.input(
            name=name,
            default_value=default_value,
            type=type,
            class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all",
        ),
        class_name="mb-6",
    )


def account_card(account: LinkedAccount) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(account["logo"], size=24, class_name="text-gray-700"),
                class_name="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center mr-4",
            ),
            rx.el.div(
                rx.el.h4(account["institution"], class_name="font-bold text-gray-900"),
                rx.el.p(
                    f"{account['account_type']} •••• {account['last_four']}",
                    class_name="text-sm text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center",
        ),
        rx.el.span(
            account["status"],
            class_name=rx.cond(
                account["status"] == "Verified",
                "px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-700",
                "px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-700",
            ),
        ),
        class_name="flex items-center justify-between p-4 border border-gray-100 rounded-2xl hover:bg-gray-50 transition-colors",
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Profile"),
        rx.el.main(
            mobile_nav(current_page="Profile"),
            rx.el.div(
                rx.el.h1(
                    "My Profile", class_name="text-2xl font-bold text-gray-900 mb-1"
                ),
                rx.el.p(
                    "Manage your personal information and account settings.",
                    class_name="text-gray-500 text-sm mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.image(
                                        src=ProfileState.avatar_url,
                                        class_name="w-24 h-24 rounded-full border-4 border-white shadow-lg",
                                    ),
                                    rx.el.button(
                                        rx.icon(
                                            "camera", size=16, class_name="text-white"
                                        ),
                                        on_click=ProfileState.upload_avatar,
                                        class_name="absolute bottom-0 right-0 p-2 bg-indigo-600 rounded-full shadow-lg hover:bg-indigo-700 transition-colors border-2 border-white",
                                    ),
                                    class_name="relative mb-6",
                                ),
                                rx.el.div(
                                    rx.el.h2(
                                        ProfileState.name,
                                        class_name="text-xl font-bold text-gray-900",
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "crown",
                                            size=14,
                                            class_name="text-amber-500 fill-amber-500",
                                        ),
                                        rx.el.span(
                                            "Premium Member",
                                            class_name="text-xs font-bold text-amber-600 uppercase tracking-wide",
                                        ),
                                        class_name="flex items-center gap-1.5 mt-1 bg-amber-50 px-3 py-1 rounded-full w-fit mx-auto",
                                    ),
                                    class_name="text-center",
                                ),
                                class_name="flex flex-col items-center p-8 bg-white rounded-3xl border border-gray-100 shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3(
                                        "Connected Accounts",
                                        class_name="text-lg font-bold text-gray-900",
                                    ),
                                    rx.el.button(
                                        rx.icon("plus", size=18),
                                        class_name="p-2 hover:bg-gray-100 rounded-full transition-colors text-gray-500",
                                    ),
                                    class_name="flex items-center justify-between mb-6",
                                ),
                                rx.el.div(
                                    rx.foreach(
                                        ProfileState.linked_accounts, account_card
                                    ),
                                    class_name="flex flex-col gap-4",
                                ),
                                class_name="p-8 bg-white rounded-3xl border border-gray-100 shadow-sm",
                            ),
                            class_name="flex flex-col gap-8",
                        ),
                        class_name="lg:col-span-1",
                    ),
                    rx.el.div(
                        rx.cond(
                            ProfileState.is_editing,
                            rx.el.form(
                                rx.el.div(
                                    rx.el.h3(
                                        "Edit Profile",
                                        class_name="text-lg font-bold text-gray-900 mb-6",
                                    ),
                                    rx.el.div(
                                        edit_field(
                                            "Full Name", "name", ProfileState.name
                                        ),
                                        edit_field(
                                            "Email Address",
                                            "email",
                                            ProfileState.email,
                                            "email",
                                        ),
                                        class_name="grid grid-cols-1 md:grid-cols-2 gap-6",
                                    ),
                                    edit_field(
                                        "Phone Number",
                                        "phone",
                                        ProfileState.phone,
                                        "tel",
                                    ),
                                    rx.el.div(
                                        rx.el.label(
                                            "Bio",
                                            class_name="block text-sm font-bold text-gray-700 mb-2",
                                        ),
                                        rx.el.textarea(
                                            name="bio",
                                            default_value=ProfileState.bio,
                                            class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all h-32 resize-none",
                                        ),
                                        class_name="mb-6",
                                    ),
                                    rx.el.div(
                                        rx.el.div(
                                            rx.el.label(
                                                "Risk Tolerance",
                                                class_name="block text-sm font-bold text-gray-700 mb-2",
                                            ),
                                            rx.el.select(
                                                rx.el.option(
                                                    "Conservative", value="Conservative"
                                                ),
                                                rx.el.option(
                                                    "Moderate", value="Moderate"
                                                ),
                                                rx.el.option(
                                                    "Aggressive", value="Aggressive"
                                                ),
                                                name="risk_tolerance",
                                                default_value=ProfileState.risk_tolerance,
                                                class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none bg-white appearance-none",
                                            ),
                                        ),
                                        rx.el.div(
                                            rx.el.label(
                                                "Investment Goal",
                                                class_name="block text-sm font-bold text-gray-700 mb-2",
                                            ),
                                            rx.el.select(
                                                rx.el.option(
                                                    "Wealth Preservation",
                                                    value="Wealth Preservation",
                                                ),
                                                rx.el.option(
                                                    "Balanced Growth",
                                                    value="Balanced Growth",
                                                ),
                                                rx.el.option(
                                                    "Long-term Growth",
                                                    value="Long-term Growth",
                                                ),
                                                name="investment_goal",
                                                default_value=ProfileState.investment_goal,
                                                class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none bg-white appearance-none",
                                            ),
                                        ),
                                        class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
                                    ),
                                    rx.el.div(
                                        rx.el.button(
                                            "Cancel",
                                            type="button",
                                            on_click=ProfileState.toggle_editing,
                                            class_name="px-6 py-2.5 text-sm font-bold text-gray-600 hover:bg-gray-50 rounded-xl transition-colors",
                                        ),
                                        rx.el.button(
                                            "Save Changes",
                                            type="submit",
                                            class_name="px-6 py-2.5 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl shadow-lg shadow-indigo-200 transition-all",
                                        ),
                                        class_name="flex items-center justify-end gap-3",
                                    ),
                                    class_name="p-8 bg-white rounded-3xl border border-gray-100 shadow-sm",
                                ),
                                on_submit=ProfileState.save_profile,
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h3(
                                        "Personal Information",
                                        class_name="text-lg font-bold text-gray-900",
                                    ),
                                    rx.el.button(
                                        rx.icon("pencil", size=16, class_name="mr-2"),
                                        "Edit Profile",
                                        on_click=ProfileState.toggle_editing,
                                        class_name="flex items-center px-4 py-2 text-sm font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-xl transition-colors",
                                    ),
                                    class_name="flex items-center justify-between mb-8",
                                ),
                                rx.el.div(
                                    info_field("Full Name", ProfileState.name, "user"),
                                    info_field(
                                        "Email Address", ProfileState.email, "mail"
                                    ),
                                    info_field(
                                        "Phone Number", ProfileState.phone, "phone"
                                    ),
                                    rx.el.div(
                                        rx.el.div(
                                            rx.icon(
                                                "file-text",
                                                size=18,
                                                class_name="text-gray-400",
                                            ),
                                            rx.el.span(
                                                "BIO",
                                                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide",
                                            ),
                                            class_name="flex items-center gap-2 mb-2",
                                        ),
                                        rx.el.p(
                                            ProfileState.bio,
                                            class_name="text-gray-900 font-medium leading-relaxed",
                                        ),
                                        class_name="p-4 bg-gray-50 rounded-xl border border-gray-100 md:col-span-2",
                                    ),
                                    class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8",
                                ),
                                rx.el.div(
                                    rx.el.h4(
                                        "Investment Profile",
                                        class_name="text-md font-bold text-gray-900 mb-6 border-t border-gray-100 pt-6",
                                    ),
                                    rx.el.div(
                                        info_field(
                                            "Risk Tolerance",
                                            ProfileState.risk_tolerance,
                                            "trending-up",
                                        ),
                                        info_field(
                                            "Investment Goal",
                                            ProfileState.investment_goal,
                                            "target",
                                        ),
                                        info_field(
                                            "Experience Level",
                                            ProfileState.experience_level,
                                            "award",
                                        ),
                                        class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                                    ),
                                ),
                                class_name="p-8 bg-white rounded-3xl border border-gray-100 shadow-sm",
                            ),
                        ),
                        class_name="lg:col-span-2",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-y-auto p-4 md:p-8",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900",
    )