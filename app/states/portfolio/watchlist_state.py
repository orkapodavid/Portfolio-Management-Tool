import reflex as rx
from typing import TypedDict
import random
import datetime


class WatchedStock(TypedDict):
    symbol: str
    name: str
    price: float
    change: float
    change_pct: float
    volume: str
    market_cap: str
    pe_ratio: float
    high_52: float
    low_52: float


class StockAlert(TypedDict):
    id: str
    symbol: str
    target_price: float
    condition: str
    active: bool
    created_at: str


class NewsItem(TypedDict):
    id: str
    headline: str
    source: str
    time_ago: str
    summary: str
    sentiment: str
    related_symbols: list[str]


class WatchlistState(rx.State):
    watchlist: list[WatchedStock] = [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 189.5,
            "change": 2.35,
            "change_pct": 1.25,
            "volume": "54.2M",
            "market_cap": "2.95T",
            "pe_ratio": 28.5,
            "high_52": 199.62,
            "low_52": 124.17,
        },
        {
            "symbol": "NVDA",
            "name": "NVIDIA Corp.",
            "price": 785.2,
            "change": 26.5,
            "change_pct": 3.5,
            "volume": "42.1M",
            "market_cap": "1.94T",
            "pe_ratio": 95.4,
            "high_52": 823.94,
            "low_52": 204.21,
        },
        {
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "price": 195.4,
            "change": -4.2,
            "change_pct": -2.1,
            "volume": "98.5M",
            "market_cap": "617.5B",
            "pe_ratio": 42.1,
            "high_52": 299.29,
            "low_52": 152.37,
        },
    ]
    alerts: list[StockAlert] = [
        {
            "id": "1",
            "symbol": "AAPL",
            "target_price": 195.0,
            "condition": "Above",
            "active": True,
            "created_at": "2024-03-10",
        },
        {
            "id": "2",
            "symbol": "TSLA",
            "target_price": 180.0,
            "condition": "Below",
            "active": True,
            "created_at": "2024-03-12",
        },
    ]
    news_feed: list[NewsItem] = [
        {
            "id": "n1",
            "headline": "Tech Sector Rallies on AI Optimism",
            "source": "Bloomberg",
            "time_ago": "2h ago",
            "summary": "Major technology stocks surged today as new AI chip announcements drove investor confidence to fresh highs.",
            "sentiment": "Positive",
            "related_symbols": ["NVDA", "MSFT", "AMD"],
        },
        {
            "id": "n2",
            "headline": "Fed Signals Potential Rate Cuts Later This Year",
            "source": "CNBC",
            "time_ago": "4h ago",
            "summary": "Federal Reserve officials hinted that inflation data is moving in the right direction, opening the door for policy easing.",
            "sentiment": "Neutral",
            "related_symbols": ["SPY", "QQQ"],
        },
        {
            "id": "n3",
            "headline": "EV Competition Heats Up as Prices Drop",
            "source": "Reuters",
            "time_ago": "5h ago",
            "summary": "Global electric vehicle manufacturers are engaging in aggressive price wars to capture market share in slowing markets.",
            "sentiment": "Negative",
            "related_symbols": ["TSLA", "RIVN"],
        },
    ]
    search_query: str = ""
    is_searching: bool = False
    available_stocks: list[WatchedStock] = [
        {
            "symbol": "MSFT",
            "name": "Microsoft Corp.",
            "price": 402.1,
            "change": 3.4,
            "change_pct": 0.85,
            "volume": "22.4M",
            "market_cap": "3.01T",
            "pe_ratio": 36.2,
            "high_52": 420.82,
            "low_52": 245.61,
        },
        {
            "symbol": "AMZN",
            "name": "Amazon.com Inc.",
            "price": 175.35,
            "change": 1.15,
            "change_pct": 0.66,
            "volume": "35.1M",
            "market_cap": "1.82T",
            "pe_ratio": 58.9,
            "high_52": 180.14,
            "low_52": 96.29,
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "price": 145.8,
            "change": 0.3,
            "change_pct": 0.21,
            "volume": "18.9M",
            "market_cap": "1.79T",
            "pe_ratio": 24.1,
            "high_52": 155.2,
            "low_52": 100.28,
        },
        {
            "symbol": "META",
            "name": "Meta Platforms",
            "price": 490.22,
            "change": -5.1,
            "change_pct": -1.03,
            "volume": "15.6M",
            "market_cap": "1.25T",
            "pe_ratio": 32.4,
            "high_52": 502.41,
            "low_52": 167.66,
        },
    ]
    is_alert_modal_open: bool = False
    alert_symbol: str = ""
    alert_target_price: float = 0.0
    alert_condition: str = "Above"

    @rx.var
    def search_results(self) -> list[WatchedStock]:
        return self.available_stocks

    @rx.event
    async def set_search_query(self, query: str):
        self.search_query = query
        self.is_searching = bool(query)
        if len(query) > 1:
            try:
                from app.services import MarketDataService

                market_data_service = MarketDataService()
                data = await market_data_service.fetch_stock_data(query.upper())
                if data and data.get("current_price", 0) > 0:
                    stock_item: WatchedStock = {
                        "symbol": data["symbol"],
                        "name": data["name"],
                        "price": data["current_price"],
                        "change": data["current_price"] - data["previous_close"],
                        "change_pct": data["daily_change_pct"],
                        "volume": str(data["volume"]),
                        "market_cap": str(data["market_cap"]),
                        "pe_ratio": data["pe_ratio"],
                        "high_52": data["high_52"],
                        "low_52": data["low_52"],
                    }
                    self.available_stocks = [stock_item]
                else:
                    self.available_stocks = []
            except Exception as e:
                import logging

                logging.exception(f"Error searching stocks: {e}")
                self.available_stocks = []
        else:
            self.available_stocks = []

    @rx.event
    def add_to_watchlist(self, stock: WatchedStock):
        if any((s["symbol"] == stock["symbol"] for s in self.watchlist)):
            yield rx.toast(
                f"{stock['symbol']} is already in your watchlist",
                position="bottom-right",
            )
            return
        self.watchlist.append(stock)
        self.search_query = ""
        self.is_searching = False
        yield rx.toast(f"Added {stock['symbol']} to watchlist", position="bottom-right")

    @rx.event
    async def refresh_watchlist(self):
        from app.services import MarketDataService

        if not self.watchlist:
            return
        yield rx.toast("Updating watchlist prices...", position="bottom-right")
        symbols = [s["symbol"] for s in self.watchlist]
        market_data_service = MarketDataService()
        results = await market_data_service.fetch_multiple_stocks(symbols)
        new_watchlist = []
        for stock in self.watchlist:
            symbol = stock["symbol"]
            if symbol in results:
                data = results[symbol]
                stock.update(
                    {
                        "price": data["current_price"],
                        "change": data["current_price"] - data["previous_close"],
                        "change_pct": data["daily_change_pct"],
                        "volume": str(data["volume"]),
                        "market_cap": str(data["market_cap"]),
                        "pe_ratio": data["pe_ratio"],
                        "high_52": data["high_52"],
                        "low_52": data["low_52"],
                    }
                )
            new_watchlist.append(stock)
        self.watchlist = new_watchlist
        yield rx.toast("Watchlist updated", position="bottom-right")

    @rx.event
    def remove_from_watchlist(self, stock: WatchedStock):
        self.watchlist = [s for s in self.watchlist if s["symbol"] != stock["symbol"]]
        yield rx.toast(
            f"Removed {stock['symbol']} from watchlist", position="bottom-right"
        )

    @rx.event
    def open_alert_modal(self, symbol: str):
        self.alert_symbol = symbol
        current_price = 0.0
        for s in self.watchlist:
            if s["symbol"] == symbol:
                current_price = s["price"]
                break
        self.alert_target_price = current_price
        self.is_alert_modal_open = True

    @rx.event
    def close_alert_modal(self):
        self.is_alert_modal_open = False

    @rx.event
    def set_alert_condition(self, condition: str):
        self.alert_condition = condition

    @rx.event
    def save_alert(self, form_data: dict):
        price = float(form_data.get("price", 0))
        if price <= 0:
            return
        new_alert: StockAlert = {
            "id": str(random.randint(1000, 9999)),
            "symbol": self.alert_symbol,
            "target_price": price,
            "condition": self.alert_condition,
            "active": True,
            "created_at": datetime.date.today().strftime("%Y-%m-%d"),
        }
        self.alerts.append(new_alert)
        self.is_alert_modal_open = False
        yield rx.toast(
            f"Alert set for {self.alert_symbol} at ${price}", position="bottom-right"
        )

    @rx.event
    def delete_alert(self, alert_id: str):
        self.alerts = [a for a in self.alerts if a["id"] != alert_id]

    @rx.event
    def toggle_alert_active(self, alert_id: str):
        self.alerts = [
            {
                "id": a["id"],
                "symbol": a["symbol"],
                "target_price": a["target_price"],
                "condition": a["condition"],
                "active": not a["active"] if a["id"] == alert_id else a["active"],
                "created_at": a["created_at"],
            }
            for a in self.alerts
        ]