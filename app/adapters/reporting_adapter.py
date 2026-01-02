from app.adapters.base_adapter import BaseAdapter


class ReportingAdapter(BaseAdapter):
    """Adapter for Reporting services covering PnL, Compliance, and Recon."""

    @classmethod
    async def get_pnl_change(cls) -> list[dict]:
        """Fetches and adapts PnL Change data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_pnl_change)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "underlying": item.get("underlying", ""),
                    "ticker": item.get("ticker", ""),
                    "pnl_ytd": cls.fmt_usd(item.get("pnl_ytd")),
                    "pnl_chg_1d": cls.fmt_usd(item.get("pnl_chg_1d")),
                    "pnl_chg_1w": cls.fmt_usd(item.get("pnl_chg_1w")),
                    "pnl_chg_1m": cls.fmt_usd(item.get("pnl_chg_1m")),
                    "pnl_chg_pct_1d": cls.fmt_pct(item.get("pnl_chg_pct_1d")),
                    "pnl_chg_pct_1w": cls.fmt_pct(item.get("pnl_chg_pct_1w")),
                    "pnl_chg_pct_1m": cls.fmt_pct(item.get("pnl_chg_pct_1m")),
                }
            )
        return adapted_data

    @classmethod
    async def get_pnl_summary(cls) -> list[dict]:
        """Fetches and adapts PnL Summary data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_pnl_summary)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "underlying": item.get("underlying", ""),
                    "currency": item.get("currency", ""),
                    "price": cls.fmt_num(item.get("price")),
                    "price_t_1": cls.fmt_num(item.get("price_t_1")),
                    "price_change": cls.fmt_num(item.get("price_change")),
                    "fx_rate": f"{item.get('fx_rate', 0):.4f}",
                    "fx_rate_t_1": f"{item.get('fx_rate_t_1', 0):.4f}",
                    "fx_rate_change": cls.fmt_num(item.get("fx_rate_change")),
                    "dtl": f"{item.get('dtl', 0):,.0f}",
                    "last_volume": f"{item.get('last_volume', 0):,.0f}",
                    "adv_3m": f"{item.get('adv_3m', 0):,.0f}",
                }
            )
        return adapted_data

    @classmethod
    async def get_pnl_currency(cls) -> list[dict]:
        """Fetches and adapts PnL Currency data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_pnl_currency)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "currency": item.get("currency", ""),
                    "fx_rate": f"{item.get('fx_rate', 0):.4f}",
                    "fx_rate_t_1": f"{item.get('fx_rate_t_1', 0):.4f}",
                    "fx_rate_change": cls.fmt_num(item.get("fx_rate_change")),
                    "ccy_exposure": cls.fmt_usd(item.get("ccy_exposure")),
                    "usd_exposure": cls.fmt_usd(item.get("usd_exposure")),
                    "pos_ccy_expo": cls.fmt_usd(item.get("pos_ccy_expo")),
                    "ccy_hedged_pnl": cls.fmt_usd(item.get("ccy_hedged_pnl")),
                    "pos_ccy_pnl": cls.fmt_usd(item.get("pos_ccy_pnl")),
                    "net_ccy": cls.fmt_usd(item.get("net_ccy")),
                    "pos_c_truncated": cls.fmt_usd(item.get("pos_c_truncated")),
                }
            )
        return adapted_data

    @classmethod
    async def get_restricted_list(cls) -> list[dict]:
        """Fetches and adapts Restricted List data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_restricted_list)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "ticker": item.get("ticker", ""),
                    "company_name": item.get("company_name", ""),
                    "in_emdx": cls.fmt_bool(item.get("in_emdx")),
                    "compliance_type": item.get("compliance_type", ""),
                    "firm_block": cls.fmt_bool(item.get("firm_block")),
                    "compliance_start": item.get("compliance_start", ""),
                    "nda_end": item.get("nda_end", ""),
                    "mnpi_end": item.get("mnpi_end", ""),
                    "wc_end": item.get("wc_end", ""),
                }
            )
        return adapted_data

    @classmethod
    async def get_pnl_recon(cls) -> list[dict]:
        """Fetches and adapts PnL Reconciliation data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_reconciliation_report, "pnl")
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "trade_date": item.get("trade_date", ""),
                    "report_date": item.get("report_date", ""),
                    "deal_num": item.get("deal_num", ""),
                    "row_index": item.get("row_index", ""),
                    "underlying": item.get("underlying", ""),
                    "pos_loc": item.get("pos_loc", ""),
                    "stock_sec_id": item.get("stock_sec_id", ""),
                    "warrant_sec_id": item.get("warrant_sec_id", ""),
                    "bond_sec_id": item.get("bond_sec_id", ""),
                    "stock_position": str(item.get("stock_position", "")),
                }
            )
        return adapted_data

    @classmethod
    async def get_risk_input_recon(cls) -> list[dict]:
        """Fetches and adapts Risk Input Reconciliation data."""
        service = cls.get_service("reporting")
        if not service:
            return []
        raw_data = await cls.execute_async(service.get_risk_inputs)
        if not raw_data:
            return []
        adapted_data = []
        for item in raw_data:
            adapted_data.append(
                {
                    "id": item["id"],
                    "value_date": item.get("value_date", ""),
                    "underlying": item.get("underlying", ""),
                    "ticker": item.get("ticker", ""),
                    "sec_type": item.get("sec_type", ""),
                    "spot_mc": cls.fmt_num(item.get("spot_mc")),
                    "spot_ppd": cls.fmt_num(item.get("spot_ppd")),
                    "position": cls.fmt_num(item.get("position")),
                    "value_mc": cls.fmt_num(item.get("value_mc")),
                    "value_ppd": cls.fmt_num(item.get("value_ppd")),
                }
            )
        return adapted_data