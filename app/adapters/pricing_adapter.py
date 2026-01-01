from app.adapters.base_adapter import BaseAdapter
from app.states.dashboard.portfolio_dashboard_types import (
    MarketDataItem,
    FXDataItem,
    HistoricalDataItem,
)


class PricingAdapter(BaseAdapter):
    """Adapter for Pricing services including Market Data, FX, and History."""

    @classmethod
    async def get_market_data(cls, tickers: list[str] = None) -> list[MarketDataItem]:
        """Fetches and adapts live market data."""
        service = cls.get_service("pricing")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_market_data, tickers)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "ticker": item.get("ticker", ""),
                    "listed_shares": f"{item.get('listed_shares', 0) / 1000000:.1f}M",
                    "last_volume": f"{item.get('last_volume', 0):,.0f}",
                    "last_price": cls.fmt_num(item.get("last_price")),
                    "vwap_price": cls.fmt_num(item.get("vwap_price")),
                    "bid": cls.fmt_num(item.get("bid")),
                    "ask": cls.fmt_num(item.get("ask")),
                    "chg_1d_pct": cls.fmt_pct(item.get("chg_1d_pct")),
                    "implied_vol_pct": cls.fmt_pct(item.get("implied_vol_pct")),
                    "market_status": item.get("market_status", ""),
                    "created_by": item.get("created_by", ""),
                }
            )
        return adapted_data

    @classmethod
    async def get_fx_data(cls) -> list[FXDataItem]:
        """Fetches and adapts FX data."""
        service = cls.get_service("pricing")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_fx_data)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "ticker": item.get("ticker", ""),
                    "last_price": f"{item.get('last_price', 0):.4f}",
                    "bid": f"{item.get('bid', 0):.4f}",
                    "ask": f"{item.get('ask', 0):.4f}",
                    "created_by": item.get("created_by", ""),
                    "created_time": item.get("created_time", ""),
                    "updated_by": item.get("updated_by", ""),
                    "update": item.get("update", ""),
                }
            )
        return adapted_data

    @classmethod
    async def get_historical_data(cls) -> list[HistoricalDataItem]:
        """Fetches and adapts historical price data."""
        service = cls.get_service("pricing")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_historical_data)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "ticker": item.get("ticker", ""),
                    "vwap_price": cls.fmt_num(item.get("vwap_price")),
                    "last_price": cls.fmt_num(item.get("last_price")),
                    "last_volume": f"{item.get('last_volume', 0):,.0f}",
                    "chg_1d_pct": cls.fmt_pct(item.get("chg_1d_pct")),
                    "created_by": item.get("created_by", ""),
                    "created_time": item.get("created_time", ""),
                    "updated_by": item.get("updated_by", ""),
                    "update": item.get("update", ""),
                }
            )
        return adapted_data