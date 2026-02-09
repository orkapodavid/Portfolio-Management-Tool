"""
Market Data Service for Portfolio Management Tool.

This service handles market data fetching from various sources including:
- Yahoo Finance (for real-time data during development)
- Bloomberg (via PyQt Bloomberg connector) - TODO for production
- Database (cached market data)
"""

import asyncio
import logging
import threading
from typing import Optional
from datetime import datetime, timedelta
import yfinance as yf
from cachetools import TTLCache
from cachetools.keys import hashkey

from app.services.shared.database_service import DatabaseService
from app.ag_grid_constants import GridId
from app.services.notifications.notification_registry import NotificationRegistry
from app.services.notifications.notification_constants import (
    NotificationCategory,
    NotificationIcon,
    NotificationColor,
)

logger = logging.getLogger(__name__)


# === NOTIFICATION PROVIDERS ===
def _get_market_data_notifications() -> list[dict]:
    """Mock market data notifications for price alerts, trade executions, etc."""
    return [
        {
            "id": "mkt-001",
            "category": NotificationCategory.ALERTS,
            "title": "Price Alert Triggered",
            "message": "TSLA has crossed above $200.00",
            "time_ago": "2 mins ago",
            "is_read": False,
            "icon": NotificationIcon.BELL,
            "color": NotificationColor.AMBER,
            "module": "Market Data",
            "subtab": "Market Data",
            "row_id": "TSLA",
            "grid_id": GridId.MARKET_DATA,
            "ticker": "TSLA",
        },
        {
            "id": "mkt-002",
            "category": NotificationCategory.PORTFOLIO,
            "title": "Trade Executed",
            "message": "Your order to buy 100 shares of AAPL has been filled at $189.50",
            "time_ago": "1 hour ago",
            "is_read": False,
            "icon": NotificationIcon.WALLET,
            "color": NotificationColor.EMERALD,
            "module": "Market Data",
            "subtab": "Market Data",
            "row_id": "AAPL",
            "grid_id": GridId.MARKET_DATA,
            "ticker": "AAPL",
        },
        {
            "id": "mkt-003",
            "category": NotificationCategory.NEWS,
            "title": "Market Update",
            "message": "S&P 500 reaches new all-time high amid strong earnings reports",
            "time_ago": "3 hours ago",
            "is_read": True,
            "icon": NotificationIcon.NEWSPAPER,
            "color": NotificationColor.BLUE,
            "module": "Market Data",
            "subtab": "Market Data",
            "row_id": "MSFT",
            "grid_id": GridId.MARKET_DATA,
            "ticker": "MSFT",
        },
        {
            "id": "mkt-004",
            "category": NotificationCategory.ALERTS,
            "title": "Volume Spike",
            "message": "NVDA trading volume 3x average",
            "time_ago": "15 mins ago",
            "is_read": False,
            "icon": NotificationIcon.TRENDING_UP,
            "color": NotificationColor.ORANGE,
            "module": "Market Data",
            "subtab": "Market Data",
            "row_id": "NVDA",
            "grid_id": GridId.MARKET_DATA,
            "ticker": "NVDA",
        },
        {
            "id": "mkt-005",
            "category": NotificationCategory.ALERTS,
            "title": "52-Week High",
            "message": "GOOGL hit new 52-week high at $142.50",
            "time_ago": "30 mins ago",
            "is_read": False,
            "icon": NotificationIcon.ARROW_UP_CIRCLE,
            "color": NotificationColor.GREEN,
            "module": "Market Data",
            "subtab": "Market Data",
            "row_id": "GOOGL",
            "grid_id": GridId.MARKET_DATA,
            "ticker": "GOOGL",
        },
    ]


def _get_fx_notifications() -> list[dict]:
    """Mock FX notifications for currency rate alerts."""
    return [
        {
            "id": "fx-001",
            "category": NotificationCategory.NEWS,
            "title": "FX Update",
            "message": "USD/JPY crossed 150 level",
            "time_ago": "20 mins ago",
            "is_read": False,
            "icon": NotificationIcon.GLOBE,
            "color": NotificationColor.INDIGO,
            "module": "Market Data",
            "subtab": "FX Data",
            "row_id": "USDJPY",
            "grid_id": GridId.FX_DATA,
            "ticker": "USD/JPY",
        },
    ]


# Register providers at module load
NotificationRegistry.register("market_data", _get_market_data_notifications)
NotificationRegistry.register("fx", _get_fx_notifications)


class MarketDataService:
    """
    Service for fetching real-time and historical market data.

    Currently uses Yahoo Finance for development/testing.
    Can be extended to integrate with:
    - Bloomberg Terminal (via PyQt bloomberg connector)
    - Database (for cached data)
    - Other market data providers
    """

    # Class-level TTL cache for historical data (shared across instances).
    # The service is instantiated fresh per state call, so instance-level
    # caches would be garbage-collected immediately.
    # maxsize=256 query combinations, ttl=3600s (1 hour).
    _historical_cache: TTLCache = TTLCache(maxsize=256, ttl=3600)
    _historical_cache_lock = threading.Lock()

    def __init__(self, db_service: Optional[DatabaseService] = None):
        """
        Initialize market data service.

        Args:
            db_service: Optional database service for cached data
        """
        self.db = db_service or DatabaseService()

    async def fetch_stock_data(self, symbol: str) -> dict:
        """
        Fetch real-time data for a single stock using Yahoo Finance.

        Args:
            symbol: Stock ticker symbol (e.g., 'AAPL')

        Returns:
            Dictionary with stock data including price, volume, market cap, etc.
        """
        try:
            ticker = yf.Ticker(symbol)
            info = await asyncio.to_thread(lambda: ticker.info)
            return self._extract_stock_info(symbol, info)
        except Exception as e:
            logger.exception(f"Error fetching data for {symbol}: {e}")
            return {}

    async def fetch_multiple_stocks(self, symbols: list[str]) -> dict[str, dict]:
        """
        Fetch real-time data for multiple stocks using Yahoo Finance.

        Args:
            symbols: List of stock ticker symbols

        Returns:
            Dictionary mapping symbols to their stock data
        """
        if not symbols:
            return {}

        valid_symbols = [s for s in symbols if s]
        if not valid_symbols:
            return {}

        try:

            def _fetch():
                tickers_obj = yf.Tickers(" ".join(valid_symbols))
                results = {}
                for symbol in valid_symbols:
                    try:
                        ticker = tickers_obj.tickers.get(symbol)
                        if ticker:
                            info = ticker.info
                            results[symbol] = self._extract_stock_info(symbol, info)
                    except Exception as e:
                        logger.exception(f"Failed to fetch {symbol} in batch: {e}")
                return results

            return await asyncio.to_thread(_fetch)
        except Exception as e:
            logger.exception(f"Batch fetch error: {e}")
            return {}

    async def fetch_stock_history(self, symbol: str, period: str = "1mo") -> list[dict]:
        """
        Fetch historical price data for a symbol using Yahoo Finance.

        Args:
            symbol: Stock ticker symbol
            period: Time period ('1mo', '3mo', '6mo', 'ytd', '1y', '2y', etc.)

        Returns:
            List of historical data points with date and price
        """
        try:

            def _fetch_history():
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period=period)
                data = []
                for date, row in hist.iterrows():
                    data.append(
                        {
                            "date": date.strftime("%Y-%m-%d"),
                            "price": round(row["Close"], 2),
                        }
                    )
                return data

            return await asyncio.to_thread(_fetch_history)
        except Exception as e:
            logger.exception(f"Error fetching history for {symbol}: {e}")
            return []

    async def fetch_stock_news(self, symbol: str) -> list[dict]:
        """
        Fetch news for a symbol using Yahoo Finance.

        Args:
            symbol: Stock ticker symbol

        Returns:
            List of news items
        """
        try:

            def _fetch_news():
                ticker = yf.Ticker(symbol)
                news = ticker.news
                formatted_news = []
                for item in news[:5]:
                    formatted_news.append(
                        {
                            "id": item.get("uuid", ""),
                            "headline": item.get("title", ""),
                            "source": item.get("publisher", "Yahoo Finance"),
                            "time_ago": "Today",
                            "summary": "No summary available.",
                            "url": item.get("link", "#"),
                            "sentiment": "Neutral",
                            "related_symbols": [symbol],
                        }
                    )
                return formatted_news

            return await asyncio.to_thread(_fetch_news)
        except Exception as e:
            logger.exception(f"Error fetching news for {symbol}: {e}")
            return []

    def _extract_stock_info(self, symbol: str, info: dict) -> dict:
        """
        Helper to extract relevant fields from yfinance info dict.

        Args:
            symbol: Stock ticker symbol
            info: yfinance info dictionary

        Returns:
            Normalized stock information dictionary
        """
        current_price = (
            info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
        )
        previous_close = (
            info.get("previousClose")
            or info.get("regularMarketPreviousClose")
            or current_price
        )

        change_pct = 0.0
        if previous_close and previous_close > 0:
            change_pct = (current_price - previous_close) / previous_close * 100

        return {
            "symbol": symbol,
            "name": info.get("shortName") or info.get("longName") or symbol,
            "current_price": current_price,
            "previous_close": previous_close,
            "daily_change_pct": round(change_pct, 2),
            "market_cap": self._format_market_cap(info.get("marketCap", 0)),
            "pe_ratio": round(info.get("trailingPE", 0.0) or 0.0, 2),
            "sector": info.get("sector", "Unknown"),
            "volume": self._format_volume(info.get("volume", 0)),
            "high_52": info.get("fiftyTwoWeekHigh", 0.0),
            "low_52": info.get("fiftyTwoWeekLow", 0.0),
            "description": info.get("longBusinessSummary", "No description available."),
            "eps": info.get("trailingEps", 0.0),
        }

    def _format_market_cap(self, value: float) -> str:
        """Formats market cap value to string (e.g. 2.5T, 500B)."""
        if not value:
            return "N/A"
        if value >= 1000000000000:
            return f"{value / 1000000000000:.2f}T"
        elif value >= 1000000000:
            return f"{value / 1000000000:.2f}B"
        elif value >= 1000000:
            return f"{value / 1000000:.2f}M"
        else:
            return f"{value:,.0f}"

    def _format_volume(self, value: float) -> str:
        """Formats volume value to string."""
        if not value:
            return "0"
        if value >= 1000000:
            return f"{value / 1000000:.1f}M"
        elif value >= 1000:
            return f"{value / 1000:.1f}K"
        else:
            return f"{value}"

    def _calculate_daily_change(self, current: float, previous: float) -> float:
        """Calculate daily percentage change."""
        if not previous:
            return 0.0
        return (current - previous) / previous * 100

    # Legacy methods for backward compatibility with existing mock structure
    async def get_realtime_market_data(self, tickers: list[str]) -> list[dict]:
        """
        Fetch real-time market data for given tickers.

        This is a wrapper around fetch_multiple_stocks for compatibility
        with the original method signature.

        Args:
            tickers: List of ticker symbols

        Returns:
            List of dictionaries with market data
        """
        stock_data = await self.fetch_multiple_stocks(tickers)

        # Convert to list format
        result = []
        for ticker, data in stock_data.items():
            result.append(
                {
                    "id": hash(ticker),
                    "ticker": ticker,
                    "listed_shares": "1,000,000",  # Not available from yfinance
                    "last_volume": data.get("volume", "0"),
                    "last_price": str(data.get("current_price", 0.0)),
                    "vwap_price": str(data.get("current_price", 0.0)),
                    "bid": str(data.get("current_price", 0.0) * 0.9995),
                    "ask": str(data.get("current_price", 0.0) * 1.0005),
                    "chg_1d_pct": f"{data.get('daily_change_pct', 0.0):+.2f}%",
                    "implied_vol_pct": "25.0%",  # Not available from yfinance
                    "market_status": "Open",
                    "created_by": "system",
                }
            )

        return result

    @staticmethod
    def _historical_cache_key(
        tickers: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ):
        """Build a hashable cache key from filter params.

        Lists are unhashable, so we convert tickers to a frozenset.
        """
        ticker_key = frozenset(tickers) if tickers else frozenset()
        return hashkey(ticker_key, start_date or "", end_date or "")

    async def get_historical_data(
        self,
        tickers: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[dict]:
        """
        Fetch historical market data, filtered by tickers and date range.

        Results are cached via cachetools TTLCache (256 entries, 1h TTL).
        Note: @cachedmethod doesn't support async, so we manage the cache
        manually while still leveraging TTLCache's eviction and TTL.

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
        # TODO: Replace with actual DB query once database integration is complete
        logger.info(
            f"Querying historical data — tickers={tickers}, "
            f"start_date={start_date}, end_date={end_date}"
        )

        all_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
        query_tickers = tickers if tickers else all_tickers

        base_date = datetime.now()
        # Generate 30 days of mock data to make date filtering meaningful
        num_days = 30

        result = []
        row_id = 0
        for i, tkr in enumerate(query_tickers):
            # Find the original index for consistent pricing
            orig_idx = all_tickers.index(tkr) if tkr in all_tickers else i
            for day in range(num_days):
                trade_date = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")

                # Apply date range filter at "query" level
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

    async def get_fx_rates(self, currency_pairs: list[str]) -> list[dict]:
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

    async def subscribe_to_tickers(self, tickers: list[str]) -> bool:
        """
        Subscribe to real-time updates for tickers.

        This would typically establish a Bloomberg subscription
        or websocket connection for live data.

        Args:
            tickers: List of tickers to subscribe to

        Returns:
            bool: True if subscription successful

        TODO: Implement Bloomberg subscription logic.
        """
        logger.info(f"Mock subscription to tickers: {tickers}")
        return True

    async def get_top_movers(self, category: str = "ops") -> list[dict]:
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

    async def get_market_data(self) -> list[dict]:
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

    async def get_fx_data(self) -> list[dict]:
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

    async def get_trading_calendar(self) -> list[dict]:
        """Get trading calendar for dashboard. TODO: Replace with DB query."""
        logger.info("Returning mock trading calendar data")
        return [
            {
                "id": 1,
                "trade_date": "2026-01-11",
                "day_of_week": "Saturday",
                "usa": "Closed",
                "hkg": "Closed",
                "jpn": "Closed",
                "aus": "Closed",
                "nzl": "Closed",
                "kor": "Closed",
                "chn": "Closed",
                "twn": "Closed",
                "ind": "Closed",
            },
        ]

    async def get_market_hours(self) -> list[dict]:
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

    async def get_ticker_data(self) -> list[dict]:
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


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def test_market_data():
        service = MarketDataService()

        # Test single stock fetch
        data = await service.fetch_stock_data("AAPL")
        print(f"Single stock data: {data}")

        # Test multiple stocks
        tickers = ["AAPL", "MSFT", "GOOGL"]
        multi_data = await service.fetch_multiple_stocks(tickers)
        print(f"Multiple stocks: {multi_data}")

        # Test historical data
        history = await service.fetch_stock_history("AAPL", period="1mo")
        print(f"Historical data: {history[:3]}")

    asyncio.run(test_market_data())
