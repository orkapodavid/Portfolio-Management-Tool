import reflex as rx
from app.components.top_navigation import top_navigation
from app.components.performance_header import performance_header
from app.components.contextual_workspace import contextual_workspace
from app.components.notification_sidebar import notification_sidebar
from app.pages.portfolio_page import portfolio_page
from app.pages.watchlist_page import watchlist_page
from app.pages.research_page import research_page
from app.pages.reports_page import reports_page
from app.pages.goals_page import goals_page
from app.pages.profile_page import profile_page
from app.pages.notifications_page import notifications_page
from app.pages.settings_page import settings_page
from app.constants import FINANCIAL_GREY, DEFAULT_FONT


def index() -> rx.Component:
    return rx.el.div(
        top_navigation(),
        performance_header(),
        rx.el.div(
            contextual_workspace(),
            notification_sidebar(),
            class_name=f"flex flex-1 overflow-hidden min-h-0 bg-[{FINANCIAL_GREY}] w-full",
        ),
        class_name=f"flex flex-col h-screen w-screen bg-[{FINANCIAL_GREY}] font-['{DEFAULT_FONT}'] antialiased overflow-hidden",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="blue"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/")
app.add_page(portfolio_page, route="/portfolios")
app.add_page(watchlist_page, route="/watchlist")
app.add_page(research_page, route="/research")
app.add_page(reports_page, route="/reports")
app.add_page(goals_page, route="/goals")
app.add_page(profile_page, route="/profile")
app.add_page(notifications_page, route="/notifications")
app.add_page(settings_page, route="/settings")