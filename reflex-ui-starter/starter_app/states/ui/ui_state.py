"""
UI State - Global UI state management

Handles:
- Navigation (Active Module, Subtabs)
- Sidebar State
- Mobile Menu
- Global Settings/Filters
"""

import reflex as rx
from typing import Any


class UIState(rx.State):
    """
    Global UI state management.
    """

    # Navigation state
    active_module: str = "Dashboard"
    _active_subtabs: dict[str, str] = {}
    _filters: dict[str, dict[str, Any]] = {}

    # UI state
    is_sidebar_open: bool = True
    is_mobile_menu_open: bool = False
    is_loading: bool = False

    # Module configuration
    MODULE_ICONS: dict[str, str] = {
        "Dashboard": "layout-dashboard",
        "Market Data": "bar-chart-3",
        "Settings": "settings",
    }

    MODULE_SUBTABS: dict[str, list[str]] = {
        "Dashboard": ["Overview", "Analytics"],
        "Market Data": ["FX Data", "Reference Data"],
    }

    # Computed vars
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

    # Event Handlers
    @rx.event
    def set_module(self, module_name: str):
        """Sets the active module."""
        self.active_module = module_name
        self.is_mobile_menu_open = False
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
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def redirect_to_default(self):
        """Redirect to the default Dashboard page when accessing root route."""
        return rx.redirect("/dashboard/overview")
