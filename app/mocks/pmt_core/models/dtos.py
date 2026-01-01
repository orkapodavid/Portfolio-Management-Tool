from typing import TypedDict, Optional, Union


class PositionDTO(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    account_id: str
    pos_loc: str


class StockPositionDTO(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    currency: str
    account_id: str
    position_location: str
    notional: float


class WarrantPositionDTO(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    subtype: str
    currency: str
    account_id: str


class BondPositionDTO(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    subtype: str
    currency: str
    account_id: str


class TradeSummaryDTO(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    ticker: str
    underlying: str
    account_id: str
    company_name: str
    sec_id: str
    sec_type: str
    subtype: str
    currency: str
    closing_date: str
    divisor: float


class PnLDTO(TypedDict):
    id: int
    trade_date: str
    underlying: str
    ticker: str
    pnl_ytd: float
    pnl_chg_1d: float
    pnl_chg_1w: float
    pnl_chg_1m: float
    pnl_chg_pct_1d: float
    pnl_chg_pct_1w: float
    pnl_chg_pct_1m: float


class PnLSummaryDTO(TypedDict):
    id: int
    trade_date: str
    underlying: str
    currency: str
    price: float
    price_t_1: float
    price_change: float
    fx_rate: float
    fx_rate_t_1: float
    fx_rate_change: float
    dtl: float
    last_volume: float
    adv_3m: float


class PnLCurrencyDTO(TypedDict):
    id: int
    trade_date: str
    currency: str
    fx_rate: float
    fx_rate_t_1: float
    fx_rate_change: float
    ccy_exposure: float
    usd_exposure: float
    pos_ccy_expo: float
    ccy_hedged_pnl: float
    pos_ccy_pnl: float
    net_ccy: float
    pos_c_truncated: float


class MarketDataDTO(TypedDict):
    id: int
    ticker: str
    listed_shares: float
    last_volume: float
    last_price: float
    vwap_price: float
    bid: float
    ask: float
    chg_1d_pct: float
    implied_vol_pct: float
    market_status: str
    created_by: str


class FXDataDTO(TypedDict):
    id: int
    ticker: str
    last_price: float
    bid: float
    ask: float
    created_by: str
    created_time: str
    updated_by: str
    update: str


class HistoricalDataDTO(TypedDict):
    id: int
    trade_date: str
    ticker: str
    vwap_price: float
    last_price: float
    last_volume: float
    chg_1d_pct: float
    created_by: str
    created_time: str
    updated_by: str
    update: str


class RestrictedListDTO(TypedDict):
    id: int
    ticker: str
    company_name: str
    in_emdx: bool
    compliance_type: str
    firm_block: bool
    compliance_start: str
    nda_end: str
    mnpi_end: str
    wc_end: str


class ReconDTO(TypedDict):
    id: int
    trade_date: str
    report_date: str
    deal_num: str
    row_index: str
    underlying: str
    pos_loc: str
    stock_sec_id: str
    warrant_sec_id: str
    bond_sec_id: str
    stock_position: float


class RiskInputDTO(TypedDict):
    id: int
    value_date: str
    underlying: str
    ticker: str
    sec_type: str
    spot_mc: float
    spot_ppd: float
    position: float
    value_mc: float
    value_ppd: float