import random
from datetime import datetime
from typing import TypedDict
import reflex as rx


class NotificationItem(TypedDict):
    id: int
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str
    read: bool


class KPIMetric(TypedDict):
    label: str
    value: str
    is_positive: bool


class TopMover(TypedDict):
    ticker: str
    name: str
    value: str
    change: str
    is_positive: bool


class PnLChangeItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    ticker: str
    pnl_ytd: str
    pnl_chg_1d: str
    pnl_chg_2d: str
    pnl_chg_1w: str
    pnl_chg_1m: str
    pnl_chg_pct_1d: str
    pnl_chg_pct_2d: str
    pnl_chg_pct_1w: str
    pnl_chg_pct_1m: str
    sparkline_data: list[float]
    sparkline_svg: str
    sparkline_color: str
    is_reconciled: bool


class PnLSummaryItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    currency: str
    price: str
    price_t_1: str
    price_change: str
    fx_rate: str
    fx_rate_t_1: str
    fx_rate_change: str
    dtl: str
    last_volume: str
    adv_3m: str


class PnLCurrencyItem(TypedDict):
    id: int
    trade_date: str
    currency: str
    fx_rate: str
    fx_rate_t_1: str
    fx_rate_change: str
    ccy_exposure: str
    usd_exposure: str
    pos_ccy_expo: str
    ccy_hedged_pnl: str
    pos_ccy_pnl: str
    net_ccy: str


def _fmt_usd(val: float) -> str:
    return f"${val:,.2f}" if val >= 0 else f"$({abs(val):,.2f})"


def _fmt_num(val: float) -> str:
    return f"{val:,.2f}" if val >= 0 else f"({abs(val):,.2f})"


def _fmt_pct(val: float) -> str:
    return f"{val:,.2f}%"


def _generate_pnl_change_data() -> list[PnLChangeItem]:
    tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "TSLA",
        "NVDA",
        "META",
        "NFLX",
        "AMD",
        "INTC",
        "JPM",
        "BAC",
        "WFC",
        "C",
        "GS",
        "MS",
        "BLK",
        "SPY",
        "QQQ",
        "IWM",
    ]
    data = []
    for i, ticker in enumerate(tickers):
        base_pnl = random.uniform(-50000, 150000)
        chg_1d = random.uniform(-5000, 5000)
        sparkline = [random.uniform(100, 150) for _ in range(10)]
        min_val = min(sparkline)
        max_val = max(sparkline)
        range_val = max_val - min_val if max_val > min_val else 1
        points = []
        width = 80
        height = 24
        step = width / (len(sparkline) - 1)
        for idx, val in enumerate(sparkline):
            x = idx * step
            normalized = (val - min_val) / range_val
            y = height - 4 - normalized * (height - 4) + 2
            points.append(f"{x:.1f},{y:.1f}")
        sparkline_svg = " ".join(points)
        sparkline_color = "#059669" if sparkline[-1] >= sparkline[0] else "#DC2626"
        is_reconciled = random.choice([True, True, True, False])
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "underlying": f"{ticker} US Equity",
                "ticker": ticker,
                "pnl_ytd": _fmt_usd(base_pnl),
                "pnl_chg_1d": _fmt_usd(chg_1d),
                "pnl_chg_2d": _fmt_usd(chg_1d * 1.2),
                "pnl_chg_1w": _fmt_usd(chg_1d * 3.5),
                "pnl_chg_1m": _fmt_usd(chg_1d * 12.0),
                "pnl_chg_pct_1d": _fmt_pct(random.uniform(-3, 3)),
                "pnl_chg_pct_2d": _fmt_pct(random.uniform(-4, 4)),
                "pnl_chg_pct_1w": _fmt_pct(random.uniform(-8, 8)),
                "pnl_chg_pct_1m": _fmt_pct(random.uniform(-15, 15)),
                "sparkline_data": sparkline,
                "sparkline_svg": sparkline_svg,
                "sparkline_color": sparkline_color,
                "is_reconciled": is_reconciled,
            }
        )
    return data


def _generate_pnl_summary_data() -> list[PnLSummaryItem]:
    tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "TSLA",
        "NVDA",
        "META",
        "NFLX",
        "AMD",
        "INTC",
    ]
    currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "SGD"]
    data = []
    for i in range(20):
        ticker = tickers[i % len(tickers)]
        ccy = currencies[i % len(currencies)]
        price = random.uniform(100, 1000)
        price_t1 = price * random.uniform(0.95, 1.05)
        fx = random.uniform(0.8, 1.5)
        fx_t1 = fx * random.uniform(0.99, 1.01)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "underlying": f"{ticker} US Equity",
                "currency": ccy,
                "price": _fmt_num(price),
                "price_t_1": _fmt_num(price_t1),
                "price_change": _fmt_num(price - price_t1),
                "fx_rate": f"{fx:,.4f}",
                "fx_rate_t_1": f"{fx_t1:,.4f}",
                "fx_rate_change": _fmt_num(fx - fx_t1),
                "dtl": f"{random.uniform(0, 1000):,.0f}",
                "last_volume": f"{random.randint(100000, 5000000):,.0f}",
                "adv_3m": f"{random.randint(100000, 5000000):,.0f}",
            }
        )
    return data


def _generate_pnl_currency_data() -> list[PnLCurrencyItem]:
    currencies = [
        "USD",
        "EUR",
        "GBP",
        "JPY",
        "CAD",
        "AUD",
        "CHF",
        "CNY",
        "HKD",
        "SGD",
        "SEK",
        "NOK",
        "DKK",
        "NZD",
        "MXN",
        "BRL",
        "INR",
        "KRW",
        "ZAR",
        "TRY",
    ]
    data = []
    for i, ccy in enumerate(currencies):
        fx = random.uniform(0.5, 1.5)
        fx_t1 = fx * random.uniform(0.98, 1.02)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "currency": ccy,
                "fx_rate": f"{fx:,.4f}",
                "fx_rate_t_1": f"{fx_t1:,.4f}",
                "fx_rate_change": _fmt_num(fx - fx_t1),
                "ccy_exposure": _fmt_usd(random.uniform(-1000000, 1000000)),
                "usd_exposure": _fmt_usd(random.uniform(-1000000, 1000000)),
                "pos_ccy_expo": _fmt_usd(random.uniform(-500000, 500000)),
                "ccy_hedged_pnl": _fmt_usd(random.uniform(-10000, 10000)),
                "pos_ccy_pnl": _fmt_usd(random.uniform(-20000, 20000)),
                "net_ccy": _fmt_usd(random.uniform(-5000, 5000)),
            }
        )
    return data


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
        {
            "id": 3,
            "ticker": "US10Y",
            "description": "US Treasury 10Y",
            "asset_class": "Bond",
            "qty": "5,000,000",
            "price": "98.25",
            "mkt_value": "4,912,500",
            "daily_pnl": "+5,600",
            "pnl_pct": "+0.11%",
            "status": "Hedged",
            "is_positive": True,
            "is_reconciled": True,
        },
        {
            "id": 4,
            "ticker": "EURUSD",
            "description": "Euro / US Dollar",
            "asset_class": "FX",
            "qty": "2,500,000",
            "price": "1.0850",
            "mkt_value": "2,712,500",
            "daily_pnl": "(4,500)",
            "pnl_pct": "-0.16%",
            "status": "Active",
            "is_positive": False,
            "is_reconciled": True,
        },
        {
            "id": 5,
            "ticker": "NVDA",
            "description": "NVIDIA Corp",
            "asset_class": "Equity",
            "qty": "4,500",
            "price": "785.30",
            "mkt_value": "3,533,850",
            "daily_pnl": "+45,200",
            "pnl_pct": "+1.28%",
            "status": "Active",
            "is_positive": True,
            "is_reconciled": False,
        },
        {
            "id": 6,
            "ticker": "GLD",
            "description": "SPDR Gold Shares",
            "asset_class": "Commodity",
            "qty": "12,000",
            "price": "195.40",
            "mkt_value": "2,344,800",
            "daily_pnl": "+8,900",
            "pnl_pct": "+0.38%",
            "status": "Hedged",
            "is_positive": True,
            "is_reconciled": True,
        },
        {
            "id": 7,
            "ticker": "TSLA",
            "description": "Tesla Inc.",
            "asset_class": "Equity",
            "qty": "10,000",
            "price": "175.20",
            "mkt_value": "1,752,000",
            "daily_pnl": "(15,400)",
            "pnl_pct": "-0.88%",
            "status": "Review",
            "is_positive": False,
            "is_reconciled": False,
        },
        {
            "id": 8,
            "ticker": "VIX",
            "description": "Volatility Index",
            "asset_class": "Index",
            "qty": "5,000",
            "price": "13.45",
            "mkt_value": "67,250",
            "daily_pnl": "(250)",
            "pnl_pct": "-0.37%",
            "status": "Hedged",
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


class PortfolioDashboardState(rx.State):
    active_module: str = "Market Data"
    _active_subtabs: dict[str, str] = {}
    _filters: dict[str, dict] = {}
    is_sidebar_open: bool = True
    is_mobile_menu_open: bool = False
    is_generate_menu_open: bool = False
    show_top_movers: bool = False
    selected_row_id: int = -1
    is_loading: bool = False
    kpi_metrics: list[KPIMetric] = [
        {"label": "Daily PnL", "value": "+$1.2M", "is_positive": True},
        {"label": "Daily Pos FX", "value": "($45K)", "is_positive": False},
        {"label": "Daily CCY Hedged", "value": "+$12K", "is_positive": True},
        {"label": "YTD Disc PnL", "value": "+$45.8M", "is_positive": True},
        {"label": "YTD R/U PnL", "value": "($2.1M)", "is_positive": False},
    ]
    top_movers_ops: list[TopMover] = [
        {
            "ticker": "AAPL",
            "name": "Apple",
            "value": "$4.5M",
            "change": "+1.2%",
            "is_positive": True,
        },
        {
            "ticker": "MSFT",
            "name": "Microsoft",
            "value": "$3.2M",
            "change": "+0.8%",
            "is_positive": True,
        },
        {
            "ticker": "TSLA",
            "name": "Tesla",
            "value": "($1.5M)",
            "change": "-2.1%",
            "is_positive": False,
        },
        {
            "ticker": "NVDA",
            "name": "NVIDIA",
            "value": "$2.1M",
            "change": "+3.5%",
            "is_positive": True,
        },
    ]
    top_movers_ytd: list[TopMover] = [
        {
            "ticker": "NVDA",
            "name": "NVIDIA",
            "value": "$15.2M",
            "change": "+45%",
            "is_positive": True,
        },
        {
            "ticker": "META",
            "name": "Meta",
            "value": "$8.4M",
            "change": "+22%",
            "is_positive": True,
        },
        {
            "ticker": "PFE",
            "name": "Pfizer",
            "value": "($2.1M)",
            "change": "-12%",
            "is_positive": False,
        },
        {
            "ticker": "XOM",
            "name": "Exxon",
            "value": "$5.1M",
            "change": "+8%",
            "is_positive": True,
        },
    ]
    top_movers_delta: list[TopMover] = [
        {
            "ticker": "SPY",
            "name": "S&P 500",
            "value": "$500K",
            "change": "+0.5",
            "is_positive": True,
        },
        {
            "ticker": "QQQ",
            "name": "Nasdaq",
            "value": "$320K",
            "change": "+0.8",
            "is_positive": True,
        },
        {
            "ticker": "IWM",
            "name": "Russell",
            "value": "($120K)",
            "change": "-0.3",
            "is_positive": False,
        },
        {
            "ticker": "GLD",
            "name": "Gold",
            "value": "$50K",
            "change": "+0.1",
            "is_positive": True,
        },
    ]
    top_movers_price: list[TopMover] = [
        {
            "ticker": "AMD",
            "name": "AMD",
            "value": "$180.5",
            "change": "+5.2%",
            "is_positive": True,
        },
        {
            "ticker": "COIN",
            "name": "Coinbase",
            "value": "$240.2",
            "change": "+8.4%",
            "is_positive": True,
        },
        {
            "ticker": "SNOW",
            "name": "Snowflake",
            "value": "$160.1",
            "change": "-15%",
            "is_positive": False,
        },
        {
            "ticker": "PLTR",
            "name": "Palantir",
            "value": "$24.5",
            "change": "+2.1%",
            "is_positive": True,
        },
    ]
    top_movers_volume: list[TopMover] = [
        {
            "ticker": "TSLA",
            "name": "Tesla",
            "value": "98M",
            "change": "+15%",
            "is_positive": True,
        },
        {
            "ticker": "AAPL",
            "name": "Apple",
            "value": "54M",
            "change": "-5%",
            "is_positive": False,
        },
        {
            "ticker": "AMD",
            "name": "AMD",
            "value": "45M",
            "change": "+25%",
            "is_positive": True,
        },
        {
            "ticker": "F",
            "name": "Ford",
            "value": "32M",
            "change": "+2%",
            "is_positive": True,
        },
    ]
    notifications: list[NotificationItem] = [
        {
            "id": 1,
            "header": "Begin Covering",
            "ticker": "AAPL",
            "timestamp": "09:30 AM",
            "instruction": "Action required before market open",
            "type": "alert",
            "read": False,
        },
        {
            "id": 2,
            "header": "Manual Booking",
            "ticker": "MSFT",
            "timestamp": "10:15 AM",
            "instruction": "Verify trade settlement details",
            "type": "info",
            "read": False,
        },
        {
            "id": 3,
            "header": "Risk Alert",
            "ticker": "TSLA",
            "timestamp": "11:00 AM",
            "instruction": "Delta exposure exceeds threshold",
            "type": "warning",
            "read": False,
        },
        {
            "id": 4,
            "header": "Corporate Action",
            "ticker": "GOOGL",
            "timestamp": "12:45 PM",
            "instruction": "Stock split adjustments pending",
            "type": "info",
            "read": True,
        },
        {
            "id": 5,
            "header": "Settlement Fail",
            "ticker": "AMZN",
            "timestamp": "02:20 PM",
            "instruction": "Contact counterparty immediately",
            "type": "alert",
            "read": False,
        },
    ]
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
            "Bond Position",
            "Trade Summary",
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
            "Inventory Recon",
            "Settlement Recon",
            "Failed Trades",
            "PnL Recon",
            "PnL Record Recon",
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
            "Short-Sell Hedge",
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
        "Orders": ["EMSX Order/Route"],
    }

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
    def set_subtab(self, subtab_name: str):
        """Sets the active subtab for the CURRENT module."""
        self._active_subtabs[self.active_module] = subtab_name

    @rx.var
    def current_search_query(self) -> str:
        return self._filters.get(self.active_module, {}).get("search", "")

    @rx.var
    def current_date_filter(self) -> str:
        return self._filters.get(self.active_module, {}).get("date", "")

    @rx.var
    def current_auto_refresh(self) -> bool:
        return self._filters.get(self.active_module, {}).get("auto_refresh", False)

    @rx.event
    def set_current_search(self, value: str):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["search"] = value
        self.current_page = 1

    @rx.event
    def set_current_date(self, value: str):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["date"] = value

    @rx.event
    def toggle_auto_refresh(self, value: bool):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["auto_refresh"] = value

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_top_movers(self):
        self.show_top_movers = not self.show_top_movers

    @rx.var
    def unread_count(self) -> int:
        return len([n for n in self.notifications if not n.get("read", False)])

    @rx.event
    def add_simulated_notification(self):
        import random
        from datetime import datetime

        types = ["alert", "warning", "info"]
        tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "AMD"]
        msgs = [
            "Price Target Reached",
            "Volume Spike Detected",
            "News Alert Released",
            "Analyst Rating Change",
            "Unusual Options Activity",
        ]
        new_note: NotificationItem = {
            "id": len(self.notifications) + random.randint(100, 999),
            "header": random.choice(msgs),
            "ticker": random.choice(tickers),
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "instruction": "Check details immediately",
            "type": random.choice(types),
            "read": False,
        }
        self.notifications.insert(0, new_note)
        if len(self.notifications) > 20:
            self.notifications = self.notifications[:20]

    @rx.event
    def dismiss_notification(self, id: int):
        """Removes a notification by ID."""
        self.notifications = [n for n in self.notifications if n["id"] != id]

    @rx.event
    def handle_generate(self, page_name: str):
        """Handle the generate action."""
        yield rx.toast(f"Generating report for {page_name}...", duration=2000)

    @rx.event
    async def refresh_prices(self):
        """Simulates refreshing market data for all PnL views."""
        self.is_loading = True
        yield
        try:
            self.pnl_change_data = _generate_pnl_change_data()
            self.pnl_summary_data = _generate_pnl_summary_data()
            self.pnl_currency_data = _generate_pnl_currency_data()
            yield rx.toast("Market data refreshed", position="bottom-right")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing portfolio dashboard prices: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def set_selected_row(self, row_id: int):
        self.selected_row_id = row_id

    current_page: int = 1
    page_size: int = 50
    page_size_options: list[int] = [25, 50, 100]
    _all_table_data: list[dict] = _generate_mock_data()
    pnl_change_data: list[PnLChangeItem] = _generate_pnl_change_data()
    pnl_summary_data: list[PnLSummaryItem] = _generate_pnl_summary_data()
    pnl_currency_data: list[PnLCurrencyItem] = _generate_pnl_currency_data()

    @rx.var(cache=True)
    def filtered_pnl_change(self) -> list[PnLChangeItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pnl_change_data
        return [
            item
            for item in self.pnl_change_data
            if query in item["ticker"].lower() or query in item["underlying"].lower()
        ]

    @rx.var(cache=True)
    def filtered_pnl_summary(self) -> list[PnLSummaryItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pnl_summary_data
        return [
            item
            for item in self.pnl_summary_data
            if query in item["underlying"].lower() or query in item["currency"].lower()
        ]

    @rx.var(cache=True)
    def filtered_pnl_currency(self) -> list[PnLCurrencyItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pnl_currency_data
        return [
            item for item in self.pnl_currency_data if query in item["currency"].lower()
        ]

    @rx.var
    def total_items(self) -> int:
        return len(self.filtered_table_data)

    @rx.var
    def total_pages(self) -> int:
        if self.total_items == 0:
            return 1
        return (self.total_items + self.page_size - 1) // self.page_size

    @rx.var(cache=True)
    def filtered_table_data(self) -> list[dict]:
        data = self._all_table_data
        query = self.current_search_query.lower()
        if not query:
            return data
        return [
            item
            for item in data
            if query in item["ticker"].lower() or query in item["description"].lower()
        ]

    @rx.var(cache=True)
    def paginated_table_data(self) -> list[dict]:
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_table_data[start:end]

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def set_page_size(self, size: str):
        self.page_size = int(size)
        self.current_page = 1