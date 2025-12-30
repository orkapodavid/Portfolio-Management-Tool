import reflex as rx
from typing import TypedDict, Optional
import datetime
from app.states.dashboard_state import Holding


class Transaction(TypedDict):
    id: str
    date: str
    symbol: str
    type: str
    shares: float
    price: float
    amount: float


class Dividend(TypedDict):
    id: str
    date: str
    symbol: str
    amount: float
    yield_on_cost: float


class Portfolio(TypedDict):
    id: str
    name: str
    description: str
    holdings: list[Holding]
    transactions: list[Transaction]
    dividends: list[Dividend]
    cash: float


class PortfolioState(rx.State):
    portfolios: list[Portfolio] = [
        {
            "id": "1",
            "name": "Main Investment Account",
            "description": "Long-term growth strategy focused on tech and finance.",
            "holdings": [
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
            ],
            "transactions": [
                {
                    "id": "t1",
                    "date": "2023-12-15",
                    "symbol": "AAPL",
                    "type": "Buy",
                    "shares": 50,
                    "price": 180.0,
                    "amount": 9000.0,
                },
                {
                    "id": "t2",
                    "date": "2024-01-10",
                    "symbol": "MSFT",
                    "type": "Buy",
                    "shares": 20,
                    "price": 390.0,
                    "amount": 7800.0,
                },
            ],
            "dividends": [
                {
                    "id": "d1",
                    "date": "2024-02-15",
                    "symbol": "AAPL",
                    "amount": 36.0,
                    "yield_on_cost": 0.5,
                },
                {
                    "id": "d2",
                    "date": "2024-03-01",
                    "symbol": "JPM",
                    "amount": 210.0,
                    "yield_on_cost": 3.0,
                },
            ],
            "cash": 12500.0,
        }
    ]
    selected_portfolio_index: int = 0
    is_add_portfolio_open: bool = False
    is_add_transaction_open: bool = False
    transaction_type: str = "Buy"

    @rx.var
    def selected_portfolio(self) -> Portfolio:
        if 0 <= self.selected_portfolio_index < len(self.portfolios):
            return self.portfolios[self.selected_portfolio_index]
        return self.portfolios[0]

    @rx.var
    def sector_breakdown(self) -> list[dict]:
        data = {}
        for h in self.selected_portfolio["holdings"]:
            sector = h["asset_class"]
            value = h["shares"] * h["current_price"]
            data[sector] = data.get(sector, 0) + value
        colors = ["#6366f1", "#ec4899", "#10b981", "#f59e0b", "#8b5cf6", "#3b82f6"]
        result = []
        i = 0
        for name, value in data.items():
            result.append(
                {
                    "name": name,
                    "value": round(value, 2),
                    "fill": colors[i % len(colors)],
                }
            )
            i += 1
        return result

    @rx.event
    def set_portfolio_index(self, index: int):
        self.selected_portfolio_index = index

    @rx.event
    def toggle_add_portfolio(self):
        self.is_add_portfolio_open = not self.is_add_portfolio_open

    @rx.event
    def toggle_add_transaction(self):
        self.is_add_transaction_open = not self.is_add_transaction_open

    @rx.event
    def set_transaction_type(self, type_: str):
        self.transaction_type = type_

    @rx.event
    def add_portfolio(self, form_data: dict):
        new_portfolio: Portfolio = {
            "id": str(len(self.portfolios) + 1),
            "name": form_data.get("name", "New Portfolio"),
            "description": form_data.get("description", ""),
            "holdings": [],
            "transactions": [],
            "dividends": [],
            "cash": 0.0,
        }
        self.portfolios.append(new_portfolio)
        self.is_add_portfolio_open = False
        self.selected_portfolio_index = len(self.portfolios) - 1

    @rx.event
    def add_transaction(self, form_data: dict):
        symbol = form_data.get("symbol", "").upper()
        shares = float(form_data.get("shares", 0))
        price = float(form_data.get("price", 0))
        date = str(form_data.get("date", datetime.date.today().strftime("%Y-%m-%d")))
        t_type = self.transaction_type
        if not symbol or shares <= 0 or price < 0:
            return
        amount = shares * price
        new_tx: Transaction = {
            "id": f"tx_{len(self.selected_portfolio['transactions']) + 1}",
            "date": date,
            "symbol": symbol,
            "type": t_type,
            "shares": shares,
            "price": price,
            "amount": amount,
        }
        holdings = self.selected_portfolio["holdings"]
        found = False
        new_holdings = []
        for h in holdings:
            if h["symbol"] == symbol:
                found = True
                if t_type == "Buy":
                    total_cost = h["shares"] * h["avg_cost"] + amount
                    total_shares = h["shares"] + shares
                    h["avg_cost"] = total_cost / total_shares
                    h["shares"] = total_shares
                    new_holdings.append(h)
                elif t_type == "Sell":
                    if h["shares"] > shares:
                        h["shares"] -= shares
                        new_holdings.append(h)
                    elif h["shares"] == shares:
                        pass
                    else:
                        pass
            else:
                new_holdings.append(h)
        if not found and t_type == "Buy":
            new_holdings.append(
                {
                    "symbol": symbol,
                    "name": symbol,
                    "shares": shares,
                    "avg_cost": price,
                    "current_price": price,
                    "daily_change_pct": 0.0,
                    "asset_class": "Stock",
                }
            )
        updated_portfolio = self.selected_portfolio.copy()
        updated_portfolio["holdings"] = new_holdings
        updated_portfolio["transactions"].append(new_tx)
        self.portfolios[self.selected_portfolio_index] = updated_portfolio
        self.is_add_transaction_open = False