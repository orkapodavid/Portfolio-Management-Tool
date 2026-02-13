"""
Analytics Service — Core business logic for analytics/market data.

Provides mock market data for the starter template.
Replace with real data source in production.
"""

from typing import List, Optional


class AnalyticsService:
    """Service for analytics and market data operations."""

    def __init__(self):
        self._market_data: List[dict] = []
        self._initialized = False

    def get_market_data(self) -> List[dict]:
        """Get all market data rows."""
        if not self._initialized:
            self._generate_mock_data()
            self._initialized = True
        return self._market_data

    def get_summary_stats(self) -> dict:
        """Get summary statistics for market data."""
        data = self.get_market_data()
        total = len(data)
        gainers = len([d for d in data if d["change"] > 0])
        losers = len([d for d in data if d["change"] < 0])
        avg_change = sum(d["change"] for d in data) / total if total else 0
        return {
            "total": total,
            "gainers": gainers,
            "losers": losers,
            "avg_change": round(avg_change, 2),
        }

    def get_column_defs(self) -> List[dict]:
        """Get AG Grid column definitions for market data."""
        return [
            {"field": "ticker", "headerName": "Ticker", "width": 100, "pinned": "left"},
            {"field": "company", "headerName": "Company", "flex": 1, "minWidth": 150},
            {"field": "sector", "headerName": "Sector", "width": 120},
            {"field": "price", "headerName": "Price", "width": 100, "type": "numericColumn"},
            {"field": "change", "headerName": "Change %", "width": 100, "type": "numericColumn"},
            {"field": "volume", "headerName": "Volume", "width": 120, "type": "numericColumn"},
            {"field": "marketCap", "headerName": "Market Cap", "width": 130},
        ]

    def _generate_mock_data(self):
        """Generate mock market data."""
        self._market_data = [
            {"ticker": "AAPL", "company": "Apple Inc.", "sector": "Technology", "price": 195.20, "change": 2.3, "volume": 52_340_000, "marketCap": "$3.0T"},
            {"ticker": "MSFT", "company": "Microsoft Corp.", "sector": "Technology", "price": 420.10, "change": 1.8, "volume": 28_120_000, "marketCap": "$3.1T"},
            {"ticker": "GOOGL", "company": "Alphabet Inc.", "sector": "Technology", "price": 175.50, "change": -0.5, "volume": 18_450_000, "marketCap": "$2.2T"},
            {"ticker": "AMZN", "company": "Amazon.com Inc.", "sector": "Consumer", "price": 185.60, "change": 1.2, "volume": 35_670_000, "marketCap": "$1.9T"},
            {"ticker": "TSLA", "company": "Tesla Inc.", "sector": "Automotive", "price": 248.30, "change": 4.1, "volume": 98_230_000, "marketCap": "$790B"},
            {"ticker": "NVDA", "company": "NVIDIA Corp.", "sector": "Technology", "price": 880.20, "change": 3.2, "volume": 42_180_000, "marketCap": "$2.2T"},
            {"ticker": "META", "company": "Meta Platforms", "sector": "Technology", "price": 510.40, "change": -1.2, "volume": 15_890_000, "marketCap": "$1.3T"},
            {"ticker": "JPM", "company": "JPMorgan Chase", "sector": "Finance", "price": 198.50, "change": 0.7, "volume": 8_340_000, "marketCap": "$571B"},
            {"ticker": "V", "company": "Visa Inc.", "sector": "Finance", "price": 280.90, "change": 0.3, "volume": 6_120_000, "marketCap": "$577B"},
            {"ticker": "JNJ", "company": "Johnson & Johnson", "sector": "Healthcare", "price": 162.30, "change": -0.8, "volume": 5_670_000, "marketCap": "$391B"},
        ]
