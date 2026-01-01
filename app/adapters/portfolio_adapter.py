from app.adapters.base_adapter import BaseAdapter
from app.states.dashboard.portfolio_dashboard_types import (
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
    TradeSummaryItem,
)


class PortfolioAdapter(BaseAdapter):
    """Adapter for Portfolio specific data aggregation and transformation."""

    @classmethod
    async def get_positions(cls) -> list[PositionItem]:
        """Fetches and adapts standard positions data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_portfolio_positions)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "deal_num": item.get("deal_num", ""),
                    "detail_id": item.get("detail_id", ""),
                    "underlying": item.get("underlying", ""),
                    "ticker": item.get("ticker", ""),
                    "company_name": item.get("company_name", ""),
                    "account_id": item.get("account_id", ""),
                    "pos_loc": item.get("pos_loc", ""),
                }
            )
        return adapted_data

    @classmethod
    async def get_stock_positions(cls) -> list[StockPositionItem]:
        """Fetches and adapts stock positions data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_stock_positions)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "deal_num": item.get("deal_num", ""),
                    "detail_id": item.get("detail_id", ""),
                    "ticker": item.get("ticker", ""),
                    "company_name": item.get("company_name", ""),
                    "sec_id": item.get("sec_id", ""),
                    "sec_type": item.get("sec_type", ""),
                    "currency": item.get("currency", ""),
                    "account_id": item.get("account_id", ""),
                    "position_location": item.get("position_location", ""),
                    "notional": cls.fmt_usd(item.get("notional")),
                }
            )
        return adapted_data

    @classmethod
    async def get_warrant_positions(cls) -> list[WarrantPositionItem]:
        """Fetches and adapts warrant positions data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_warrant_positions)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "deal_num": item.get("deal_num", ""),
                    "detail_id": item.get("detail_id", ""),
                    "underlying": item.get("underlying", ""),
                    "ticker": item.get("ticker", ""),
                    "company_name": item.get("company_name", ""),
                    "sec_id": item.get("sec_id", ""),
                    "sec_type": item.get("sec_type", ""),
                    "subtype": item.get("subtype", ""),
                    "currency": item.get("currency", ""),
                    "account_id": item.get("account_id", ""),
                }
            )
        return adapted_data

    @classmethod
    async def get_bond_positions(cls) -> list[BondPositionItem]:
        """Fetches and adapts bond positions data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_bond_positions)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "deal_num": item.get("deal_num", ""),
                    "detail_id": item.get("detail_id", ""),
                    "underlying": item.get("underlying", ""),
                    "ticker": item.get("ticker", ""),
                    "company_name": item.get("company_name", ""),
                    "sec_id": item.get("sec_id", ""),
                    "sec_type": item.get("sec_type", ""),
                    "subtype": item.get("subtype", ""),
                    "currency": item.get("currency", ""),
                    "account_id": item.get("account_id", ""),
                }
            )
        return adapted_data

    @classmethod
    async def get_trade_summaries(cls) -> list[TradeSummaryItem]:
        """Fetches and adapts trade summary data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_trade_summaries)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "deal_num": item.get("deal_num", ""),
                    "detail_id": item.get("detail_id", ""),
                    "ticker": item.get("ticker", ""),
                    "underlying": item.get("underlying", ""),
                    "account_id": item.get("account_id", ""),
                    "company_name": item.get("company_name", ""),
                    "sec_id": item.get("sec_id", ""),
                    "sec_type": item.get("sec_type", ""),
                    "subtype": item.get("subtype", ""),
                    "currency": item.get("currency", ""),
                    "closing_date": item.get("closing_date", ""),
                    "divisor": str(item.get("divisor", "")),
                }
            )
        return adapted_data