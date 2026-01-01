import random
from datetime import datetime
from ..models.dtos import (
    PositionDTO,
    PnLDTO,
    StockPositionDTO,
    WarrantPositionDTO,
    BondPositionDTO,
    TradeSummaryDTO,
    PnLSummaryDTO,
    PnLCurrencyDTO,
    RestrictedListDTO,
    ReconDTO,
    RiskInputDTO,
)


def get_portfolio_positions(date: str = None) -> list[PositionDTO]:
    """Mock service to get positions."""
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


def get_stock_positions() -> list[StockPositionDTO]:
    """Mock service to get stock positions."""
    tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "NFLX"]
    data = []
    for i, t in enumerate(tickers):
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "ticker": t,
                "company_name": f"{t} Inc",
                "sec_id": f"US{random.randint(100000000, 999999999)}",
                "sec_type": "Common Stock",
                "currency": "USD",
                "account_id": f"ACC-{random.randint(10, 99)}",
                "position_location": random.choice(["NY", "LN", "HK"]),
                "notional": random.uniform(100000, 5000000),
            }
        )
    return data


def get_warrant_positions() -> list[WarrantPositionDTO]:
    """Mock service to get warrant positions."""
    data = []
    for i in range(10):
        und = random.choice(["AAPL", "TSLA", "NVDA"])
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


def get_bond_positions() -> list[BondPositionDTO]:
    """Mock service to get bond positions."""
    data = []
    for i in range(10):
        issuer = random.choice(["US GOVT", "APPLE INC", "MICROSOFT"])
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


def get_trade_summaries() -> list[TradeSummaryDTO]:
    """Mock service to get trade summaries."""
    data = []
    for i in range(10):
        data.append(
            {
                "id": i,
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "ticker": f"TKR{i}",
                "underlying": f"UND{i}",
                "account_id": f"ACC-{random.randint(10, 99)}",
                "company_name": f"Company {i}",
                "sec_id": f"S{i}",
                "sec_type": "Equity",
                "subtype": "Common",
                "currency": "USD",
                "closing_date": "2024-12-31",
                "divisor": random.uniform(0.1, 1.0),
            }
        )
    return data


def get_pnl_change(start_date: str = None, end_date: str = None) -> list[PnLDTO]:
    """Mock service to get PnL change."""
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
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
                "pnl_ytd": base_pnl,
                "pnl_chg_1d": chg_1d,
                "pnl_chg_1w": chg_1d * 3.5,
                "pnl_chg_1m": chg_1d * 12.0,
                "pnl_chg_pct_1d": random.uniform(-3, 3),
                "pnl_chg_pct_1w": random.uniform(-8, 8),
                "pnl_chg_pct_1m": random.uniform(-15, 15),
            }
        )
    return data


def get_pnl_summary(
    start_date: str = None, end_date: str = None
) -> list[PnLSummaryDTO]:
    """Mock service to get PnL summary."""
    tickers = ["AAPL", "MSFT", "GOOGL"]
    data = []
    for i, ticker in enumerate(tickers):
        price = random.uniform(100, 1000)
        price_t1 = price * random.uniform(0.95, 1.05)
        fx = random.uniform(0.8, 1.5)
        fx_t1 = fx * random.uniform(0.99, 1.01)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "underlying": f"{ticker} US Equity",
                "currency": "USD",
                "price": price,
                "price_t_1": price_t1,
                "price_change": price - price_t1,
                "fx_rate": fx,
                "fx_rate_t_1": fx_t1,
                "fx_rate_change": fx - fx_t1,
                "dtl": random.uniform(0, 1000),
                "last_volume": random.randint(100000, 5000000),
                "adv_3m": random.randint(100000, 5000000),
            }
        )
    return data


def get_pnl_currency() -> list[PnLCurrencyDTO]:
    """Mock service to get PnL currency."""
    currencies = ["USD", "EUR", "GBP", "JPY"]
    data = []
    for i, ccy in enumerate(currencies):
        fx = random.uniform(0.5, 1.5)
        fx_t1 = fx * random.uniform(0.98, 1.02)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "currency": ccy,
                "fx_rate": fx,
                "fx_rate_t_1": fx_t1,
                "fx_rate_change": fx - fx_t1,
                "ccy_exposure": random.uniform(-1000000, 1000000),
                "usd_exposure": random.uniform(-1000000, 1000000),
                "pos_ccy_expo": random.uniform(-500000, 500000),
                "ccy_hedged_pnl": random.uniform(-10000, 10000),
                "pos_ccy_pnl": random.uniform(-20000, 20000),
                "net_ccy": random.uniform(-5000, 5000),
                "pos_c_truncated": random.uniform(-500, 500),
            }
        )
    return data


def get_restricted_list() -> list[RestrictedListDTO]:
    """Mock service to get restricted list."""
    data = []
    for i in range(10):
        data.append(
            {
                "id": i,
                "ticker": f"TKR{i}",
                "company_name": f"Company {i}",
                "in_emdx": random.choice([True, False]),
                "compliance_type": "Watch",
                "firm_block": False,
                "compliance_start": "2024-01-01",
                "nda_end": "2024-12-31",
                "mnpi_end": "",
                "wc_end": "",
            }
        )
    return data


def get_reconciliation_report(recon_type: str) -> list[ReconDTO]:
    """Mock service for reconciliation reports."""
    data = []
    for i in range(10):
        data.append(
            {
                "id": i,
                "trade_date": "2024-03-20",
                "report_date": "2024-03-20",
                "deal_num": f"D{i}",
                "row_index": str(i),
                "underlying": f"UND{i}",
                "pos_loc": "NY",
                "stock_sec_id": f"S{i}",
                "warrant_sec_id": f"W{i}",
                "bond_sec_id": f"B{i}",
                "stock_position": 1000.0,
            }
        )
    return data


def get_risk_inputs() -> list[RiskInputDTO]:
    """Mock service for risk inputs."""
    data = []
    for i in range(10):
        data.append(
            {
                "id": i,
                "value_date": "2024-03-20",
                "underlying": f"UND{i}",
                "ticker": f"TKR{i}",
                "sec_type": "Equity",
                "spot_mc": 100.0,
                "spot_ppd": 100.1,
                "position": 500.0,
                "value_mc": 50000.0,
                "value_ppd": 50050.0,
            }
        )
    return data