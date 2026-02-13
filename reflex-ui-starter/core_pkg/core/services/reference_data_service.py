"""
Reference Data Service — Core business logic for instrument reference data.

Provides mock reference/ticker data for the starter template.
"""

from typing import List


class ReferenceDataService:
    """Service for instrument reference data operations."""

    def __init__(self):
        self._reference_data: List[dict] = []
        self._initialized = False

    def get_reference_data(self) -> List[dict]:
        """Get all reference data rows."""
        if not self._initialized:
            self._generate_mock_data()
            self._initialized = True
        return self._reference_data

    def get_summary_stats(self) -> dict:
        """Get summary statistics for reference data."""
        data = self.get_reference_data()
        total = len(data)
        exchanges = len(set(d["exchange"] for d in data))
        countries = len(set(d["country"] for d in data))
        return {
            "total": total,
            "exchanges": exchanges,
            "countries": countries,
        }

    def _generate_mock_data(self):
        """Generate mock reference data."""
        self._reference_data = [
            {"ticker": "AAPL", "name": "Apple Inc.", "isin": "US0378331005", "exchange": "NASDAQ", "currency": "USD", "industry": "Technology", "country": "US", "market_cap": "$3.0T", "status": "Active"},
            {"ticker": "MSFT", "name": "Microsoft Corp.", "isin": "US5949181045", "exchange": "NASDAQ", "currency": "USD", "industry": "Technology", "country": "US", "market_cap": "$3.1T", "status": "Active"},
            {"ticker": "GOOGL", "name": "Alphabet Inc.", "isin": "US02079K3059", "exchange": "NASDAQ", "currency": "USD", "industry": "Technology", "country": "US", "market_cap": "$2.2T", "status": "Active"},
            {"ticker": "AMZN", "name": "Amazon.com Inc.", "isin": "US0231351067", "exchange": "NASDAQ", "currency": "USD", "industry": "Consumer", "country": "US", "market_cap": "$1.9T", "status": "Active"},
            {"ticker": "TSLA", "name": "Tesla Inc.", "isin": "US88160R1014", "exchange": "NASDAQ", "currency": "USD", "industry": "Automotive", "country": "US", "market_cap": "$790B", "status": "Active"},
            {"ticker": "7203.T", "name": "Toyota Motor Corp.", "isin": "JP3633400001", "exchange": "TSE", "currency": "JPY", "industry": "Automotive", "country": "JP", "market_cap": "$250B", "status": "Active"},
            {"ticker": "NESN.SW", "name": "Nestlé S.A.", "isin": "CH0038863350", "exchange": "SIX", "currency": "CHF", "industry": "Consumer", "country": "CH", "market_cap": "$280B", "status": "Active"},
            {"ticker": "HSBA.L", "name": "HSBC Holdings", "isin": "GB0005405286", "exchange": "LSE", "currency": "GBP", "industry": "Finance", "country": "GB", "market_cap": "$160B", "status": "Active"},
            {"ticker": "SAP.DE", "name": "SAP SE", "isin": "DE0007164600", "exchange": "XETRA", "currency": "EUR", "industry": "Technology", "country": "DE", "market_cap": "$230B", "status": "Active"},
            {"ticker": "BHP.AX", "name": "BHP Group Ltd", "isin": "AU000000BHP4", "exchange": "ASX", "currency": "AUD", "industry": "Mining", "country": "AU", "market_cap": "$140B", "status": "Active"},
            {"ticker": "005930.KS", "name": "Samsung Electronics", "isin": "KR7005930003", "exchange": "KRX", "currency": "KRW", "industry": "Technology", "country": "KR", "market_cap": "$350B", "status": "Active"},
            {"ticker": "RY.TO", "name": "Royal Bank of Canada", "isin": "CA7800871021", "exchange": "TSX", "currency": "CAD", "industry": "Finance", "country": "CA", "market_cap": "$170B", "status": "Active"},
        ]
