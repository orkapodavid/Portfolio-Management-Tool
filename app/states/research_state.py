import reflex as rx
from typing import TypedDict
import random


class StockData(TypedDict):
    symbol: str
    name: str
    price: float
    change_pct: float
    pe_ratio: float
    market_cap: str
    volume: str
    eps: float
    high_52: float
    low_52: float
    description: str
    sector: str


class PricePoint(TypedDict):
    date: str
    price: float


class ResearchState(rx.State):
    search_query: str = ""
    selected_stock: StockData = {
        "symbol": "",
        "name": "",
        "price": 0.0,
        "change_pct": 0.0,
        "pe_ratio": 0.0,
        "market_cap": "",
        "volume": "",
        "eps": 0.0,
        "high_52": 0.0,
        "low_52": 0.0,
        "description": "",
        "sector": "",
    }
    is_modal_open: bool = False
    all_stocks: list[StockData] = [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 189.5,
            "change_pct": 1.25,
            "pe_ratio": 28.5,
            "market_cap": "2.95T",
            "volume": "54.2M",
            "eps": 6.43,
            "high_52": 199.62,
            "low_52": 124.17,
            "sector": "Technology",
            "description": "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.",
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corp.",
            "price": 402.1,
            "change_pct": 0.85,
            "pe_ratio": 36.2,
            "market_cap": "3.01T",
            "volume": "22.4M",
            "eps": 11.06,
            "high_52": 420.82,
            "low_52": 245.61,
            "sector": "Technology",
            "description": "Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide.",
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "price": 145.8,
            "change_pct": 0.2,
            "pe_ratio": 24.1,
            "market_cap": "1.79T",
            "volume": "18.9M",
            "eps": 5.8,
            "high_52": 155.2,
            "low_52": 100.28,
            "sector": "Technology",
            "description": "Alphabet Inc. offers various products and platforms in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America.",
        },
        {
            "symbol": "AMZN",
            "name": "Amazon.com Inc.",
            "price": 175.35,
            "change_pct": 0.66,
            "pe_ratio": 58.9,
            "market_cap": "1.82T",
            "volume": "35.1M",
            "eps": 2.9,
            "high_52": 180.14,
            "low_52": 96.29,
            "sector": "Consumer Cyclical",
            "description": "Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions in North America and internationally.",
        },
        {
            "symbol": "NVDA",
            "name": "NVIDIA Corp.",
            "price": 785.2,
            "change_pct": 3.5,
            "pe_ratio": 95.4,
            "market_cap": "1.94T",
            "volume": "42.1M",
            "eps": 8.4,
            "high_52": 823.94,
            "low_52": 204.21,
            "sector": "Technology",
            "description": "NVIDIA Corporation provides graphics, computing and networking solutions in the United States, Taiwan, China, and internationally.",
        },
        {
            "symbol": "JPM",
            "name": "JPMorgan Chase",
            "price": 175.3,
            "change_pct": -0.45,
            "pe_ratio": 11.2,
            "market_cap": "505.4B",
            "volume": "9.1M",
            "eps": 16.23,
            "high_52": 178.5,
            "low_52": 123.11,
            "sector": "Financial Services",
            "description": "JPMorgan Chase & Co. operates as a financial services company worldwide.",
        },
        {
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "price": 195.4,
            "change_pct": -2.1,
            "pe_ratio": 42.1,
            "market_cap": "617.5B",
            "volume": "98.5M",
            "eps": 4.3,
            "high_52": 299.29,
            "low_52": 152.37,
            "sector": "Consumer Cyclical",
            "description": "Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems.",
        },
    ]
    chart_data: list[PricePoint] = []

    @rx.var
    def filtered_stocks(self) -> list[StockData]:
        return self.all_stocks

    @rx.event
    async def set_search_query(self, query: str):
        self.search_query = query
        if len(query) > 1:
            from app.services import finance_service

            try:
                data = finance_service.fetch_stock_data(query.upper())
                if data and data.get("current_price", 0) > 0:
                    stock_data: StockData = {
                        "symbol": data["symbol"],
                        "name": data["name"],
                        "price": data["current_price"],
                        "change_pct": data["daily_change_pct"],
                        "pe_ratio": data["pe_ratio"],
                        "market_cap": str(data["market_cap"]),
                        "volume": str(data["volume"]),
                        "eps": data.get("eps", 0.0),
                        "high_52": data["high_52"],
                        "low_52": data["low_52"],
                        "description": data.get("description", ""),
                        "sector": data.get("sector", "Unknown"),
                    }
                    self.all_stocks = [stock_data]
            except Exception as e:
                import logging

                logging.exception(f"Error fetching stock data: {e}")
                pass

    @rx.event
    async def open_modal(self, stock: StockData):
        self.selected_stock = stock
        self.is_modal_open = True
        await self.generate_chart_data(stock["symbol"])

    @rx.event
    def close_modal(self):
        self.is_modal_open = False

    @rx.event
    async def generate_chart_data(self, symbol: str):
        """Generates chart data using real history."""
        from app.services import finance_service

        if not symbol:
            return
        history = finance_service.fetch_stock_history(symbol, period="1mo")
        self.chart_data = history

    @rx.event
    async def add_to_watchlist(self):
        """Adds the currently selected stock to the watchlist."""
        from app.states.watchlist_state import WatchlistState, WatchedStock

        if not self.selected_stock["symbol"]:
            return
        watchlist_state = await self.get_state(WatchlistState)
        price = self.selected_stock["price"]
        pct = self.selected_stock["change_pct"]
        prev = price / (1 + pct / 100) if 1 + pct / 100 != 0 else price
        change = price - prev
        stock_item: WatchedStock = {
            "symbol": self.selected_stock["symbol"],
            "name": self.selected_stock["name"],
            "price": self.selected_stock["price"],
            "change": change,
            "change_pct": self.selected_stock["change_pct"],
            "volume": self.selected_stock["volume"],
            "market_cap": self.selected_stock["market_cap"],
            "pe_ratio": self.selected_stock["pe_ratio"],
            "high_52": self.selected_stock["high_52"],
            "low_52": self.selected_stock["low_52"],
        }
        watchlist_state.add_to_watchlist(stock_item)