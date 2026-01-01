import random
from ..models.dtos import MarketDataDTO, FXDataDTO, HistoricalDataDTO


def get_current_prices(tickers: list[str]) -> dict[str, float]:
    """Mock service to get current prices for a list of tickers."""
    return {ticker: random.uniform(100.0, 500.0) for ticker in tickers}


def get_market_data(tickers: list[str] = None) -> list[MarketDataDTO]:
    """Mock service to get full market data."""
    if not tickers:
        tickers = [f"TKR{i}" for i in range(10)]
    data = []
    for i, ticker in enumerate(tickers):
        data.append(
            {
                "id": i,
                "ticker": ticker,
                "listed_shares": 100000000.0,
                "last_volume": 500000.0,
                "last_price": random.uniform(100, 200),
                "vwap_price": random.uniform(100, 200),
                "bid": random.uniform(100, 200),
                "ask": random.uniform(100, 200),
                "chg_1d_pct": random.uniform(-2, 2),
                "implied_vol_pct": random.uniform(10, 30),
                "market_status": "Open",
                "created_by": "MockFeed",
            }
        )
    return data


def get_fx_data() -> list[FXDataDTO]:
    """Mock service to get FX data."""
    pairs = ["USD/EUR", "USD/GBP", "USD/JPY"]
    data = []
    for i, pair in enumerate(pairs):
        data.append(
            {
                "id": i,
                "ticker": pair,
                "last_price": random.uniform(0.8, 1.5),
                "bid": random.uniform(0.8, 1.5),
                "ask": random.uniform(0.8, 1.5),
                "created_by": "System",
                "created_time": "09:00",
                "updated_by": "System",
                "update": "09:05",
            }
        )
    return data


def get_historical_data() -> list[HistoricalDataDTO]:
    """Mock service to get historical data."""
    data = []
    for i in range(10):
        data.append(
            {
                "id": i,
                "trade_date": "2024-03-19",
                "ticker": f"TKR{i}",
                "vwap_price": random.uniform(100, 200),
                "last_price": random.uniform(100, 200),
                "last_volume": random.uniform(100000, 1000000),
                "chg_1d_pct": random.uniform(-2, 2),
                "created_by": "System",
                "created_time": "17:00",
                "updated_by": "System",
                "update": "17:05",
            }
        )
    return data