import reflex as rx
from typing import TypedDict
import random
import datetime
import logging
from app.services import MarketDataService


class Holding(TypedDict):
    symbol: str
    name: str
    shares: float
    avg_cost: float
    current_price: float
    daily_change_pct: float
    asset_class: str


class AssetAllocation(TypedDict):
    name: str
    value: float
    fill: str


class Performer(TypedDict):
    symbol: str
    name: str
    change_pct: float
    price: float


class DashboardState(rx.State):
    holdings: list[Holding] = [
        {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "shares": 150,
            "avg_cost": 175.0,
            "current_price": 189.5,
            "daily_change_pct": 1.25,
            "asset_class": "Technology",
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corp.",
            "shares": 100,
            "avg_cost": 350.0,
            "current_price": 402.1,
            "daily_change_pct": 0.85,
            "asset_class": "Technology",
        },
        {
            "symbol": "JPM",
            "name": "JPMorgan Chase",
            "shares": 200,
            "avg_cost": 140.0,
            "current_price": 175.3,
            "daily_change_pct": -0.45,
            "asset_class": "Finance",
        },
        {
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "shares": 50,
            "avg_cost": 220.0,
            "current_price": 195.4,
            "daily_change_pct": -2.1,
            "asset_class": "Automotive",
        },
        {
            "symbol": "NVDA",
            "name": "NVIDIA Corp.",
            "shares": 40,
            "avg_cost": 450.0,
            "current_price": 785.2,
            "daily_change_pct": 3.5,
            "asset_class": "Technology",
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "shares": 120,
            "avg_cost": 130.0,
            "current_price": 145.8,
            "daily_change_pct": 0.2,
            "asset_class": "Technology",
        },
        {
            "symbol": "O",
            "name": "Realty Income",
            "shares": 300,
            "avg_cost": 55.0,
            "current_price": 52.4,
            "daily_change_pct": 0.15,
            "asset_class": "Real Estate",
        },
        {
            "symbol": "V",
            "name": "Visa Inc.",
            "shares": 80,
            "avg_cost": 240.0,
            "current_price": 278.9,
            "daily_change_pct": 0.6,
            "asset_class": "Finance",
        },
        {
            "symbol": "BTC-USD",
            "name": "Bitcoin",
            "shares": 0.5,
            "avg_cost": 45000.0,
            "current_price": 62000.0,
            "daily_change_pct": 5.2,
            "asset_class": "Crypto",
        },
        {
            "symbol": "BND",
            "name": "Vanguard Total Bond",
            "shares": 500,
            "avg_cost": 75.0,
            "current_price": 72.5,
            "daily_change_pct": -0.05,
            "asset_class": "Bonds",
        },
    ]
    selected_period: str = "1D"
    periods: list[str] = ["1D", "1W", "1M", "3M", "YTD", "1Y", "ALL"]
    is_loading: bool = False
    last_updated: str = ""

    @rx.var
    def total_value(self) -> float:
        return sum([h["shares"] * h["current_price"] for h in self.holdings])

    @rx.var
    def total_cost_basis(self) -> float:
        return sum([h["shares"] * h["avg_cost"] for h in self.holdings])

    @rx.var
    def total_gain_loss(self) -> float:
        return self.total_value - self.total_cost_basis

    @rx.var
    def total_gain_loss_pct(self) -> float:
        if self.total_cost_basis == 0:
            return 0.0
        return self.total_gain_loss / self.total_cost_basis * 100

    @rx.var
    def daily_change_value(self) -> float:
        change = sum(
            [
                h["shares"] * h["current_price"] * (h["daily_change_pct"] / 100)
                for h in self.holdings
            ]
        )
        return change

    @rx.var
    def asset_allocation_data(self) -> list[AssetAllocation]:
        allocation_map = {}
        total = self.total_value
        if total == 0:
            return []
        colors = [
            "#4F46E5",
            "#06B6D4",
            "#10B981",
            "#F59E0B",
            "#EF4444",
            "#8B5CF6",
            "#EC4899",
        ]
        for h in self.holdings:
            ac = h["asset_class"]
            val = h["shares"] * h["current_price"]
            allocation_map[ac] = allocation_map.get(ac, 0) + val
        result = []
        i = 0
        for name, value in allocation_map.items():
            result.append(
                {
                    "name": name,
                    "value": round(value, 2),
                    "fill": colors[i % len(colors)],
                }
            )
            i += 1
        return result

    @rx.var
    def top_performers(self) -> list[Holding]:
        sorted_holdings = sorted(
            self.holdings, key=lambda x: x["daily_change_pct"], reverse=True
        )
        return sorted_holdings[:3]

    @rx.var
    def bottom_performers(self) -> list[Holding]:
        sorted_holdings = sorted(self.holdings, key=lambda x: x["daily_change_pct"])
        return sorted_holdings[:3]

    @rx.event
    def set_period(self, period: str):
        self.selected_period = period

    @rx.event
    async def refresh_prices(self):
        """Refresh stock prices using MarketDataService."""
        self.is_loading = True
        yield
        try:
            symbols = [h["symbol"] for h in self.holdings]
            
            # Use MarketDataService instead of finance_service module
            market_data_service = MarketDataService()
            stock_data = await market_data_service.fetch_multiple_stocks(symbols)
            
            new_holdings = []
            for h in self.holdings:
                symbol = h["symbol"]
                if symbol in stock_data:
                    data = stock_data[symbol]
                    h["current_price"] = data["current_price"]
                    h["daily_change_pct"] = data["daily_change_pct"]
                new_holdings.append(h)
            self.holdings = new_holdings
            self.last_updated = datetime.datetime.now().strftime("%H:%M:%S")
        except Exception as e:
            logging.exception(f"Error refreshing prices: {e}")
        finally:
            self.is_loading = False
