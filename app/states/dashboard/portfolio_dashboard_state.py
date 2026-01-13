"""
Portfolio Dashboard State - Unified State with Mixin Architecture

This file defines the main PortfolioDashboardState class that inherits from
all domain-specific Mixins to provide a unified state interface.

Architecture:
- Uses Mixin pattern from Reflex best practices
- Each Mixin provides domain-specific state and functionality
- All data lives once in the appropriate Mixin
- Components continue to import PortfolioDashboardState for backward compatibility

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Multiple Mixin Inheritance for code organization

Original file: 2,788 lines
Refactored file: ~500 lines (this file + mixins)
"""

import random
from datetime import datetime
import reflex as rx

# Import all Mixins
from app.states.dashboard.mixins.positions_mixin import PositionsMixin
from app.states.dashboard.mixins.pnl_mixin import PnLMixin
from app.states.dashboard.mixins.risk_mixin import RiskMixin
from app.states.dashboard.mixins.compliance_mixin import ComplianceMixin
from app.states.dashboard.mixins.market_data_mixin import MarketDataMixin
from app.states.dashboard.mixins.reconciliation_mixin import ReconciliationMixin
from app.states.dashboard.mixins.operations_mixin import OperationsMixin
from app.states.dashboard.mixins.portfolio_tools_mixin import PortfolioToolsMixin
from app.states.dashboard.mixins.instruments_mixin import InstrumentsMixin
from app.states.dashboard.mixins.events_mixin import EventsMixin
from app.states.dashboard.mixins.emsx_mixin import EMSXMixin

# Import types for type hints and backwards compatibility
from app.states.dashboard.types import (
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
    TradeSummaryItem,
    PnLChangeItem,
    PnLSummaryItem,
    PnLCurrencyItem,
    PnLFullItem,
    DeltaChangeItem,
    RiskMeasureItem,
    RiskInputItem,
    RestrictedListItem,
    UndertakingItem,
    BeneficialOwnershipItem,
    MonthlyExerciseLimitItem,
    PayToHoldItem,
    ShortECLItem,
    StockBorrowItem,
    POSettlementItem,
    DealIndicationItem,
    ResetDateItem,
    ComingResetItem,
    CBInstallmentItem,
    ExcessAmountItem,
    PPSReconItem,
    SettlementReconItem,
    FailedTradeItem,
    PnLReconItem,
    RiskInputReconItem,
    DailyProcedureItem,
    OperationProcessItem,
    MarketDataItem,
    FXDataItem,
    HistoricalDataItem,
    TradingCalendarItem,
    MarketHoursItem,
    EventCalendarItem,
    EventStreamItem,
    ReverseInquiryItem,
    TickerDataItem,
    StockScreenerItem,
    SpecialTermItem,
    InstrumentDataItem,
    InstrumentTermItem,
    EMSAOrderItem,
    NotificationItem,
    KPIMetric,
    TopMover,
)


# Helper functions for formatting
def _fmt_usd(val: float) -> str:
    return f"${val:,.2f}" if val >= 0 else f"$({abs(val):,.2f})"


def _fmt_num(val: float) -> str:
    return f"{val:,.2f}" if val >= 0 else f"({abs(val):,.2f})"


def _fmt_pct(val: float) -> str:
    return f"{val:,.2f}%"


# Mock data generators (kept for backward compatibility, will be replaced by services)
def _generate_mock_data() -> list[dict]:
    """Generates mock data once at module load time."""
    base_data = [
        {
            "id": 1,
            "ticker": "AAPL",
            "description": "Apple Inc.",
            "asset_class": "Equity",
            "qty": "15,400",
            "price": "182.50",
            "mkt_value": "2,810,500",
            "daily_pnl": "+12,450",
            "pnl_pct": "+0.45%",
            "status": "Active",
            "is_positive": True,
            "is_reconciled": True,
        },
        {
            "id": 2,
            "ticker": "MSFT",
            "description": "Microsoft Corp.",
            "asset_class": "Equity",
            "qty": "8,200",
            "price": "405.12",
            "mkt_value": "3,321,984",
            "daily_pnl": "(1,230)",
            "pnl_pct": "-0.03%",
            "status": "Active",
            "is_positive": False,
            "is_reconciled": True,
        },
    ]
    expanded_data = []
    for i in range(50):
        for item in base_data:
            new_item = item.copy()
            new_item["id"] = len(expanded_data) + 1
            expanded_data.append(new_item)
    return expanded_data


class PortfolioDashboardState(
    PositionsMixin,
    PnLMixin,
    RiskMixin,
    ComplianceMixin,
    MarketDataMixin,
    ReconciliationMixin,
    OperationsMixin,
    PortfolioToolsMixin,
    InstrumentsMixin,
    EventsMixin,
    EMSXMixin,
    rx.State,
):
    """
    Unified Portfolio Dashboard State.

    This class inherits from all domain-specific Mixins to provide
    a single state interface for the portfolio dashboard.

    NOTE: UI state variables are defined directly here (not in a Mixin)
    because Reflex's compilation-time evaluation of event handlers
    doesn't work correctly with Mixin-inherited boolean state variables.

    Components continue to use PortfolioDashboardState for full backward compatibility.
    """

    # =====================================================
    # UI State Variables (defined directly to avoid Mixin issues)
    # =====================================================

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
    is_loading: bool = False
    is_loading_data: bool = False
    is_exporting: bool = False

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
    export_dropdown_open: bool = False  # Used in contextual_workspace.py line 420

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
    def total_items(self) -> int:
        return len(self.filtered_table_data)

    @rx.var
    def total_pages(self) -> int:
        return max(1, (self.total_items + self.page_size - 1) // self.page_size)

    @rx.var
    def paginated_table_data(self) -> list[dict]:
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_table_data[start:end]

    @rx.var
    def filtered_table_data(self) -> list[dict]:
        """Filters the mock data based on current search query."""
        if not self.current_search_query:
            return self.sort_data(self._mock_data)

        query = self.current_search_query.lower()
        filtered = [
            item
            for item in self._mock_data
            if any(query in str(v).lower() for v in item.values())
        ]
        return self.sort_data(filtered)

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

    # Additional mock data for backward compatibility
    _mock_data: list[dict] = _generate_mock_data()

    async def on_load(self):
        """Load all data when dashboard loads."""
        # Load data from all mixins
        await self.load_positions_data()
        await self.load_pnl_data()
        await self.load_risk_data()
        await self.load_compliance_data()
        await self.load_market_data()
        await self.load_reconciliation_data()
        await self.load_emsa_data()
        await self.load_operations_data()
        await self.load_instruments_data()
        await self.load_portfolio_tools_data()
        await self.load_events_data()
        # Load notifications and top movers from services
        await self._load_notifications()
        await self._load_top_movers()
        # Load KPI metrics from service
        await self._load_kpi_metrics()

    async def _load_notifications(self):
        """Load notifications from NotificationService."""
        try:
            from app.services import NotificationService

            service = NotificationService()
            notifications = await service.get_notifications(limit=10)
            # Convert to expected format
            self.notifications = [
                {
                    "id": int(n.get("id", i + 1)),
                    "header": n.get("title", "Notification"),
                    "ticker": n.get("message", "").split()[-1]
                    if n.get("message")
                    else "N/A",
                    "timestamp": n.get("time_ago", "Just now"),
                    "instruction": n.get("message", ""),
                    "type": "alert" if n.get("category") == "Alerts" else "info",
                    "read": n.get("is_read", False),
                }
                for i, n in enumerate(notifications)
            ]
        except Exception as e:
            import logging

            logging.exception(f"Error loading notifications: {e}")
            # Fallback to empty list
            self.notifications = []

    async def _load_top_movers(self):
        """Load top movers data from MarketDataService."""
        try:
            from app.services import MarketDataService

            service = MarketDataService()
            self.top_movers_ops = await service.get_top_movers("ops")
            self.top_movers_ytd = await service.get_top_movers("ytd")
            self.top_movers_delta = await service.get_top_movers("delta")
            self.top_movers_price = await service.get_top_movers("price")
            self.top_movers_volume = await service.get_top_movers("volume")
        except Exception as e:
            import logging

            logging.exception(f"Error loading top movers: {e}")
            # Fallback to empty lists
            self.top_movers_ops = []
            self.top_movers_ytd = []
            self.top_movers_delta = []
            self.top_movers_price = []
            self.top_movers_volume = []

    async def _load_kpi_metrics(self):
        """Load KPI metrics from PnLService."""
        try:
            from app.services import PnLService

            service = PnLService()
            self.kpi_metrics = await service.get_kpi_metrics()
        except Exception as e:
            import logging

            logging.exception(f"Error loading KPI metrics: {e}")
            # Fallback to empty list
            self.kpi_metrics = []

    @rx.event
    def add_simulated_notification(self):
        """Add a simulated notification for testing."""
        new_id = max([n.get("id", 0) for n in self.notifications], default=0) + 1
        types = ["alert", "info", "warning"]
        tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "META"]
        headers = ["Price Alert", "Volume Spike", "Risk Warning", "Settlement Notice"]

        new_notification = {
            "id": new_id,
            "header": random.choice(headers),
            "ticker": random.choice(tickers),
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "instruction": f"Simulated notification #{new_id}",
            "type": random.choice(types),
            "read": False,
        }
        self.notifications = [new_notification] + self.notifications

    # =====================================================
    # UI Event Handlers (defined here instead of UIMixin
    # to avoid Reflex compilation issues with Mixin methods)
    # =====================================================

    @rx.event
    def set_module(self, module_name: str):
        """Sets the active module."""
        self.active_module = module_name
        self.is_mobile_menu_open = False

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
    def toggle_top_movers(self):
        self.show_top_movers = not self.show_top_movers

    @rx.event
    def toggle_export_dropdown(self):
        self.is_export_dropdown_open = not self.is_export_dropdown_open
        self.export_dropdown_open = self.is_export_dropdown_open  # Keep in sync

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
        if self.current_page < self.total_pages:
            self.current_page += 1

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
        # Use XOR to avoid 'not current' which triggers __bool__ during compilation
        self._filters[self.active_module]["auto_refresh"] = current ^ True

    @rx.event
    def handle_generate(self, action: str):
        # Placeholder for generation logic
        self.is_generate_menu_open = False

    @rx.event
    def refresh_prices(self):
        self.is_loading = True
        # In a real app, this would call a service
        self.is_loading = False

    @rx.event
    def export_data(self, format: str):
        self.is_exporting = True
        self.is_export_dropdown_open = False
        self.export_dropdown_open = False
        # Placeholder for export logic
        self.is_exporting = False

    @rx.event
    def set_subtab(self, subtab_name: str):
        """Sets the active subtab for the CURRENT module."""
        self._active_subtabs[self.active_module] = subtab_name

    # Notification event handlers
    @rx.event
    def next_notification_page(self):
        if self.notification_page < self.total_notification_pages:
            self.notification_page += 1

    @rx.event
    def prev_notification_page(self):
        if self.notification_page > 1:
            self.notification_page -= 1

    @rx.event
    def set_notification_filter(self, filter_val: str):
        self.notification_filter = filter_val
        self.notification_page = 1

    @rx.event
    def mark_notification_read(self, notif_id: int):
        for n in self.notifications:
            if n.get("id") == notif_id:
                n["read"] = True
                break

    @rx.event
    def navigate_to_notification(self, notif_id: int):
        self.mark_notification_read(notif_id)

    @rx.event
    def dismiss_notification(self, id: int):
        """Removes a notification by ID."""
        self.notifications = [n for n in self.notifications if n.get("id") != id]

    # Computed vars for filtered data (backward compatibility)
    @rx.var(cache=True)
    def filtered_positions(self) -> list[PositionItem]:
        return self._filter_by_ticker(self.positions, self.current_search_query)

    @rx.var(cache=True)
    def filtered_stock_positions(self) -> list[StockPositionItem]:
        return self._filter_by_ticker(self.stock_positions, self.current_search_query)

    @rx.var(cache=True)
    def filtered_warrant_positions(self) -> list[WarrantPositionItem]:
        return self._filter_by_ticker(self.warrant_positions, self.current_search_query)

    @rx.var(cache=True)
    def filtered_bond_positions(self) -> list[BondPositionItem]:
        return self._filter_by_ticker(self.bond_positions, self.current_search_query)

    @rx.var(cache=True)
    def filtered_trade_summaries(self) -> list[TradeSummaryItem]:
        return self._filter_by_ticker(self.trade_summaries, self.current_search_query)

    @rx.var(cache=True)
    def filtered_pnl_change(self) -> list[PnLChangeItem]:
        return self._filter_pnl_by_ticker(
            self.pnl_change_list, self.current_search_query
        )

    @rx.var(cache=True)
    def filtered_pnl_summary(self) -> list[PnLSummaryItem]:
        return self._filter_pnl_by_ticker(
            self.pnl_summary_list, self.current_search_query
        )

    @rx.var(cache=True)
    def filtered_pnl_full(self) -> list[PnLFullItem]:
        return self._filter_pnl_by_ticker(self.pnl_full_list, self.current_search_query)

    @rx.var(cache=True)
    def filtered_pnl_currency(self) -> list[PnLCurrencyItem]:
        if not self.current_search_query:
            return self.pnl_currency_list
        query = self.current_search_query.lower()
        return [
            item
            for item in self.pnl_currency_list
            if query in item.get("currency", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_restricted_list(self) -> list[RestrictedListItem]:
        return self._filter_by_ticker(self.restricted_list, self.current_search_query)

    @rx.var(cache=True)
    def filtered_undertakings(self) -> list[UndertakingItem]:
        return self._filter_by_ticker(self.undertakings, self.current_search_query)

    @rx.var(cache=True)
    def filtered_beneficial_ownership(self) -> list[BeneficialOwnershipItem]:
        return self._filter_by_ticker(
            self.beneficial_ownership, self.current_search_query
        )

    @rx.var(cache=True)
    def filtered_monthly_exercise_limit(self) -> list[MonthlyExerciseLimitItem]:
        return self._filter_by_ticker(
            self.monthly_exercise_limit, self.current_search_query
        )

    @rx.var(cache=True)
    def filtered_pth(self) -> list[PayToHoldItem]:
        return self._filter_by_ticker(self.pay_to_hold, self.current_search_query)

    @rx.var(cache=True)
    def filtered_short_ecl(self) -> list[ShortECLItem]:
        return self._filter_by_ticker(self.short_ecl, self.current_search_query)

    @rx.var(cache=True)
    def filtered_stock_borrow(self) -> list[StockBorrowItem]:
        return self._filter_by_ticker(self.stock_borrow, self.current_search_query)

    @rx.var(cache=True)
    def filtered_po_settlement(self) -> list[POSettlementItem]:
        return self._filter_by_ticker(self.po_settlement, self.current_search_query)

    @rx.var(cache=True)
    def filtered_deal_indication(self) -> list[DealIndicationItem]:
        return self._filter_by_ticker(self.deal_indication, self.current_search_query)

    @rx.var(cache=True)
    def filtered_reset_dates(self) -> list[ResetDateItem]:
        return self._filter_by_ticker(self.reset_dates, self.current_search_query)

    @rx.var(cache=True)
    def filtered_coming_resets(self) -> list[ComingResetItem]:
        return self._filter_by_ticker(self.coming_resets, self.current_search_query)

    @rx.var(cache=True)
    def filtered_cb_installments(self) -> list[CBInstallmentItem]:
        return self._filter_by_ticker(self.cb_installments, self.current_search_query)

    @rx.var(cache=True)
    def filtered_excess_amount(self) -> list[ExcessAmountItem]:
        return self._filter_by_ticker(self.excess_amount, self.current_search_query)

    @rx.var(cache=True)
    def filtered_pps_recon(self) -> list[PPSReconItem]:
        return self._filter_by_ticker(self.pps_recon, self.current_search_query)

    @rx.var(cache=True)
    def filtered_settlement_recon(self) -> list[SettlementReconItem]:
        return self._filter_by_ticker(self.settlement_recon, self.current_search_query)

    @rx.var(cache=True)
    def filtered_failed_trades(self) -> list[FailedTradeItem]:
        return self._filter_by_ticker(self.failed_trades, self.current_search_query)

    @rx.var(cache=True)
    def filtered_pnl_recon(self) -> list[PnLReconItem]:
        if not self.current_search_query:
            return self.pnl_recon
        query = self.current_search_query.lower()
        return [
            item
            for item in self.pnl_recon
            if query in item.get("underlying", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_risk_input_recon(self) -> list[RiskInputReconItem]:
        return self._filter_by_ticker(self.risk_input_recon, self.current_search_query)

    @rx.var(cache=True)
    def filtered_daily_procedures(self) -> list[DailyProcedureItem]:
        if not self.current_search_query:
            return self.daily_procedures
        query = self.current_search_query.lower()
        return [
            item
            for item in self.daily_procedures
            if query in item.get("procedure_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_operation_processes(self) -> list[OperationProcessItem]:
        return self._filter_by_ticker(
            self.operation_processes, self.current_search_query
        )

    @rx.var(cache=True)
    def filtered_market_data(self) -> list[MarketDataItem]:
        return self._filter_by_ticker(self.market_data, self.current_search_query)

    @rx.var(cache=True)
    def filtered_fx_data(self) -> list[FXDataItem]:
        return self._filter_by_ticker(self.fx_data, self.current_search_query)

    @rx.var(cache=True)
    def filtered_historical_data(self) -> list[HistoricalDataItem]:
        return self._filter_by_ticker(self.historical_data, self.current_search_query)

    @rx.var(cache=True)
    def filtered_trading_calendar(self) -> list[TradingCalendarItem]:
        if not self.current_search_query:
            return self.trading_calendar
        query = self.current_search_query.lower()
        return [
            item
            for item in self.trading_calendar
            if query in item.get("trade_date", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_market_hours(self) -> list[MarketHoursItem]:
        if not self.current_search_query:
            return self.market_hours
        query = self.current_search_query.lower()
        return [
            item
            for item in self.market_hours
            if query in item.get("market", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_event_calendar(self) -> list[EventCalendarItem]:
        return self._filter_by_ticker(self.event_calendar, self.current_search_query)

    @rx.var(cache=True)
    def filtered_event_stream(self) -> list[EventStreamItem]:
        if not self.current_search_query:
            return self.event_stream
        query = self.current_search_query.lower()
        return [
            item
            for item in self.event_stream
            if query in item.get("symbol", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_reverse_inquiry(self) -> list[ReverseInquiryItem]:
        return self._filter_by_ticker(self.reverse_inquiry, self.current_search_query)

    @rx.var(cache=True)
    def filtered_ticker_data(self) -> list[TickerDataItem]:
        return self._filter_by_ticker(self.ticker_data, self.current_search_query)

    @rx.var(cache=True)
    def filtered_stock_screener(self) -> list[StockScreenerItem]:
        return self._filter_by_ticker(self.stock_screener, self.current_search_query)

    @rx.var(cache=True)
    def filtered_special_terms(self) -> list[SpecialTermItem]:
        return self._filter_by_ticker(self.special_terms, self.current_search_query)

    @rx.var(cache=True)
    def filtered_instrument_data(self) -> list[InstrumentDataItem]:
        return self._filter_by_ticker(self.instrument_data, self.current_search_query)

    @rx.var(cache=True)
    def filtered_instrument_terms(self) -> list[InstrumentTermItem]:
        return self._filter_by_ticker(self.instrument_terms, self.current_search_query)

    @rx.var(cache=True)
    def filtered_delta_changes(self) -> list[DeltaChangeItem]:
        return self._filter_risk_by_ticker(
            self.delta_changes, self.current_search_query
        )

    @rx.var(cache=True)
    def filtered_risk_measures(self) -> list[RiskMeasureItem]:
        return self._filter_risk_by_ticker(
            self.risk_measures, self.current_search_query
        )

    @rx.var(cache=True)
    def filtered_risk_inputs(self) -> list[RiskInputItem]:
        return self._filter_risk_by_ticker(self.risk_inputs, self.current_search_query)

    @rx.var(cache=True)
    def filtered_emsa_orders(self) -> list[EMSAOrderItem]:
        return self._filter_by_ticker(self.emsa_orders, self.current_search_query)

    @rx.var(cache=True)
    def filtered_emsa_routes(self) -> list[dict]:
        return self._filter_by_ticker(self.emsa_routes, self.current_search_query)

    # Pagination helpers for computed data

    def _get_paginated_data(self, data: list[dict]) -> list[dict]:
        """Return paginated subset of data."""
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return data[start:end]
