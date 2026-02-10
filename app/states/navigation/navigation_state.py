"""
Navigation State - Global navigation and UI state

This module handles cross-cutting navigation concerns:
- Active module tracking
- Subtab navigation per module
- Mobile menu state
- Sidebar toggle
- Module icons and configuration

This state is used by shared components like top_navigation.py.
"""

import reflex as rx
from typing import ClassVar


class NavigationState(rx.State):
    """
    Global navigation state for module-based routing.

    This state is separate from domain-specific states (PnL, Positions, etc.)
    and handles the navigation UI across the entire application.
    """

    # Current active module
    active_module: str = "Market Data"

    # Active subtab per module (dict maps module name to active subtab)
    _active_subtabs: dict[str, str] = {}

    # UI toggles
    is_sidebar_open: bool = True
    is_mobile_menu_open: bool = False

    # Module configuration - icons for navigation
    module_icons: ClassVar[dict[str, str]] = {
        "Market Data": "bar-chart-2",
        "Positions": "briefcase",
        "PnL": "dollar-sign",
        "Risk": "shield-alert",
        "Recon": "file-check-2",
        "Compliance": "scale",
        "Portfolio Tools": "wrench",
        "Instruments": "layers",
        "Events": "calendar",
        "Operations": "settings",
        "Orders": "shopping-cart",
    }

    MODULE_CATEGORIES: ClassVar[dict[str, list[str]]] = {
        "Trading": ["Market Data", "Positions", "Orders"],
        "Analytics": ["PnL", "Risk"],
        "Operations": ["Recon", "Compliance", "Operations"],
        "Reference": ["Instruments", "Events", "Portfolio Tools"],
    }

    MODULE_SUBTABS: ClassVar[dict[str, list[str]]] = {
        "Market Data": [
            "Market Data",
            "FX Data",
            "Reference Data",
            "Historical Data",
            "Trading Calendar",
            "Market Hours",
        ],
        "Positions": [
            "Positions",
            "Stock Position",
            "Warrant Position",
            "Bond Positions",
            "Trade Summary (War/Bond)",
        ],
        "PnL": ["PnL Change", "PnL Full", "PnL Summary", "PnL Currency"],
        "Risk": [
            "Delta Change",
            "Risk Measures",
            "Risk Inputs",
            "Pricer Warrant",
            "Pricer Bond",
        ],
        "Recon": [
            "PPS Recon",
            "Settlement Recon",
            "Failed Trades",
            "PnL Recon",
            "Risk Input Recon",
        ],
        "Compliance": [
            "Restricted List",
            "Undertakings",
            "Beneficial Ownership",
            "Monthly Exercise Limit",
        ],
        "Portfolio Tools": [
            "Pay-To-Hold",
            "Short ECL",
            "Stock Borrow",
            "PO Settlement",
            "Deal Indication",
            "Reset Dates",
            "Coming Resets",
            "CB Installments",
            "Excess Amount",
        ],
        "Instruments": [
            "Ticker Data",
            "Stock Screener",
            "Special Term",
            "Instrument Data",
            "Instrument Term",
        ],
        "Events": ["Event Calendar", "Event Stream", "Reverse Inquiry"],
        "Operations": ["Daily Procedure Check", "Operation Process"],
        "Orders": ["EMSX Order", "EMSX Route"],
    }

    # Computed vars for navigation
    @rx.var
    def current_subtabs(self) -> list[str]:
        """Returns the list of subtabs for the currently active module."""
        return self.MODULE_SUBTABS.get(self.active_module, [])

    @rx.var
    def active_subtab(self) -> str:
        """Returns the active subtab for the current module."""
        return self._active_subtabs.get(
            self.active_module, self.current_subtabs[0] if self.current_subtabs else ""
        )

    @rx.var
    def active_category(self) -> str:
        """Returns the category of the currently active module."""
        for category, modules in self.MODULE_CATEGORIES.items():
            if self.active_module in modules:
                return category
        return ""

    # Event handlers
    @rx.event
    def set_module(self, module_name: str):
        """Sets the active module and closes mobile menu."""
        self.active_module = module_name
        self.is_mobile_menu_open = False

    @rx.event
    def set_subtab(self, subtab_name: str):
        """Sets the active subtab for the current module."""
        self._active_subtabs[self.active_module] = subtab_name

    @rx.event
    def toggle_mobile_menu(self):
        """Toggle mobile menu visibility."""
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def toggle_sidebar(self):
        """Toggle sidebar visibility."""
        self.is_sidebar_open = not self.is_sidebar_open
