"""
UI State - Global UI state management

Handles:
- Navigation (Active Module, Subtabs)
- Sidebar State
- Mobile Menu
- Global Settings/Filters
- Notifications
"""

import reflex as rx
from typing import Dict, List, Any
import random
from datetime import datetime
from app.states.types import GenericTableItem


class UIState(rx.State):
    """
    Global UI state management.
    """

    # Navigation state
    active_module: str = "Market Data"
    _active_subtabs: Dict[str, str] = {}
    _filters: Dict[str, Dict[str, Any]] = {}

    # UI state
    is_sidebar_open: bool = True
    is_mobile_menu_open: bool = False
    is_generate_menu_open: bool = False
    is_export_dropdown_open: bool = False
    is_loading: bool = False
    is_loading_data: bool = False
    is_exporting: bool = False

    # Sorting state
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row_id: int = 0

    # Pagination state
    current_page: int = 1
    page_size: int = 20
    page_size_options: List[int] = [10, 20, 50, 100]
    total_pages: int = 1
    total_items: int = 0
    paginated_table_data: List[GenericTableItem] = []

    @rx.event
    def refresh_prices(self):
        """Refreshes data for the active module."""
        # Placeholder for global refresh logic
        pass

    # Module configuration
    MODULE_ICONS: Dict[str, str] = {
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

    MODULE_CATEGORIES: Dict[str, List[str]] = {
        "Trading": ["Market Data", "Positions", "Orders"],
        "Analytics": ["PnL", "Risk"],
        "Operations": ["Recon", "Compliance", "Operations"],
        "Reference": ["Instruments", "Events", "Portfolio Tools"],
    }

    MODULE_SUBTABS: Dict[str, List[str]] = {
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

    # Computed vars
    @rx.var
    def current_subtabs(self) -> List[str]:
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

    @rx.var
    def current_search_query(self) -> str:
        return self._filters.get(self.active_module, {}).get("search", "")

    @rx.var
    def current_date_filter(self) -> str:
        return self._filters.get(self.active_module, {}).get("date", "")

    # Event Handlers
    @rx.event
    def set_module(self, module_name: str):
        """Sets the active module."""
        self.active_module = module_name
        self.is_mobile_menu_open = False
        # Initialize subtab if not set
        if module_name not in self._active_subtabs and self.MODULE_SUBTABS.get(
            module_name
        ):
            self._active_subtabs[module_name] = self.MODULE_SUBTABS[module_name][0]

    @rx.event
    def set_subtab(self, subtab_name: str):
        """Sets the active subtab for the CURRENT module."""
        self._active_subtabs[self.active_module] = subtab_name

    @rx.event
    def toggle_mobile_menu(self):
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def toggle_generate_menu(self):
        self.is_generate_menu_open = not self.is_generate_menu_open

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_export_dropdown(self):
        self.is_export_dropdown_open = not self.is_export_dropdown_open

    @rx.event
    def toggle_sort(self, column: str):
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"

    @rx.event
    def set_page_size(self, size: str):
        self.page_size = int(size)
        self.current_page = 1

    @rx.event
    def next_page(self):
        # Note: total_pages is not defined in UIState yet, might need to add it or pass it
        # For now, simplistic implementation or placeholder
        pass

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def set_page(self, page: int):
        self.current_page = page

    @rx.event
    def set_selected_row(self, row_id: int):
        self.selected_row_id = row_id

    @rx.event
    def set_current_search(self, query: str):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["search"] = query
        self.current_page = 1

    @rx.event
    def clear_search(self):
        if self.active_module in self._filters:
            self._filters[self.active_module]["search"] = ""
        self.current_page = 1

    @rx.event
    def set_current_date(self, date_str: str):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["date"] = date_str

    @rx.event
    def toggle_auto_refresh(self):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        current = self._filters[self.active_module].get("auto_refresh", False)
        self._filters[self.active_module]["auto_refresh"] = current ^ True

    @rx.event
    def handle_generate(self, action: str):
        self.is_generate_menu_open = False

    @rx.event
    def export_data(self, format: str):
        self.is_export_dropdown_open = False

    @rx.event
    def redirect_to_default(self):
        """Redirect to the default Market Data page when accessing root route."""
        return rx.redirect("/market-data/market-data")

    def sort_data(self, data: list[dict]) -> list[dict]:
        """Sort data based on current sort column and direction."""
        if not self.sort_column or not data:
            return data

        def get_sort_key(item):
            value = item.get(self.sort_column, "")
            if isinstance(value, str):
                cleaned = (
                    value.replace("$", "")
                    .replace(",", "")
                    .replace("(", "-")
                    .replace(")", "")
                    .replace("%", "")
                )
                try:
                    return float(cleaned)
                except ValueError:
                    return value.lower()
            return value

        return sorted(
            data,
            key=get_sort_key,
            reverse=(self.sort_direction == "desc"),
        )
