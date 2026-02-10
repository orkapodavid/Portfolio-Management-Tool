"""
Market Data Service for Portfolio Management Tool.

This service handles market data fetching from various sources including:
- Yahoo Finance (for real-time data during development)
- Bloomberg (via PyQt Bloomberg connector) - TODO for production
- Database (cached market data)

Delegates core data methods to pmt_core.services.market_data.MarketDataService.
"""

import asyncio
import logging
from typing import Optional
from datetime import datetime
import yfinance as yf

from pmt_core.services.market_data import MarketDataService as CoreMarketDataService

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
    Delegates core data methods to pmt_core MarketDataService.
    """

    def __init__(self, db_service: Optional[DatabaseService] = None):
        """
        Initialize market data service.

        Args:
            db_service: Optional database service for cached data
        """
        self.db = db_service or DatabaseService()
        self.core_service = CoreMarketDataService()

    # === Yahoo Finance integration (stays in app layer) ===

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
        """Helper to extract relevant fields from yfinance info dict."""
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

    # === Delegated to core service ===

    async def get_realtime_market_data(self, tickers: list[str]) -> list[dict]:
        """Fetch real-time market data for given tickers. Delegates to core."""
        return await self.core_service.get_realtime_market_data(tickers)

    async def get_historical_data(
        self,
        tickers: list[str] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[dict]:
        """Fetch historical market data. Delegates to core."""
        return await self.core_service.get_historical_data(tickers, start_date, end_date)

    async def get_fx_rates(self, currency_pairs: list[str]) -> list[dict]:
        """Fetch FX rates for currency pairs. Delegates to core."""
        return await self.core_service.get_fx_rates(currency_pairs)

    async def subscribe_to_tickers(self, tickers: list[str]) -> bool:
        """
        Subscribe to real-time updates for tickers.
        TODO: Implement Bloomberg subscription logic.
        """
        logger.info(f"Mock subscription to tickers: {tickers}")
        return True

    async def get_top_movers(self, category: str = "ops") -> list[dict]:
        """Get top movers data. Delegates to core."""
        return await self.core_service.get_top_movers(category)

    async def get_market_data(self) -> list[dict]:
        """Get market data. Delegates to core."""
        return await self.core_service.get_market_data()

    async def get_fx_data(self) -> list[dict]:
        """Get FX data. Delegates to core."""
        return await self.core_service.get_fx_data()

    async def get_trading_calendar(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[dict]:
        """Get trading calendar. Delegates to core."""
        return await self.core_service.get_trading_calendar(start_date, end_date)

    async def get_market_hours(self) -> list[dict]:
        """Get market hours. Delegates to core."""
        return await self.core_service.get_market_hours()

    async def get_ticker_data(self) -> list[dict]:
        """Get reference ticker data. Delegates to core."""
        return await self.core_service.get_ticker_data()
