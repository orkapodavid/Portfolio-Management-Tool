"""
UI Mixin - State variables for shared UI state

This Mixin provides UI-related state VARIABLES only.
Event handlers are defined in the main PortfolioDashboardState class
because Reflex evaluates event handlers during compilation, which
causes issues with Mixin inheritance.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for data storage
"""

import reflex as rx
from app.states.dashboard.types import NotificationItem, KPIMetric, TopMover


class UIMixin(rx.State, mixin=True):
    """
    Mixin providing shared UI state VARIABLES.

    NOTE: Event handlers are defined in PortfolioDashboardState to avoid
    Reflex compilation issues with Mixin event handlers.

    Provides:
    - Navigation state (active module, subtabs)
    - Sidebar state
    - Mobile menu state
    - Notifications
    - Pagination and sorting
    """

    # Navigation state
    active_module: str = "Market Data"
    _active_subtabs: dict[str, str] = {}
    _filters: dict[str, dict] = {}

    # UI state
    is_sidebar_open: bool = True
    is_mobile_menu_open: bool = False
    is_generate_menu_open: bool = False
    is_export_dropdown_open: bool = False
    show_top_movers: bool = False

    # Pagination state
    current_page: int = 1
    page_size: int = 20
    page_size_options: list[int] = [10, 20, 50, 100]

    # Sorting state
    sort_column: str = ""
    sort_direction: str = "asc"

    # Selected row state
    selected_row_id: int = -1

    # Notification state
    notification_page: int = 1
    notification_page_size: int = 5
    notification_filter: str = "all"

    # KPI Metrics for header
    kpi_metrics: list[KPIMetric] = [
        {
            "label": "Total NAV",
            "value": "$2.4B",
            "is_positive": True,
            "trend_data": "+2.5%",
        },
        {
            "label": "Daily P&L",
            "value": "+$12.5M",
            "is_positive": True,
            "trend_data": "+0.5%",
        },
        {
            "label": "YTD Return",
            "value": "+18.2%",
            "is_positive": True,
            "trend_data": "vs 15% benchmark",
        },
        {
            "label": "Net Exposure",
            "value": "72%",
            "is_positive": True,
            "trend_data": "Target: 70-80%",
        },
    ]

    # Top movers data
    top_movers_ops: list[TopMover] = []
    top_movers_ytd: list[TopMover] = []
    top_movers_delta: list[TopMover] = []
    top_movers_price: list[TopMover] = []
    top_movers_volume: list[TopMover] = []

    # Notifications list
    notifications: list[NotificationItem] = []

    # Module configuration
    module_icons: dict[str, str] = {
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

    MODULE_CATEGORIES: dict[str, list[str]] = {
        "Trading": ["Market Data", "Positions", "Orders", "EMSA"],
        "Analytics": ["PnL", "Risk"],
        "Operations": ["Recon", "Compliance", "Operations"],
        "Reference": ["Instruments", "Events", "Portfolio Tools"],
    }

    MODULE_SUBTABS: dict[str, list[str]] = {
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

    # Computed vars for navigation (these are fine in mixins)
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

    @rx.var
    def current_search_query(self) -> str:
        return self._filters.get(self.active_module, {}).get("search", "")

    @rx.var
    def current_date_filter(self) -> str:
        return self._filters.get(self.active_module, {}).get("date", "")

    @rx.var
    def current_auto_refresh(self) -> bool:
        return self._filters.get(self.active_module, {}).get("auto_refresh", False)

    @rx.var
    def total_notification_pages(self) -> int:
        total = len(self.filtered_notifications_list)
        return max(
            1, (total + self.notification_page_size - 1) // self.notification_page_size
        )

    @rx.var
    def paginated_notifications(self) -> list[NotificationItem]:
        start = (self.notification_page - 1) * self.notification_page_size
        end = start + self.notification_page_size
        return self.filtered_notifications_list[start:end]

    @rx.var
    def unread_count(self) -> int:
        return len([n for n in self.notifications if not n.get("read", False)])

    @rx.var
    def filtered_notifications_list(self) -> list[NotificationItem]:
        """Filter notifications based on selected filter."""
        if self.notification_filter == "all":
            return self.notifications
        elif self.notification_filter == "unread":
            return [n for n in self.notifications if not n.get("read", False)]
        else:
            return [
                n
                for n in self.notifications
                if n.get("type", "") == self.notification_filter
            ]

    def sort_data(self, data: list[dict]) -> list[dict]:
        """Sort data based on current sort column and direction."""
        if not self.sort_column or not data:
            return data

        def get_sort_key(item):
            value = item.get(self.sort_column, "")
            if isinstance(value, str):
                # Try to parse as number
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
