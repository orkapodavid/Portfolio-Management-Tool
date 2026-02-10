"""
Market Data Service — core business logic for market data.

Provides mock data for market data grids, FX rates, top movers,
trading calendar, market hours, ticker data, and historical data.
TODO: Replace mock data with actual database/repository calls.
"""

import logging
import threading
from typing import Any, Optional
from datetime import datetime, timedelta

from cachetools import TTLCache
from cachetools.keys import hashkey

logger = logging.getLogger(__name__)


class MarketDataService:
    """
    Core service for market data.

    Generates mock market data.
    Real implementation would delegate to a repository layer.
    """

    # Class-level TTL cache for historical data (shared across instances).
    _historical_cache: TTLCache = TTLCache(maxsize=256, ttl=3600)
    _historical_cache_lock = threading.Lock()

    async def get_market_data(self) -> list[dict[str, Any]]:
        """Get market data for dashboard. TODO: Replace with DB query."""
        logger.info("Returning mock market data")
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]
        return [
            {
                "id": i + 1,
                "ticker": t,
                "listed_shares": "1,000,000",
                "last_volume": "54.2M",
                "last_price": "182.50",
                "vwap_price": "182.25",
                "bid": "182.45",
                "ask": "182.55",
                "chg_1d_pct": "+0.5%",
                "implied_vol_pct": "25.0%",
                "market_status": "Open",
                "created_by": "system",
            }
            for i, t in enumerate(tickers)
        ]

    async def get_fx_data(self) -> list[dict[str, Any]]:
        """Get FX data for dashboard. TODO: Replace with DB query."""
        logger.info("Returning mock FX data")
        pairs = ["EURUSD", "GBPUSD", "USDJPY", "USDCNY", "AUDUSD"]
        return [
            {
                "id": i + 1,
                "ticker": p,
                "last_price": "1.1000",
                "bid": "1.0995",
                "ask": "1.1005",
                "created_by": "system",
                "created_time": datetime.now().isoformat(),
                "updated_by": "system",
                "update": "",
            }
            for i, p in enumerate(pairs)
        ]

    async def get_fx_rates(self, currency_pairs: list[str]) -> list[dict[str, Any]]:
        """
        Fetch FX rates for currency pairs.

        Args:
            currency_pairs: List of currency pairs (e.g., ['EURUSD', 'GBPUSD'])

        Returns:
            List of FX rate data

        TODO: Implement using Bloomberg or database.
        """
        logger.warning("Using mock FX data. Implement real integration!")

        mock_data = []
        for pair in currency_pairs:
            mock_data.append(
                {
                    "ticker": pair,
                    "last_price": "1.1000",
                    "bid": "1.0995",
                    "ask": "1.1005",
                    "created_by": "system",
                    "created_time": datetime.now().isoformat(),
                }
            )

        return mock_data

    async def get_top_movers(self, category: str = "ops") -> list[dict[str, Any]]:
        """
        Get top movers data for dashboard.

        Args:
            category: Category of top movers ('ops', 'ytd', 'delta', 'price', 'volume')

        Returns:
            List of top mover dictionaries
        """
        logger.info(f"Returning mock top movers data for category: {category}")

        movers_data = {
            "ops": [
                {
                    "ticker": "NVDA",
                    "name": "NVIDIA",
                    "value": "+$2.4M",
                    "change": "+12%",
                    "is_positive": True,
                },
                {
                    "ticker": "AAPL",
                    "name": "Apple",
                    "value": "+$1.8M",
                    "change": "+5%",
                    "is_positive": True,
                },
                {
                    "ticker": "TSLA",
                    "name": "Tesla",
                    "value": "-$1.2M",
                    "change": "-8%",
                    "is_positive": False,
                },
                {
                    "ticker": "META",
                    "name": "Meta",
                    "value": "+$950K",
                    "change": "+3%",
                    "is_positive": True,
                },
            ],
            "ytd": [
                {
                    "ticker": "NVDA",
                    "name": "NVIDIA",
                    "value": "+$45M",
                    "change": "+180%",
                    "is_positive": True,
                },
                {
                    "ticker": "META",
                    "name": "Meta",
                    "value": "+$28M",
                    "change": "+120%",
                    "is_positive": True,
                },
                {
                    "ticker": "AAPL",
                    "name": "Apple",
                    "value": "+$15M",
                    "change": "+45%",
                    "is_positive": True,
                },
                {
                    "ticker": "MSFT",
                    "name": "Microsoft",
                    "value": "+$12M",
                    "change": "+35%",
                    "is_positive": True,
                },
            ],
            "delta": [
                {
                    "ticker": "TSLA",
                    "name": "Tesla",
                    "value": "+15K",
                    "change": "+8%",
                    "is_positive": True,
                },
                {
                    "ticker": "GOOGL",
                    "name": "Google",
                    "value": "-12K",
                    "change": "-5%",
                    "is_positive": False,
                },
                {
                    "ticker": "AMZN",
                    "name": "Amazon",
                    "value": "+8K",
                    "change": "+3%",
                    "is_positive": True,
                },
                {
                    "ticker": "NFLX",
                    "name": "Netflix",
                    "value": "-5K",
                    "change": "-2%",
                    "is_positive": False,
                },
            ],
            "price": [
                {
                    "ticker": "SMCI",
                    "name": "Super Micro",
                    "value": "$985.2",
                    "change": "+25%",
                    "is_positive": True,
                },
                {
                    "ticker": "ARM",
                    "name": "ARM Holdings",
                    "value": "$142.5",
                    "change": "+18%",
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
            ],
            "volume": [
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
            ],
        }
        return movers_data.get(category, movers_data["ops"])

    async def get_trading_calendar(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get trading calendar, filtered by optional date range.

        Args:
            start_date: Start date inclusive (YYYY-MM-DD, optional)
            end_date: End date inclusive (YYYY-MM-DD, optional)

        Returns:
            List of trading calendar entries matching the filters.
        """
        logger.info(
            f"Querying trading calendar — start_date={start_date}, end_date={end_date}"
        )

        base_date = datetime.now()
        num_days = 60  # 2 months of calendar data

        # Day-of-week names
        day_names = [
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday",
        ]

        result = []
        row_id = 0
        for day in range(num_days):
            trade_dt = base_date - timedelta(days=day)
            trade_date = trade_dt.strftime("%Y-%m-%d")
            weekday = trade_dt.weekday()  # 0=Mon … 6=Sun

            # Apply date range filter at "query" level
            if start_date and trade_date < start_date:
                continue
            if end_date and trade_date > end_date:
                continue

            is_weekend = weekday >= 5
            # Simulate per-market open/closed (weekends always closed)
            status_open = "Open"
            status_closed = "Closed"

            row_id += 1
            result.append(
                {
                    "id": row_id,
                    "trade_date": trade_date,
                    "day_of_week": day_names[weekday],
                    "usa": status_closed if is_weekend else status_open,
                    "hkg": status_closed if is_weekend else status_open,
                    "jpn": status_closed if is_weekend else status_open,
                    "aus": status_closed if is_weekend else status_open,
                    "nzl": status_closed if is_weekend else status_open,
                    "kor": status_closed if is_weekend else status_open,
                    "chn": status_closed if is_weekend else status_open,
                    "twn": status_closed if is_weekend else status_open,
                    "ind": status_closed if is_weekend else status_open,
                }
            )

        logger.info(f"Trading calendar — {len(result)} rows")
        return result

    async def get_market_hours(self) -> list[dict[str, Any]]:
        """Get market hours for dashboard. TODO: Replace with DB query."""
        logger.info("Returning mock market hours data")
        return [
            {
                "id": 1,
                "market": "NYSE",
                "ticker": "SPY",
                "session": "Regular",
                "local_time": "09:30-16:00",
                "session_period": "Morning",
                "is_open": "Yes",
                "timezone": "EST",
            },
        ]

    async def get_ticker_data(self) -> list[dict[str, Any]]:
        """Get reference ticker data for dashboard. TODO: Replace with DB query."""
        logger.info("Returning mock ticker data")
        return [
            {
                "id": 1,
                "ticker": "AAPL",
                "currency": "USD",
                "fx_rate": "1.00",
                "sector": "Technology",
                "company": "Apple Inc.",
                "po_lead_manager": "GS",
                "fmat_cap": "2.95T",
                "smkt_cap": "2.95T",
                "chg_1d_pct": "+0.5%",
                "dtl": "0",
            },
        ]

    async def get_realtime_market_data(
        self, tickers: list[str]
    ) -> list[dict[str, Any]]:
        """
        Fetch real-time market data for given tickers.

        Returns mock data; real implementation would fetch from Bloomberg/DB.

        Args:
            tickers: List of ticker symbols

        Returns:
            List of dictionaries with market data
        """
        logger.info(f"Returning mock realtime market data for {tickers}")
        return [
            {
                "id": hash(t),
                "ticker": t,
                "listed_shares": "1,000,000",
                "last_volume": "54.2M",
                "last_price": "182.50",
                "vwap_price": "182.25",
                "bid": "182.45",
                "ask": "182.55",
                "chg_1d_pct": "+0.5%",
                "implied_vol_pct": "25.0%",
                "market_status": "Open",
                "created_by": "system",
            }
            for t in tickers
        ]

    @staticmethod
    def _historical_cache_key(
        tickers: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ):
        """Build a hashable cache key from filter params."""
        ticker_key = frozenset(tickers) if tickers else frozenset()
        return hashkey(ticker_key, start_date or "", end_date or "")

    async def get_historical_data(
        self,
        tickers: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch historical market data, filtered by tickers and date range.

        Results are cached via cachetools TTLCache (256 entries, 1h TTL).

        Args:
            tickers: List of ticker symbols (optional — all tickers if empty/None)
            start_date: Start date inclusive (YYYY-MM-DD, optional)
            end_date: End date inclusive (YYYY-MM-DD, optional)

        Returns:
            List of historical data points matching the filters
        """
        key = self._historical_cache_key(tickers, start_date, end_date)

        with self._historical_cache_lock:
            if key in self._historical_cache:
                logger.debug(f"Historical data cache HIT for {key}")
                return self._historical_cache[key]

        # --- Mock data generation (simulates DB query) ---
        logger.info(
            f"Querying historical data — tickers={tickers}, "
            f"start_date={start_date}, end_date={end_date}"
        )

        all_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
        query_tickers = tickers if tickers else all_tickers

        base_date = datetime.now()
        num_days = 30

        result = []
        row_id = 0
        for i, tkr in enumerate(query_tickers):
            orig_idx = all_tickers.index(tkr) if tkr in all_tickers else i
            for day in range(num_days):
                trade_date = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")

                if start_date and trade_date < start_date:
                    continue
                if end_date and trade_date > end_date:
                    continue

                row_id += 1
                result.append(
                    {
                        "id": row_id,
                        "trade_date": trade_date,
                        "ticker": tkr,
                        "vwap_price": f"{150 + orig_idx * 50 + day:.2f}",
                        "last_price": f"{151 + orig_idx * 50 + day:.2f}",
                        "last_volume": f"{(orig_idx + 1) * 1000000:,}",
                        "chg_1d_pct": f"{(-1 + orig_idx * 0.5):.2f}%",
                        "created_by": "system",
                        "created_time": datetime.now().isoformat(),
                        "updated_by": "system",
                        "update": "Active",
                    }
                )

        with self._historical_cache_lock:
            self._historical_cache[key] = result

        logger.info(f"Historical data fetched & cached — {len(result)} rows")

        return result
