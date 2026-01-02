import reflex as rx
from typing import TypedDict, Optional
import datetime
import asyncio
import logging
from app.states.dashboard.dashboard_state import Holding
from app.adapters.portfolio_adapter import PortfolioAdapter


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
            "id": "local_1",
            "name": "Standard Trading",
            "description": "Local Account",
            "holdings": [
                {
                    "symbol": "AAPL",
                    "name": "Apple Inc.",
                    "shares": 100.0,
                    "avg_cost": 150.0,
                    "current_price": 182.5,
                    "daily_change_pct": 1.2,
                    "asset_class": "Equity",
                }
            ],
            "transactions": [],
            "dividends": [],
            "cash": 10000.0,
        }
    ]
    selected_portfolio_index: int = 0
    is_add_portfolio_open: bool = False
    is_add_transaction_open: bool = False
    transaction_type: str = "Buy"
    is_loading: bool = False

    @rx.event
    async def load_portfolio_data(self):
        """Fetches and adapts portfolio data from backend services via PortfolioAdapter."""
        self.is_loading = True
        yield
        try:
            from app.adapters.portfolio_adapter import PortfolioAdapter
            from app.config import PMT_INTEGRATION_MODE

            stock_pos = await PortfolioAdapter.get_stock_positions()
            if stock_pos:
                new_holdings: list[Holding] = []
                for p in stock_pos:
                    raw_notional = str(p.get("notional", "$0"))
                    notional_clean = (
                        raw_notional.replace("$", "")
                        .replace(",", "")
                        .replace("(", "-")
                        .replace(")", "")
                    )
                    try:
                        notional_val = float(notional_clean)
                    except (ValueError, TypeError) as e:
                        logging.exception(
                            f"Error parsing notional value '{notional_clean}': {e}"
                        )
                        notional_val = 0.0
                    base_price = 150.0
                    shares = (
                        round(abs(notional_val) / base_price, 2)
                        if notional_val != 0
                        else 100.0
                    )
                    holding: Holding = {
                        "symbol": str(p.get("ticker", "")).upper(),
                        "name": str(p.get("company_name", ""))
                        or str(p.get("ticker", "")),
                        "shares": float(shares),
                        "avg_cost": float(base_price * 0.98),
                        "current_price": float(base_price),
                        "daily_change_pct": 0.0,
                        "asset_class": str(p.get("sec_type", "Equity")),
                    }
                    new_holdings.append(holding)
                updated_portfolios = self.portfolios.copy()
                feed_id = "pmt_feed"
                feed_index = -1
                for i, p in enumerate(updated_portfolios):
                    if p["id"] == feed_id:
                        feed_index = i
                        break
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                feed_description = (
                    f"Live institutional feed via {PMT_INTEGRATION_MODE} at {timestamp}"
                )
                if feed_index != -1:
                    updated_portfolios[feed_index]["holdings"] = new_holdings
                    updated_portfolios[feed_index]["description"] = feed_description
                else:
                    updated_portfolios.insert(
                        0,
                        {
                            "id": feed_id,
                            "name": "Institutional Feed",
                            "description": feed_description,
                            "holdings": new_holdings,
                            "transactions": [],
                            "dividends": [],
                            "cash": 0.0,
                        },
                    )
                self.portfolios = updated_portfolios
                if feed_index == -1:
                    self.selected_portfolio_index = 0
                yield rx.toast(
                    f"Synced {len(new_holdings)} positions from {PMT_INTEGRATION_MODE}",
                    position="bottom-right",
                )
            else:
                yield rx.toast(
                    "No remote positions returned from feed.", position="bottom-right"
                )
        except Exception as e:
            logging.exception(f"Portfolio state integration error: {e}")
            yield rx.toast(
                f"Connection failed: Check {PMT_INTEGRATION_MODE} integration settings.",
                position="bottom-right",
            )
        finally:
            self.is_loading = False

    @rx.var
    def selected_portfolio(self) -> Portfolio:
        if 0 <= self.selected_portfolio_index < len(self.portfolios):
            return self.portfolios[self.selected_portfolio_index]
        return {
            "id": "0",
            "name": "No Portfolio",
            "description": "",
            "holdings": [],
            "transactions": [],
            "dividends": [],
            "cash": 0.0,
        }

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