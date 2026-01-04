import random
from datetime import datetime
import reflex as rx
from app.adapters.portfolio_adapter import PortfolioAdapter
from app.states.dashboard.portfolio_dashboard_types import (
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
    TradeSummaryItem,
)


def _fmt_usd(val: float) -> str:
    return f"${val:,.2f}" if val >= 0 else f"$({abs(val):,.2f})"


def _generate_positions_data() -> list[PositionItem]:
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "BTC-USD", "EURUSD", "US10Y"]
    companies = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corp.",
        "GOOGL": "Alphabet Inc.",
        "TSLA": "Tesla Inc.",
        "NVDA": "NVIDIA Corp.",
        "BTC-USD": "Bitcoin",
        "EURUSD": "Euro/USD",
        "US10Y": "US Treasury 10Y",
    }
    data = []
    for i, t in enumerate(tickers):
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "underlying": f"{t} US",
                "ticker": t,
                "company_name": companies.get(t, t),
                "account_id": f"ACC-{random.randint(10, 99)}",
                "pos_loc": random.choice(["NY", "LN", "HK"]),
            }
        )
    return data


def _generate_stock_positions() -> list[StockPositionItem]:
    tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "NFLX"]
    companies = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corp.",
        "AMZN": "Amazon.com",
        "GOOGL": "Alphabet Inc.",
        "META": "Meta Platforms",
        "NVDA": "NVIDIA Corp.",
        "NFLX": "Netflix Inc.",
    }
    data = []
    for i, t in enumerate(tickers):
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "ticker": t,
                "company_name": companies.get(t, t),
                "sec_id": f"US{random.randint(100000000, 999999999)}",
                "sec_type": "Common Stock",
                "currency": "USD",
                "account_id": f"ACC-{random.randint(10, 99)}",
                "position_location": random.choice(["NY", "LN", "HK"]),
                "notional": _fmt_usd(random.uniform(100000, 5000000)),
            }
        )
    return data


def _generate_warrant_positions() -> list[WarrantPositionItem]:
    underlyings = ["AAPL", "TSLA", "NVDA", "AMZN"]
    data = []
    for i in range(10):
        und = random.choice(underlyings)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "underlying": und,
                "ticker": f"{und}-W",
                "company_name": f"{und} Warrant",
                "sec_id": f"W{random.randint(100000, 999999)}",
                "sec_type": "Warrant",
                "subtype": random.choice(["Call", "Put"]),
                "currency": "USD",
                "account_id": f"ACC-{random.randint(10, 99)}",
            }
        )
    return data


def _generate_bond_positions() -> list[BondPositionItem]:
    issuers = ["US GOVT", "APPLE INC", "MICROSOFT", "GOLDMAN SACHS", "JPM"]
    data = []
    for i, issuer in enumerate(issuers):
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "underlying": issuer,
                "ticker": f"{issuer[:4]} 4.5%",
                "company_name": issuer,
                "sec_id": f"US{random.randint(100000000, 999999999)}",
                "sec_type": "Corp Bond",
                "subtype": "Fixed",
                "currency": "USD",
                "account_id": f"ACC-{random.randint(10, 99)}",
            }
        )
    return data


def _generate_trade_summaries() -> list[TradeSummaryItem]:
    tickers = ["AAPL", "MSFT", "TSLA", "EURUSD", "US10Y"]
    data = []
    for i in range(15):
        ticker = random.choice(tickers)
        data.append(
            {
                "id": i,
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "ticker": ticker,
                "underlying": f"{ticker} US",
                "account_id": f"ACC-{random.randint(10, 99)}",
                "company_name": f"{ticker} Inc",
                "sec_id": f"US{random.randint(100000000, 999999999)}",
                "sec_type": "Equity",
                "subtype": "Common",
                "currency": "USD",
                "closing_date": "2024-12-31",
                "divisor": f"{random.uniform(0.1, 1.0):.4f}",
            }
        )
    return data


class PositionsState(rx.State):
    _filters: dict[str, dict] = {}
    active_module: str = "Market Data"

    @rx.var
    def current_search_query(self) -> str:
        return self._filters.get(self.active_module, {}).get("search", "")

    positions_data: list[PositionItem] = _generate_positions_data()
    stock_positions: list[StockPositionItem] = _generate_stock_positions()
    warrant_positions: list[WarrantPositionItem] = _generate_warrant_positions()
    bond_positions: list[BondPositionItem] = _generate_bond_positions()
    trade_summaries: list[TradeSummaryItem] = _generate_trade_summaries()

    @rx.var(cache=True)
    def filtered_positions(self) -> list[PositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.positions_data
        return [p for p in self.positions_data if query in p["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_stock_positions(self) -> list[StockPositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.stock_positions
        return [
            p
            for p in self.stock_positions
            if query in p["ticker"].lower() or query in p["company_name"].lower()
        ]

    @rx.var(cache=True)
    def filtered_warrant_positions(self) -> list[WarrantPositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.warrant_positions
        return [
            p
            for p in self.warrant_positions
            if query in p["ticker"].lower() or query in p["underlying"].lower()
        ]

    @rx.var(cache=True)
    def filtered_bond_positions(self) -> list[BondPositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.bond_positions
        return [p for p in self.bond_positions if query in p["underlying"].lower()]

    @rx.var(cache=True)
    def filtered_trade_summaries(self) -> list[TradeSummaryItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.trade_summaries
        return [p for p in self.trade_summaries if query in p["ticker"].lower()]

    @rx.event
    async def load_positions_data(self):
        """Fetch Positions related data via PortfolioAdapter."""
        positions = await PortfolioAdapter.get_positions()
        if positions:
            self.positions_data = positions
        stock_pos = await PortfolioAdapter.get_stock_positions()
        if stock_pos:
            self.stock_positions = stock_pos
        warrant_pos = await PortfolioAdapter.get_warrant_positions()
        if warrant_pos:
            self.warrant_positions = warrant_pos
        bond_pos = await PortfolioAdapter.get_bond_positions()
        if bond_pos:
            self.bond_positions = bond_pos
        trade_sums = await PortfolioAdapter.get_trade_summaries()
        if trade_sums:
            self.trade_summaries = trade_sums