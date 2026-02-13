"""Starter App — Reflex Application Entry Point

Defines routes for 2 demo modules:
- Dashboard: Overview, Analytics (Market Data AG Grid)
- Market Data: FX Data, Reference Data (AG Grid pages)

Uses the page/tab/notification UI pattern with mixin state architecture.
Data flows: core_pkg → services → mixin states → pages.
All grids use ag_grid_config factory with toolbar + notification navigation.
"""

import reflex as rx

# States
from starter_app.states.ui.ui_state import UIState
from starter_app.states.dashboard import DashboardState
from starter_app.states.market_data import MarketDataState

# Pages
from starter_app.pages.dashboard.overview_page import overview_page
from starter_app.pages.dashboard.analytics_page import analytics_page
from starter_app.pages.market_data.fx_data_page import fx_data_page
from starter_app.pages.market_data.reference_data_page import reference_data_page

# Font
font_url = "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap"

# App
app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[font_url, "/notification_highlight.css"],
)

# === Root Route ===
app.add_page(lambda: rx.fragment(), route="/", on_load=UIState.redirect_to_default)

# === Dashboard Module ===
app.add_page(
    overview_page,
    route="/dashboard",
    on_load=[UIState.set_module("Dashboard"), DashboardState.load_overview_data],
    title="Dashboard — Overview",
)
app.add_page(
    overview_page,
    route="/dashboard/overview",
    on_load=[UIState.set_module("Dashboard"), DashboardState.load_overview_data],
    title="Dashboard — Overview",
)
app.add_page(
    analytics_page,
    route="/dashboard/analytics",
    on_load=[UIState.set_module("Dashboard"), UIState.set_subtab("Analytics"), DashboardState.load_analytics_data],
    title="Dashboard — Analytics",
)

# === Market Data Module ===
app.add_page(
    fx_data_page,
    route="/market-data",
    on_load=[UIState.set_module("Market Data"), MarketDataState.load_fx_data],
    title="Market Data — FX Data",
)
app.add_page(
    fx_data_page,
    route="/market-data/fx-data",
    on_load=[UIState.set_module("Market Data"), MarketDataState.load_fx_data],
    title="Market Data — FX Data",
)
app.add_page(
    reference_data_page,
    route="/market-data/reference-data",
    on_load=[UIState.set_module("Market Data"), UIState.set_subtab("Reference Data"), MarketDataState.load_reference_data],
    title="Market Data — Reference Data",
)
