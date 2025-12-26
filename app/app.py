import reflex as rx
from app.components.sidebar import sidebar
from app.components.mobile_nav import mobile_nav
from app.components.summary_cards import portfolio_summary
from app.components.allocation_chart import allocation_chart
from app.components.holdings_table import holdings_table
from app.components.performers_widget import performers_widget
from app.components.portfolio_modals import add_transaction_modal
from app.components.goal_components import goals_summary_widget
from app.states.dashboard_state import DashboardState
from app.states.portfolio_state import PortfolioState
from app.states.reports_state import ReportsState
from app.pages.portfolio_page import portfolio_page
from app.pages.watchlist_page import watchlist_page
from app.pages.research_page import research_page
from app.pages.reports_page import reports_page
from app.pages.goals_page import goals_page


def dashboard_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Dashboard",
                class_name="text-3xl font-bold text-gray-900 tracking-tight",
            ),
            rx.el.div(
                rx.el.p(
                    "Welcome back, Alex. Here's your portfolio overview.",
                    class_name="text-gray-500 font-medium",
                ),
                rx.cond(
                    DashboardState.last_updated != "",
                    rx.el.p(
                        f"Last updated: {DashboardState.last_updated}",
                        class_name="text-xs text-gray-400 mt-1",
                    ),
                ),
                class_name="flex flex-col mt-1",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    DashboardState.periods,
                    lambda period: rx.el.button(
                        period,
                        on_click=lambda: DashboardState.set_period(period),
                        class_name=rx.cond(
                            DashboardState.selected_period == period,
                            "px-4 py-1.5 text-xs font-bold bg-white text-indigo-600 rounded-lg shadow-sm border border-gray-100 transition-all duration-200 transform scale-105",
                            "px-4 py-1.5 text-xs font-bold text-gray-500 hover:text-gray-900 hover:bg-white/50 transition-all duration-200",
                        ),
                    ),
                ),
                class_name="p-1.5 bg-gray-100/80 backdrop-blur-sm rounded-xl flex items-center gap-1 border border-gray-100",
            ),
            rx.el.button(
                rx.cond(
                    DashboardState.is_loading,
                    rx.spinner(size="1", class_name="text-gray-500 mr-2"),
                    rx.icon("refresh-cw", size=16, class_name="mr-2 text-gray-500"),
                ),
                rx.cond(DashboardState.is_loading, "Updating...", "Refresh Prices"),
                on_click=DashboardState.refresh_prices,
                disabled=DashboardState.is_loading,
                class_name="flex items-center bg-white border border-gray-200 text-gray-700 px-4 py-2.5 rounded-xl text-sm font-bold hover:bg-gray-50 transition-all shadow-sm",
            ),
            rx.el.button(
                rx.icon("plus", size=18, class_name="mr-2"),
                "Add Transaction",
                on_click=PortfolioState.toggle_add_transaction,
                class_name="flex items-center bg-gradient-to-r from-indigo-600 to-violet-600 text-white px-5 py-2.5 rounded-xl text-sm font-bold hover:shadow-lg hover:shadow-indigo-500/30 hover:-translate-y-0.5 transition-all duration-300",
            ),
            class_name="flex flex-col sm:flex-row items-center gap-4",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Dashboard"),
        add_transaction_modal(),
        rx.el.main(
            mobile_nav(current_page="Dashboard"),
            rx.el.div(
                dashboard_header(),
                portfolio_summary(),
                rx.el.div(
                    rx.el.div(holdings_table(), class_name="lg:col-span-2"),
                    rx.el.div(
                        goals_summary_widget(),
                        allocation_chart(),
                        performers_widget(),
                        class_name="flex flex-col gap-8 lg:col-span-1",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8",
                ),
                class_name="max-w-[1600px] mx-auto w-full",
            ),
            class_name="flex-1 bg-[#F8FAFC] h-screen overflow-y-auto p-4 md:p-8 lg:p-10 scroll-smooth",
        ),
        class_name="flex w-full h-screen font-['Inter'] text-gray-900 antialiased selection:bg-indigo-100 selection:text-indigo-900 overflow-hidden",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/", on_load=DashboardState.refresh_prices)
app.add_page(portfolio_page, route="/portfolios")
app.add_page(watchlist_page, route="/watchlist")
app.add_page(research_page, route="/research")
app.add_page(reports_page, route="/reports", on_load=ReportsState.on_mount)
app.add_page(goals_page, route="/goals")
from app.pages.profile_page import profile_page
from app.pages.notifications_page import notifications_page
from app.pages.settings_page import settings_page

app.add_page(profile_page, route="/profile")
app.add_page(notifications_page, route="/notifications")
app.add_page(settings_page, route="/settings")