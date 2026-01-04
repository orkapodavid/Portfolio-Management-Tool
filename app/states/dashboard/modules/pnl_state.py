import random
from datetime import datetime
import reflex as rx
from app.adapters.reporting_adapter import ReportingAdapter
from app.states.dashboard.portfolio_dashboard_types import (
    PnLChangeItem,
    PnLSummaryItem,
    PnLCurrencyItem,
)


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
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "underlying": f"{ticker} US Equity",
                "ticker": ticker,
                "pnl_ytd": _fmt_usd(base_pnl),
                "pnl_chg_1d": _fmt_usd(chg_1d),
                "pnl_chg_1w": _fmt_usd(chg_1d * 3.5),
                "pnl_chg_1m": _fmt_usd(chg_1d * 12.0),
                "pnl_chg_pct_1d": _fmt_pct(random.uniform(-3, 3)),
                "pnl_chg_pct_1w": _fmt_pct(random.uniform(-8, 8)),
                "pnl_chg_pct_1m": _fmt_pct(random.uniform(-15, 15)),
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
                "pos_c_truncated": _fmt_usd(random.uniform(-500, 500)),
            }
        )
    return data


from .positions_state import PositionsState


class PnLState(PositionsState):
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

    @rx.event
    async def load_pnl_data(self):
        """Fetch PnL related data via ReportingAdapter."""
        pnl_change = await ReportingAdapter.get_pnl_change()
        if pnl_change:
            self.pnl_change_data = pnl_change
        pnl_summary = await ReportingAdapter.get_pnl_summary()
        if pnl_summary:
            self.pnl_summary_data = pnl_summary
        pnl_currency = await ReportingAdapter.get_pnl_currency()
        if pnl_currency:
            self.pnl_currency_data = pnl_currency