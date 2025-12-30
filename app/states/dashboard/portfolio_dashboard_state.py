import random
from datetime import datetime
from typing import TypedDict
import reflex as rx


class PositionItem(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    account_id: str
    pos_loc: str


class StockPositionItem(TypedDict):
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
    notional: str


class WarrantPositionItem(TypedDict):
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


class BondPositionItem(TypedDict):
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


class TradeSummaryItem(TypedDict):
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
    divisor: str


class NotificationItem(TypedDict):
    id: int
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str
    read: bool


class KPIMetric(TypedDict):
    label: str
    value: str
    is_positive: bool


class TopMover(TypedDict):
    ticker: str
    name: str
    value: str
    change: str
    is_positive: bool


class PnLChangeItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    ticker: str
    pnl_ytd: str
    pnl_chg_1d: str
    pnl_chg_1w: str
    pnl_chg_1m: str
    pnl_chg_pct_1d: str
    pnl_chg_pct_1w: str
    pnl_chg_pct_1m: str


class PnLSummaryItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    currency: str
    price: str
    price_t_1: str
    price_change: str
    fx_rate: str
    fx_rate_t_1: str
    fx_rate_change: str
    dtl: str
    last_volume: str
    adv_3m: str


class PnLCurrencyItem(TypedDict):
    id: int
    trade_date: str
    currency: str
    fx_rate: str
    fx_rate_t_1: str
    fx_rate_change: str
    ccy_exposure: str
    usd_exposure: str
    pos_ccy_expo: str
    ccy_hedged_pnl: str
    pos_ccy_pnl: str
    net_ccy: str
    pos_c_truncated: str


class RestrictedListItem(TypedDict):
    id: int
    ticker: str
    company_name: str
    in_emdx: str
    compliance_type: str
    firm_block: str
    compliance_start: str
    nda_end: str
    mnpi_end: str
    wc_end: str


class UndertakingItem(TypedDict):
    id: int
    deal_num: str
    ticker: str
    company_name: str
    account: str
    undertaking_expiry: str
    undertaking_type: str
    undertaking_details: str


class BeneficialOwnershipItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    company_name: str
    nosh_reported: str
    nosh_bbg: str
    nosh_proforma: str
    stock_shares: str
    warrant_shares: str
    bond_shares: str
    total_shares: str


class MonthlyExerciseLimitItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    company_name: str
    sec_type: str
    original_nosh: str
    original_quantity: str
    monthly_exercised_quantity: str
    monthly_exercised_pct: str
    monthly_sal: str


class PayToHoldItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    currency: str
    counter_party: str
    side: str
    sl_rate: str
    pth_amount_sod: str
    pth_amount: str
    emsa_order: str
    emsa_remark: str
    emsa_working: str
    emsa_order_col: str
    emsa_filled: str


class ShortECLItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    company_name: str
    pos_loc: str
    account: str
    short_position: str
    nosh: str
    short_ownership: str
    last_volume: str
    short_pos_truncated: str


class StockBorrowItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    company_name: str
    jpm_req: str
    jpm_firm: str
    borrow_rate: str
    bofa_req: str
    bofa_firm: str


class POSettlementItem(TypedDict):
    id: int
    deal_num: str
    ticker: str
    company_name: str
    structure: str
    currency: str
    fx_rate: str
    last_price: str
    current_position: str
    shares_allocated: str
    shares_swap: str
    shares_hedged: str


class DealIndicationItem(TypedDict):
    id: int
    ticker: str
    company_name: str
    identification: str
    deal_type: str
    agent: str
    captain: str
    indication_date: str
    currency: str
    market_cap_loc: str
    gross_proceed_loc: str
    indication_amount: str


class ResetDateItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    company_name: str
    sec_type: str
    currency: str
    trade_date: str
    first_reset: str
    expiry: str
    latest_reset: str
    reset_up_down: str
    market_price: str


class ComingResetItem(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    ticker: str
    account: str
    company_name: str
    announce_date: str
    closing_date: str
    cal_days: str
    biz_days: str


class CBInstallmentItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    currency: str
    installment_date: str
    total_amount: str
    outstanding: str
    redeemed: str
    deferred: str
    converted: str
    installment_amount: str
    period: str


class ExcessAmountItem(TypedDict):
    id: int
    deal_num: str
    underlying: str
    ticker: str
    company_name: str
    warrants: str
    excess_amount: str
    threshold: str
    cb_redeem: str
    redeem: str


class PPSReconItem(TypedDict):
    id: int
    value_date: str
    trade_date: str
    underlying: str
    ticker: str
    code: str
    company_name: str
    sec_type: str
    pos_loc: str
    account: str


class SettlementReconItem(TypedDict):
    id: int
    trade_date: str
    ml_report_date: str
    underlying: str
    ticker: str
    company_name: str
    pos_loc: str
    currency: str
    sec_type: str
    position_settled: str
    ml_inventory: str


class FailedTradeItem(TypedDict):
    id: int
    report_date: str
    trade_date: str
    value_date: str
    settlement_date: str
    portfolio_code: str
    instrument_ref: str
    instrument_name: str
    ticker: str
    company_name: str
    isin: str
    sedol: str
    broker: str
    glass_reference: str
    trade_reference: str
    deal_type: str
    q: str


class PnLReconItem(TypedDict):
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
    stock_position: str


class RiskInputReconItem(TypedDict):
    id: int
    value_date: str
    underlying: str
    ticker: str
    sec_type: str
    spot_mc: str
    spot_ppd: str
    position: str
    value_mc: str
    value_ppd: str


class DailyProcedureItem(TypedDict):
    id: int
    check_date: str
    host_run_date: str
    scheduled_time: str
    procedure_name: str
    status: str
    error_message: str
    frequency: str
    scheduled_day: str
    created_by: str
    created_time: str


class OperationProcessItem(TypedDict):
    id: int
    process: str
    status: str
    last_run_time: str


class MarketDataItem(TypedDict):
    id: int
    ticker: str
    listed_shares: str
    last_volume: str
    last_price: str
    vwap_price: str
    bid: str
    ask: str
    chg_1d_pct: str
    implied_vol_pct: str
    market_status: str
    created_by: str


class FXDataItem(TypedDict):
    id: int
    ticker: str
    last_price: str
    bid: str
    ask: str
    created_by: str
    created_time: str
    updated_by: str
    update: str


class HistoricalDataItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    vwap_price: str
    last_price: str
    last_volume: str
    chg_1d_pct: str
    created_by: str
    created_time: str
    updated_by: str
    update: str


class TradingCalendarItem(TypedDict):
    id: int
    trade_date: str
    day_of_week: str
    usa: str
    hkg: str
    jpn: str
    aus: str
    nzl: str
    kor: str
    chn: str
    twn: str
    ind: str


class MarketHoursItem(TypedDict):
    id: int
    market: str
    ticker: str
    session: str
    local_time: str
    session_period: str
    is_open: str
    timezone: str


class EventCalendarItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    company: str
    event_date: str
    day_of_week: str
    event_type: str
    time: str


class EventStreamItem(TypedDict):
    id: int
    symbol: str
    record_date: str
    event_date: str
    day_of_week: str
    event_type: str
    subject: str
    notes: str
    alerted: str
    recur: str
    created_by: str
    created_time: str
    updated_by: str
    updated_time: str


class ReverseInquiryItem(TypedDict):
    id: int
    ticker: str
    company: str
    inquiry_date: str
    expiry_date: str
    deal_point: str
    agent: str
    notes: str


class TickerDataItem(TypedDict):
    id: int
    ticker: str
    currency: str
    fx_rate: str
    sector: str
    company: str
    po_lead_manager: str
    fmat_cap: str
    smkt_cap: str
    chg_1d_pct: str
    dtl: str


class StockScreenerItem(TypedDict):
    id: int
    otl: str
    mkt_cap_37_pct: str
    ticker: str
    company: str
    country: str
    industry: str
    last_price: str
    mkt_cap_loc: str
    mkt_cap_usd: str
    adv_3m: str
    locate_qty_mm: str
    locate_f: str


class SpecialTermItem(TypedDict):
    id: int
    deal_num: str
    ticker: str
    company_name: str
    sec_type: str
    pos_loc: str
    account: str
    effective_date: str
    position: str


class InstrumentDataItem(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    pos_loc: str
    account: str


class InstrumentTermItem(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_type: str
    effective_date: str
    maturity_date: str
    first_reset_da: str


class DeltaChangeItem(TypedDict):
    id: int
    ticker: str
    company_name: str
    structure: str
    currency: str
    fx_rate: str
    current_price: str
    valuation_price: str
    pos_delta: str
    pos_delta_small: str
    pos_g: str


class RiskMeasureItem(TypedDict):
    id: int
    seed: str
    simulation_num: str
    trial_num: str
    underlying: str
    ticker: str
    sec_type: str
    is_private: str
    national: str
    national_used: str
    national_current: str
    currency: str
    fx_rate: str
    spot_price: str


class RiskInputItem(TypedDict):
    id: int
    seed: str
    simulation_num: str
    trial_num: str
    underlying: str
    ticker: str
    sec_type: str
    is_private: str
    national: str
    national_used: str
    national_current: str
    currency: str
    fx_rate: str
    spot_price: str


class EMSAOrderItem(TypedDict):
    id: int
    sequence: str
    underlying: str
    ticker: str
    broker: str
    pos_loc: str
    side: str
    status: str
    emsa_amount: str
    emsa_routed: str
    emsa_working: str
    emsa_filled: str


def _fmt_usd(val: float) -> str:
    return f"${val:,.2f}" if val >= 0 else f"$({abs(val):,.2f})"


def _fmt_num(val: float) -> str:
    return f"{val:,.2f}" if val >= 0 else f"({abs(val):,.2f})"


def _fmt_pct(val: float) -> str:
    return f"{val:,.2f}%"


def _generate_pnl_change_data() -> list[PnLChangeItem]:
    tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "TSLA",
        "NVDA",
        "META",
        "NFLX",
        "AMD",
        "INTC",
        "JPM",
        "BAC",
        "WFC",
        "C",
        "GS",
        "MS",
        "BLK",
        "SPY",
        "QQQ",
        "IWM",
    ]
    data = []
    for i, ticker in enumerate(tickers):
        base_pnl = random.uniform(-50000, 150000)
        chg_1d = random.uniform(-5000, 5000)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "underlying": f"{ticker} US Equity",
                "ticker": ticker,
                "pnl_ytd": _fmt_usd(base_pnl),
                "pnl_chg_1d": _fmt_usd(chg_1d),
                "pnl_chg_1w": _fmt_usd(chg_1d * 3.5),
                "pnl_chg_1m": _fmt_usd(chg_1d * 12.0),
                "pnl_chg_pct_1d": _fmt_pct(random.uniform(-3, 3)),
                "pnl_chg_pct_1w": _fmt_pct(random.uniform(-8, 8)),
                "pnl_chg_pct_1m": _fmt_pct(random.uniform(-15, 15)),
            }
        )
    return data


def _generate_pnl_summary_data() -> list[PnLSummaryItem]:
    tickers = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "TSLA",
        "NVDA",
        "META",
        "NFLX",
        "AMD",
        "INTC",
    ]
    currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "SGD"]
    data = []
    for i in range(20):
        ticker = tickers[i % len(tickers)]
        ccy = currencies[i % len(currencies)]
        price = random.uniform(100, 1000)
        price_t1 = price * random.uniform(0.95, 1.05)
        fx = random.uniform(0.8, 1.5)
        fx_t1 = fx * random.uniform(0.99, 1.01)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "underlying": f"{ticker} US Equity",
                "currency": ccy,
                "price": _fmt_num(price),
                "price_t_1": _fmt_num(price_t1),
                "price_change": _fmt_num(price - price_t1),
                "fx_rate": f"{fx:,.4f}",
                "fx_rate_t_1": f"{fx_t1:,.4f}",
                "fx_rate_change": _fmt_num(fx - fx_t1),
                "dtl": f"{random.uniform(0, 1000):,.0f}",
                "last_volume": f"{random.randint(100000, 5000000):,.0f}",
                "adv_3m": f"{random.randint(100000, 5000000):,.0f}",
            }
        )
    return data


def _generate_pnl_currency_data() -> list[PnLCurrencyItem]:
    currencies = [
        "USD",
        "EUR",
        "GBP",
        "JPY",
        "CAD",
        "AUD",
        "CHF",
        "CNY",
        "HKD",
        "SGD",
        "SEK",
        "NOK",
        "DKK",
        "NZD",
        "MXN",
        "BRL",
        "INR",
        "KRW",
        "ZAR",
        "TRY",
    ]
    data = []
    for i, ccy in enumerate(currencies):
        fx = random.uniform(0.5, 1.5)
        fx_t1 = fx * random.uniform(0.98, 1.02)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "currency": ccy,
                "fx_rate": f"{fx:,.4f}",
                "fx_rate_t_1": f"{fx_t1:,.4f}",
                "fx_rate_change": _fmt_num(fx - fx_t1),
                "ccy_exposure": _fmt_usd(random.uniform(-1000000, 1000000)),
                "usd_exposure": _fmt_usd(random.uniform(-1000000, 1000000)),
                "pos_ccy_expo": _fmt_usd(random.uniform(-500000, 500000)),
                "ccy_hedged_pnl": _fmt_usd(random.uniform(-10000, 10000)),
                "pos_ccy_pnl": _fmt_usd(random.uniform(-20000, 20000)),
                "net_ccy": _fmt_usd(random.uniform(-5000, 5000)),
                "pos_c_truncated": _fmt_usd(random.uniform(-500, 500)),
            }
        )
    return data


def _generate_positions_data() -> list[PositionItem]:
    tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "BTC-USD", "EURUSD", "US10Y"]
    companies = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corp.",
        "GOOGL": "Alphabet Inc.",
        "TSLA": "Tesla Inc.",
        "NVDA": "NVIDIA Corp.",
        "BTC-USD": "Bitcoin",
        "EURUSD": "Euro/USD",
        "US10Y": "US Treasury 10Y",
    }
    data = []
    for i, t in enumerate(tickers):
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "underlying": f"{t} US",
                "ticker": t,
                "company_name": companies.get(t, t),
                "account_id": f"ACC-{random.randint(10, 99)}",
                "pos_loc": random.choice(["NY", "LN", "HK"]),
            }
        )
    return data


def _generate_stock_positions() -> list[StockPositionItem]:
    tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "NFLX"]
    companies = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corp.",
        "AMZN": "Amazon.com",
        "GOOGL": "Alphabet Inc.",
        "META": "Meta Platforms",
        "NVDA": "NVIDIA Corp.",
        "NFLX": "Netflix Inc.",
    }
    data = []
    for i, t in enumerate(tickers):
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "ticker": t,
                "company_name": companies.get(t, t),
                "sec_id": f"US{random.randint(100000000, 999999999)}",
                "sec_type": "Common Stock",
                "currency": "USD",
                "account_id": f"ACC-{random.randint(10, 99)}",
                "position_location": random.choice(["NY", "LN", "HK"]),
                "notional": _fmt_usd(random.uniform(100000, 5000000)),
            }
        )
    return data


def _generate_warrant_positions() -> list[WarrantPositionItem]:
    underlyings = ["AAPL", "TSLA", "NVDA", "AMZN"]
    data = []
    for i in range(10):
        und = random.choice(underlyings)
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "underlying": und,
                "ticker": f"{und}-W",
                "company_name": f"{und} Warrant",
                "sec_id": f"W{random.randint(100000, 999999)}",
                "sec_type": "Warrant",
                "subtype": random.choice(["Call", "Put"]),
                "currency": "USD",
                "account_id": f"ACC-{random.randint(10, 99)}",
            }
        )
    return data


def _generate_bond_positions() -> list[BondPositionItem]:
    issuers = ["US GOVT", "APPLE INC", "MICROSOFT", "GOLDMAN SACHS", "JPM"]
    data = []
    for i, issuer in enumerate(issuers):
        data.append(
            {
                "id": i,
                "trade_date": datetime.now().strftime("%Y-%m-%d"),
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "underlying": issuer,
                "ticker": f"{issuer[:4]} 4.5%",
                "company_name": issuer,
                "sec_id": f"US{random.randint(100000000, 999999999)}",
                "sec_type": "Corp Bond",
                "subtype": "Fixed",
                "currency": "USD",
                "account_id": f"ACC-{random.randint(10, 99)}",
            }
        )
    return data


def _generate_trade_summaries() -> list[TradeSummaryItem]:
    tickers = ["AAPL", "MSFT", "TSLA", "EURUSD", "US10Y"]
    data = []
    for i in range(15):
        ticker = random.choice(tickers)
        data.append(
            {
                "id": i,
                "deal_num": f"{random.randint(100000, 999999)}",
                "detail_id": f"{random.randint(1000, 9999)}",
                "ticker": ticker,
                "underlying": f"{ticker} US",
                "account_id": f"ACC-{random.randint(10, 99)}",
                "company_name": f"{ticker} Inc",
                "sec_id": f"US{random.randint(100000000, 999999999)}",
                "sec_type": "Equity",
                "subtype": "Common",
                "currency": "USD",
                "closing_date": "2024-12-31",
                "divisor": f"{random.uniform(0.1, 1.0):.4f}",
            }
        )
    return data


def _generate_compliance_data() -> tuple[list, list, list, list]:
    restricted = []
    for i in range(10):
        restricted.append(
            {
                "id": i,
                "ticker": f"TKR{i}",
                "company_name": f"Company {i}",
                "in_emdx": random.choice(["Yes", "No"]),
                "compliance_type": "Watch",
                "firm_block": "No",
                "compliance_start": "2024-01-01",
                "nda_end": "2024-12-31",
                "mnpi_end": "",
                "wc_end": "",
            }
        )
    undertakings = []
    for i in range(10):
        undertakings.append(
            {
                "id": i,
                "deal_num": f"DL{i + 1000}",
                "ticker": f"TKR{i}",
                "company_name": f"Company {i}",
                "account": f"ACC{i}",
                "undertaking_expiry": "2025-06-30",
                "undertaking_type": "Lock-up",
                "undertaking_details": "No selling",
            }
        )
    ownership = []
    for i in range(10):
        ownership.append(
            {
                "id": i,
                "trade_date": "2024-03-20",
                "ticker": f"TKR{i}",
                "company_name": f"Company {i}",
                "nosh_reported": "10M",
                "nosh_bbg": "10.5M",
                "nosh_proforma": "10.5M",
                "stock_shares": "500K",
                "warrant_shares": "0",
                "bond_shares": "0",
                "total_shares": "500K",
            }
        )
    limits = []
    for i in range(10):
        limits.append(
            {
                "id": i,
                "underlying": f"UND{i}",
                "ticker": f"TKR{i}",
                "company_name": f"Company {i}",
                "sec_type": "Warrant",
                "original_nosh": "20M",
                "original_quantity": "1M",
                "monthly_exercised_quantity": "100K",
                "monthly_exercised_pct": "10%",
                "monthly_sal": "500K",
            }
        )
    return (restricted, undertakings, ownership, limits)


def _generate_tools_data() -> tuple[
    list, list, list, list, list, list, list, list, list
]:
    def common(i):
        return {
            "id": i,
            "trade_date": "2024-03-20",
            "ticker": f"TKR{i}",
            "company_name": f"Comp {i}",
            "currency": "USD",
        }

    pth = [
        dict(
            common(i),
            **{
                "counter_party": "GS",
                "side": "Buy",
                "sl_rate": "0.25%",
                "pth_amount_sod": "100K",
                "pth_amount": "150K",
                "emsa_order": "ORD123",
                "emsa_remark": "",
                "emsa_working": "0",
                "emsa_order_col": "ORD123",
                "emsa_filled": "50K",
            },
        )
        for i in range(10)
    ]
    ecl = [
        dict(
            common(i),
            **{
                "pos_loc": "NY",
                "account": "Main",
                "short_position": "-5000",
                "nosh": "100M",
                "short_ownership": "0.005%",
                "last_volume": "1M",
                "short_pos_truncated": "-5K",
            },
        )
        for i in range(10)
    ]
    borrow = [
        dict(
            common(i),
            **{
                "jpm_req": "10K",
                "jpm_firm": "Yes",
                "borrow_rate": "0.4%",
                "bofa_req": "5K",
                "bofa_firm": "No",
            },
        )
        for i in range(10)
    ]
    settle = [
        dict(
            common(i),
            **{
                "deal_num": f"D{i}",
                "structure": "Equity",
                "fx_rate": "1.0",
                "last_price": "100.0",
                "current_position": "50K",
                "shares_allocated": "50K",
                "shares_swap": "0",
                "shares_hedged": "10K",
            },
        )
        for i in range(10)
    ]
    deals = [
        dict(
            common(i),
            **{
                "identification": "ID123",
                "deal_type": "IPO",
                "agent": "MS",
                "captain": "JD",
                "indication_date": "2024-04-01",
                "market_cap_loc": "500M",
                "gross_proceed_loc": "100M",
                "indication_amount": "10M",
            },
        )
        for i in range(10)
    ]
    resets = [
        dict(
            common(i),
            **{
                "underlying": f"UND{i}",
                "sec_type": "CB",
                "first_reset": "2024-06-01",
                "expiry": "2029-06-01",
                "latest_reset": "2024-03-01",
                "reset_up_down": "Down",
                "market_price": "98.5",
            },
        )
        for i in range(10)
    ]
    coming = [
        dict(
            common(i),
            **{
                "deal_num": f"D{i}",
                "detail_id": f"DT{i}",
                "account": "Main",
                "announce_date": "2024-04-15",
                "closing_date": "2024-04-20",
                "cal_days": "25",
                "biz_days": "18",
            },
        )
        for i in range(10)
    ]
    install = [
        dict(
            common(i),
            **{
                "underlying": f"UND{i}",
                "installment_date": "2024-05-01",
                "total_amount": "1M",
                "outstanding": "500K",
                "redeemed": "200K",
                "deferred": "0",
                "converted": "300K",
                "installment_amount": "100K",
                "period": "Q1",
            },
        )
        for i in range(10)
    ]
    excess = [
        dict(
            common(i),
            **{
                "deal_num": f"D{i}",
                "underlying": f"UND{i}",
                "warrants": "50K",
                "excess_amount": "10K",
                "threshold": "5%",
                "cb_redeem": "0",
                "redeem": "0",
            },
        )
        for i in range(10)
    ]
    return (pth, ecl, borrow, settle, deals, resets, coming, install, excess)


def _generate_recon_data() -> tuple[list, list, list, list, list]:
    pps = [
        {
            "id": i,
            "value_date": "2024-03-20",
            "trade_date": "2024-03-18",
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "code": "C1",
            "company_name": f"Company {i}",
            "sec_type": "Equity",
            "pos_loc": "NY",
            "account": "Main",
        }
        for i in range(10)
    ]
    settle = [
        {
            "id": i,
            "trade_date": "2024-03-18",
            "ml_report_date": "2024-03-19",
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "company_name": f"Company {i}",
            "pos_loc": "LN",
            "currency": "USD",
            "sec_type": "Equity",
            "position_settled": "Yes",
            "ml_inventory": "1000",
        }
        for i in range(10)
    ]
    failed = [
        {
            "id": i,
            "report_date": "2024-03-20",
            "trade_date": "2024-03-15",
            "value_date": "2024-03-17",
            "settlement_date": "2024-03-17",
            "portfolio_code": "P1",
            "instrument_ref": f"REF{i}",
            "instrument_name": f"Inst {i}",
            "ticker": f"TKR{i}",
            "company_name": f"Company {i}",
            "isin": f"US{i}999",
            "sedol": f"B0{i}XYZ",
            "broker": "MS",
            "glass_reference": "G123",
            "trade_reference": "T123",
            "deal_type": "Buy",
            "q": "100",
        }
        for i in range(10)
    ]
    pnl_rec = [
        {
            "id": i,
            "trade_date": "2024-03-20",
            "report_date": "2024-03-20",
            "deal_num": f"D{i}",
            "row_index": str(i),
            "underlying": f"UND{i}",
            "pos_loc": "NY",
            "stock_sec_id": f"S{i}",
            "warrant_sec_id": f"W{i}",
            "bond_sec_id": f"B{i}",
            "stock_position": "1000",
        }
        for i in range(10)
    ]
    risk_rec = [
        {
            "id": i,
            "value_date": "2024-03-20",
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "sec_type": "Equity",
            "spot_mc": "100.0",
            "spot_ppd": "100.1",
            "position": "500",
            "value_mc": "50000",
            "value_ppd": "50050",
        }
        for i in range(10)
    ]
    return (pps, settle, failed, pnl_rec, risk_rec)


def _generate_ops_data() -> tuple[list, list]:
    daily = [
        {
            "id": i,
            "check_date": "2024-03-20",
            "host_run_date": "2024-03-20",
            "scheduled_time": "09:00",
            "procedure_name": f"Proc {i}",
            "status": "Success",
            "error_message": "",
            "frequency": "Daily",
            "scheduled_day": "All",
            "created_by": "System",
            "created_time": "09:01",
        }
        for i in range(10)
    ]
    ops = [
        {
            "id": i,
            "process": f"Process {i}",
            "status": random.choice(["Active", "Inactive", "Running", "Error"]),
            "last_run_time": "10:00 AM",
        }
        for i in range(10)
    ]
    return (daily, ops)


def _generate_market_data() -> tuple[list, list, list, list, list, list, list, list]:
    mkt = [
        {
            "id": i,
            "ticker": f"TKR{i}",
            "listed_shares": "100M",
            "last_volume": "500K",
            "last_price": "150.00",
            "vwap_price": "149.50",
            "bid": "149.90",
            "ask": "150.10",
            "chg_1d_pct": "+0.5%",
            "implied_vol_pct": "15%",
            "market_status": "Open",
            "created_by": "Feed",
        }
        for i in range(10)
    ]
    fx = [
        {
            "id": i,
            "ticker": f"USD/EUR",
            "last_price": "0.92",
            "bid": "0.919",
            "ask": "0.921",
            "created_by": "System",
            "created_time": "09:00",
            "updated_by": "System",
            "update": "09:05",
        }
        for i in range(10)
    ]
    hist = [
        {
            "id": i,
            "trade_date": "2024-03-19",
            "ticker": f"TKR{i}",
            "vwap_price": "148.00",
            "last_price": "148.50",
            "last_volume": "450K",
            "chg_1d_pct": "-0.2%",
            "created_by": "System",
            "created_time": "17:00",
            "updated_by": "System",
            "update": "17:05",
        }
        for i in range(10)
    ]
    cal = [
        {
            "id": i,
            "trade_date": "2024-03-20",
            "day_of_week": "Wednesday",
            "usa": "Open",
            "hkg": "Closed",
            "jpn": "Open",
            "aus": "Open",
            "nzl": "Open",
            "kor": "Open",
            "chn": "Open",
            "twn": "Open",
            "ind": "Open",
        }
        for i in range(10)
    ]
    hours = [
        {
            "id": i,
            "market": "NYSE",
            "ticker": "All",
            "session": "Regular",
            "local_time": "09:30 - 16:00",
            "session_period": "Day",
            "is_open": "Yes",
            "timezone": "EST",
        }
        for i in range(5)
    ]
    ev_cal = [
        {
            "id": i,
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "company": f"Comp {i}",
            "event_date": "2024-04-01",
            "day_of_week": "Monday",
            "event_type": "Earnings",
            "time": "16:00",
        }
        for i in range(10)
    ]
    stream = [
        {
            "id": i,
            "symbol": f"TKR{i}",
            "record_date": "2024-03-20",
            "event_date": "2024-03-20",
            "day_of_week": "Wed",
            "event_type": "News",
            "subject": "Announcement",
            "notes": "Details...",
            "alerted": "No",
            "recur": "No",
            "created_by": "User",
            "created_time": "10:00",
            "updated_by": "User",
            "updated_time": "10:00",
        }
        for i in range(10)
    ]
    rev = [
        {
            "id": i,
            "ticker": f"TKR{i}",
            "company": f"Comp {i}",
            "inquiry_date": "2024-03-15",
            "expiry_date": "2024-03-22",
            "deal_point": "Mid",
            "agent": "GS",
            "notes": "Note...",
        }
        for i in range(10)
    ]
    return (mkt, fx, hist, cal, hours, ev_cal, stream, rev)


def _generate_instrument_data() -> tuple[list, list, list, list, list]:
    ticker = [
        {
            "id": i,
            "ticker": f"TKR{i}",
            "currency": "USD",
            "fx_rate": "1.0",
            "sector": "Tech",
            "company": f"Comp {i}",
            "po_lead_manager": "MS",
            "fmat_cap": "10B",
            "smkt_cap": "9B",
            "chg_1d_pct": "+1.2%",
            "dtl": "5",
        }
        for i in range(10)
    ]
    screener = [
        {
            "id": i,
            "otl": "Top",
            "mkt_cap_37_pct": "37%",
            "ticker": f"TKR{i}",
            "company": f"Comp {i}",
            "country": "USA",
            "industry": "Tech",
            "last_price": "150.0",
            "mkt_cap_loc": "10B",
            "mkt_cap_usd": "10B",
            "adv_3m": "1M",
            "locate_qty_mm": "500K",
            "locate_f": "Yes",
        }
        for i in range(10)
    ]
    special = [
        {
            "id": i,
            "deal_num": f"D{i}",
            "ticker": f"TKR{i}",
            "company_name": f"Comp {i}",
            "sec_type": "Equity",
            "pos_loc": "NY",
            "account": "Main",
            "effective_date": "2024-01-01",
            "position": "1000",
        }
        for i in range(10)
    ]
    inst = [
        {
            "id": i,
            "deal_num": f"D{i}",
            "detail_id": f"DT{i}",
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "company_name": f"Comp {i}",
            "sec_id": f"SEC{i}",
            "sec_type": "Equity",
            "pos_loc": "NY",
            "account": "Main",
        }
        for i in range(10)
    ]
    term = [
        {
            "id": i,
            "deal_num": f"D{i}",
            "detail_id": f"DT{i}",
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "company_name": f"Comp {i}",
            "sec_type": "Equity",
            "effective_date": "2024-01-01",
            "maturity_date": "2025-01-01",
            "first_reset_da": "2024-06-01",
        }
        for i in range(10)
    ]
    return (ticker, screener, special, inst, term)


def _generate_risk_data() -> tuple[list, list, list]:
    delta = [
        {
            "id": i,
            "ticker": f"TKR{i}",
            "company_name": f"Comp {i}",
            "structure": "Struct",
            "currency": "USD",
            "fx_rate": "1.0",
            "current_price": "150.0",
            "valuation_price": "149.0",
            "pos_delta": "0.5",
            "pos_delta_small": "0.5",
            "pos_g": "0.1",
        }
        for i in range(10)
    ]
    measures = [
        {
            "id": i,
            "seed": "12345",
            "simulation_num": "1",
            "trial_num": "1",
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "sec_type": "Equity",
            "is_private": "No",
            "national": "US",
            "national_used": "US",
            "national_current": "US",
            "currency": "USD",
            "fx_rate": "1.0",
            "spot_price": "150.0",
        }
        for i in range(10)
    ]
    inputs = [
        {
            "id": i,
            "seed": "67890",
            "simulation_num": "2",
            "trial_num": "1",
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "sec_type": "Equity",
            "is_private": "No",
            "national": "US",
            "national_used": "US",
            "national_current": "US",
            "currency": "USD",
            "fx_rate": "1.0",
            "spot_price": "150.0",
        }
        for i in range(10)
    ]
    return (delta, measures, inputs)


def _generate_emsa_data() -> tuple[list, list]:
    orders = [
        {
            "id": i,
            "sequence": str(i),
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "broker": "GS",
            "pos_loc": "NY",
            "side": "Buy",
            "status": "Filled",
            "emsa_amount": "1000",
            "emsa_routed": "1000",
            "emsa_working": "0",
            "emsa_filled": "1000",
        }
        for i in range(10)
    ]
    routes = [
        {
            "id": i,
            "sequence": str(i),
            "underlying": f"UND{i}",
            "ticker": f"TKR{i}",
            "broker": "MS",
            "pos_loc": "LN",
            "side": "Sell",
            "status": "Working",
            "emsa_amount": "500",
            "emsa_routed": "500",
            "emsa_working": "500",
            "emsa_filled": "0",
        }
        for i in range(10)
    ]
    return (orders, routes)


def _generate_mock_data() -> list[dict]:
    """Generates mock data once at module load time."""
    base_data = [
        {
            "id": 1,
            "ticker": "AAPL",
            "description": "Apple Inc.",
            "asset_class": "Equity",
            "qty": "15,400",
            "price": "182.50",
            "mkt_value": "2,810,500",
            "daily_pnl": "+12,450",
            "pnl_pct": "+0.45%",
            "status": "Active",
            "is_positive": True,
            "is_reconciled": True,
        },
        {
            "id": 2,
            "ticker": "MSFT",
            "description": "Microsoft Corp.",
            "asset_class": "Equity",
            "qty": "8,200",
            "price": "405.12",
            "mkt_value": "3,321,984",
            "daily_pnl": "(1,230)",
            "pnl_pct": "-0.03%",
            "status": "Active",
            "is_positive": False,
            "is_reconciled": True,
        },
        {
            "id": 3,
            "ticker": "US10Y",
            "description": "US Treasury 10Y",
            "asset_class": "Bond",
            "qty": "5,000,000",
            "price": "98.25",
            "mkt_value": "4,912,500",
            "daily_pnl": "+5,600",
            "pnl_pct": "+0.11%",
            "status": "Hedged",
            "is_positive": True,
            "is_reconciled": True,
        },
        {
            "id": 4,
            "ticker": "EURUSD",
            "description": "Euro / US Dollar",
            "asset_class": "FX",
            "qty": "2,500,000",
            "price": "1.0850",
            "mkt_value": "2,712,500",
            "daily_pnl": "(4,500)",
            "pnl_pct": "-0.16%",
            "status": "Active",
            "is_positive": False,
            "is_reconciled": True,
        },
        {
            "id": 5,
            "ticker": "NVDA",
            "description": "NVIDIA Corp",
            "asset_class": "Equity",
            "qty": "4,500",
            "price": "785.30",
            "mkt_value": "3,533,850",
            "daily_pnl": "+45,200",
            "pnl_pct": "+1.28%",
            "status": "Active",
            "is_positive": True,
            "is_reconciled": False,
        },
        {
            "id": 6,
            "ticker": "GLD",
            "description": "SPDR Gold Shares",
            "asset_class": "Commodity",
            "qty": "12,000",
            "price": "195.40",
            "mkt_value": "2,344,800",
            "daily_pnl": "+8,900",
            "pnl_pct": "+0.38%",
            "status": "Hedged",
            "is_positive": True,
            "is_reconciled": True,
        },
        {
            "id": 7,
            "ticker": "TSLA",
            "description": "Tesla Inc.",
            "asset_class": "Equity",
            "qty": "10,000",
            "price": "175.20",
            "mkt_value": "1,752,000",
            "daily_pnl": "(15,400)",
            "pnl_pct": "-0.88%",
            "status": "Review",
            "is_positive": False,
            "is_reconciled": False,
        },
        {
            "id": 8,
            "ticker": "VIX",
            "description": "Volatility Index",
            "asset_class": "Index",
            "qty": "5,000",
            "price": "13.45",
            "mkt_value": "67,250",
            "daily_pnl": "(250)",
            "pnl_pct": "-0.37%",
            "status": "Hedged",
            "is_positive": False,
            "is_reconciled": True,
        },
    ]
    expanded_data = []
    for i in range(50):
        for item in base_data:
            new_item = item.copy()
            new_item["id"] = len(expanded_data) + 1
            expanded_data.append(new_item)
    return expanded_data


class PortfolioDashboardState(rx.State):
    active_module: str = "Market Data"
    _active_subtabs: dict[str, str] = {}
    _filters: dict[str, dict] = {}
    is_sidebar_open: bool = True
    is_mobile_menu_open: bool = False
    is_generate_menu_open: bool = False
    show_top_movers: bool = False
    selected_row_id: int = -1
    is_loading: bool = False
    kpi_metrics: list[KPIMetric] = [
        {"label": "Daily PnL", "value": "+$1.2M", "is_positive": True},
        {"label": "Daily Pos FX", "value": "($45K)", "is_positive": False},
        {"label": "Daily CCY Hedged", "value": "+$12K", "is_positive": True},
        {"label": "YTD Disc PnL", "value": "+$45.8M", "is_positive": True},
        {"label": "YTD R/U PnL", "value": "($2.1M)", "is_positive": False},
    ]
    top_movers_ops: list[TopMover] = [
        {
            "ticker": "AAPL",
            "name": "Apple",
            "value": "$4.5M",
            "change": "+1.2%",
            "is_positive": True,
        },
        {
            "ticker": "MSFT",
            "name": "Microsoft",
            "value": "$3.2M",
            "change": "+0.8%",
            "is_positive": True,
        },
        {
            "ticker": "TSLA",
            "name": "Tesla",
            "value": "($1.5M)",
            "change": "-2.1%",
            "is_positive": False,
        },
        {
            "ticker": "NVDA",
            "name": "NVIDIA",
            "value": "$2.1M",
            "change": "+3.5%",
            "is_positive": True,
        },
    ]
    top_movers_ytd: list[TopMover] = [
        {
            "ticker": "NVDA",
            "name": "NVIDIA",
            "value": "$15.2M",
            "change": "+45%",
            "is_positive": True,
        },
        {
            "ticker": "META",
            "name": "Meta",
            "value": "$8.4M",
            "change": "+22%",
            "is_positive": True,
        },
        {
            "ticker": "PFE",
            "name": "Pfizer",
            "value": "($2.1M)",
            "change": "-12%",
            "is_positive": False,
        },
        {
            "ticker": "XOM",
            "name": "Exxon",
            "value": "$5.1M",
            "change": "+8%",
            "is_positive": True,
        },
    ]
    top_movers_delta: list[TopMover] = [
        {
            "ticker": "SPY",
            "name": "S&P 500",
            "value": "$500K",
            "change": "+0.5",
            "is_positive": True,
        },
        {
            "ticker": "QQQ",
            "name": "Nasdaq",
            "value": "$320K",
            "change": "+0.8",
            "is_positive": True,
        },
        {
            "ticker": "IWM",
            "name": "Russell",
            "value": "($120K)",
            "change": "-0.3",
            "is_positive": False,
        },
        {
            "ticker": "GLD",
            "name": "Gold",
            "value": "$50K",
            "change": "+0.1",
            "is_positive": True,
        },
    ]
    top_movers_price: list[TopMover] = [
        {
            "ticker": "AMD",
            "name": "AMD",
            "value": "$180.5",
            "change": "+5.2%",
            "is_positive": True,
        },
        {
            "ticker": "COIN",
            "name": "Coinbase",
            "value": "$240.2",
            "change": "+8.4%",
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
    ]
    top_movers_volume: list[TopMover] = [
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
    ]
    notifications: list[NotificationItem] = [
        {
            "id": 1,
            "header": "Begin Covering",
            "ticker": "AAPL",
            "timestamp": "09:30 AM",
            "instruction": "Action required before market open",
            "type": "alert",
            "read": False,
        },
        {
            "id": 2,
            "header": "Manual Booking",
            "ticker": "MSFT",
            "timestamp": "10:15 AM",
            "instruction": "Verify trade settlement details",
            "type": "info",
            "read": False,
        },
        {
            "id": 3,
            "header": "Risk Alert",
            "ticker": "TSLA",
            "timestamp": "11:00 AM",
            "instruction": "Delta exposure exceeds threshold",
            "type": "warning",
            "read": False,
        },
        {
            "id": 4,
            "header": "Corporate Action",
            "ticker": "GOOGL",
            "timestamp": "12:45 PM",
            "instruction": "Stock split adjustments pending",
            "type": "info",
            "read": True,
        },
        {
            "id": 5,
            "header": "Settlement Fail",
            "ticker": "AMZN",
            "timestamp": "02:20 PM",
            "instruction": "Contact counterparty immediately",
            "type": "alert",
            "read": False,
        },
    ]
    module_icons: dict[str, str] = {
        "Market Data": "bar-chart-2",
        "Positions": "briefcase",
        "PnL": "dollar-sign",
        "Risk": "shield-alert",
        "Recon": "file-check-2",
        "Compliance": "scale",
        "Portfolio Tools": "wrench",
        "Instruments": "layers",
        "Events": "calendar",
        "Operations": "settings",
        "Orders": "shopping-cart",
    }
    MODULE_SUBTABS: dict[str, list[str]] = {
        "Market Data": [
            "Market Data",
            "FX Data",
            "Reference Data",
            "Historical Data",
            "Trading Calendar",
            "Market Hours",
        ],
        "Positions": [
            "Positions",
            "Stock Position",
            "Warrant Position",
            "Bond Positions",
            "Trade Summary (War/Bond)",
        ],
        "PnL": ["PnL Change", "PnL Full", "PnL Summary", "PnL Currency"],
        "Risk": [
            "Delta Change",
            "Risk Measures",
            "Risk Inputs",
            "Pricer Warrant",
            "Pricer Bond",
        ],
        "Recon": [
            "PPS Recon",
            "Settlement Recon",
            "Failed Trades",
            "PnL Recon",
            "Risk Input Recon",
        ],
        "Compliance": [
            "Restricted List",
            "Undertakings",
            "Beneficial Ownership",
            "Monthly Exercise Limit",
        ],
        "Portfolio Tools": [
            "Pay-To-Hold",
            "Short ECL",
            "Stock Borrow",
            "PO Settlement",
            "Deal Indication",
            "Reset Dates",
            "Coming Resets",
            "CB Installments",
            "Excess Amount",
        ],
        "Instruments": [
            "Ticker Data",
            "Stock Screener",
            "Special Term",
            "Instrument Data",
            "Instrument Term",
        ],
        "Events": ["Event Calendar", "Event Stream", "Reverse Inquiry"],
        "Operations": ["Daily Procedure Check", "Operation Process"],
        "Orders": ["EMSX Order", "EMSX Route"],
    }

    @rx.var
    def current_subtabs(self) -> list[str]:
        """Returns the list of subtabs for the currently active module."""
        return self.MODULE_SUBTABS.get(self.active_module, [])

    @rx.var
    def active_subtab(self) -> str:
        """Returns the active subtab for the current module."""
        return self._active_subtabs.get(
            self.active_module, self.current_subtabs[0] if self.current_subtabs else ""
        )

    @rx.event
    def set_module(self, module_name: str):
        """Sets the active module."""
        self.active_module = module_name
        self.is_mobile_menu_open = False

    @rx.event
    def toggle_mobile_menu(self):
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def toggle_generate_menu(self):
        self.is_generate_menu_open = not self.is_generate_menu_open

    @rx.event
    def set_subtab(self, subtab_name: str):
        """Sets the active subtab for the CURRENT module."""
        self._active_subtabs[self.active_module] = subtab_name

    @rx.var
    def current_search_query(self) -> str:
        return self._filters.get(self.active_module, {}).get("search", "")

    @rx.var
    def current_date_filter(self) -> str:
        return self._filters.get(self.active_module, {}).get("date", "")

    @rx.var
    def current_auto_refresh(self) -> bool:
        return self._filters.get(self.active_module, {}).get("auto_refresh", False)

    @rx.event
    def set_current_search(self, value: str):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["search"] = value
        self.current_page = 1

    @rx.event
    def set_current_date(self, value: str):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["date"] = value

    @rx.event
    def toggle_auto_refresh(self, value: bool):
        if self.active_module not in self._filters:
            self._filters[self.active_module] = {}
        self._filters[self.active_module]["auto_refresh"] = value

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def toggle_top_movers(self):
        self.show_top_movers = not self.show_top_movers

    @rx.var
    def unread_count(self) -> int:
        return len([n for n in self.notifications if not n.get("read", False)])

    @rx.event
    def add_simulated_notification(self):
        import random
        from datetime import datetime

        types = ["alert", "warning", "info"]
        tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN", "NVDA", "AMD"]
        msgs = [
            "Price Target Reached",
            "Volume Spike Detected",
            "News Alert Released",
            "Analyst Rating Change",
            "Unusual Options Activity",
        ]
        new_note: NotificationItem = {
            "id": len(self.notifications) + random.randint(100, 999),
            "header": random.choice(msgs),
            "ticker": random.choice(tickers),
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "instruction": "Check details immediately",
            "type": random.choice(types),
            "read": False,
        }
        self.notifications.insert(0, new_note)
        if len(self.notifications) > 20:
            self.notifications = self.notifications[:20]

    @rx.event
    def dismiss_notification(self, id: int):
        """Removes a notification by ID."""
        self.notifications = [n for n in self.notifications if n["id"] != id]

    @rx.event
    def handle_generate(self, page_name: str):
        """Handle the generate action."""
        yield rx.toast(f"Generating report for {page_name}...", duration=2000)

    @rx.event
    async def refresh_prices(self):
        """Simulates refreshing market data for all PnL views."""
        self.is_loading = True
        yield
        try:
            self.pnl_change_data = _generate_pnl_change_data()
            self.pnl_summary_data = _generate_pnl_summary_data()
            self.pnl_currency_data = _generate_pnl_currency_data()
            yield rx.toast("Market data refreshed", position="bottom-right")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing portfolio dashboard prices: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def set_selected_row(self, row_id: int):
        self.selected_row_id = row_id

    current_page: int = 1
    page_size: int = 50
    page_size_options: list[int] = [25, 50, 100]
    _all_table_data: list[dict] = _generate_mock_data()
    pnl_change_data: list[PnLChangeItem] = _generate_pnl_change_data()
    pnl_summary_data: list[PnLSummaryItem] = _generate_pnl_summary_data()
    pnl_currency_data: list[PnLCurrencyItem] = _generate_pnl_currency_data()
    positions_data: list[PositionItem] = _generate_positions_data()
    stock_positions: list[StockPositionItem] = _generate_stock_positions()
    warrant_positions: list[WarrantPositionItem] = _generate_warrant_positions()
    bond_positions: list[BondPositionItem] = _generate_bond_positions()
    trade_summaries: list[TradeSummaryItem] = _generate_trade_summaries()
    _comp_data = _generate_compliance_data()
    restricted_list_data: list[RestrictedListItem] = _comp_data[0]
    undertakings_data: list[UndertakingItem] = _comp_data[1]
    beneficial_ownership_data: list[BeneficialOwnershipItem] = _comp_data[2]
    monthly_exercise_limit_data: list[MonthlyExerciseLimitItem] = _comp_data[3]
    _tools_data = _generate_tools_data()
    pth_data: list[PayToHoldItem] = _tools_data[0]
    short_ecl_data: list[ShortECLItem] = _tools_data[1]
    stock_borrow_data: list[StockBorrowItem] = _tools_data[2]
    po_settlement_data: list[POSettlementItem] = _tools_data[3]
    deal_indication_data: list[DealIndicationItem] = _tools_data[4]
    reset_dates_data: list[ResetDateItem] = _tools_data[5]
    coming_resets_data: list[ComingResetItem] = _tools_data[6]
    cb_installments_data: list[CBInstallmentItem] = _tools_data[7]
    excess_amount_data: list[ExcessAmountItem] = _tools_data[8]
    _recon_data = _generate_recon_data()
    pps_recon_data: list[PPSReconItem] = _recon_data[0]
    settlement_recon_data: list[SettlementReconItem] = _recon_data[1]
    failed_trades_data: list[FailedTradeItem] = _recon_data[2]
    pnl_recon_data: list[PnLReconItem] = _recon_data[3]
    risk_input_recon_data: list[RiskInputReconItem] = _recon_data[4]
    _ops_data = _generate_ops_data()
    daily_procedure_data: list[DailyProcedureItem] = _ops_data[0]
    operation_process_data: list[OperationProcessItem] = _ops_data[1]
    _mkt_data = _generate_market_data()
    market_data_list: list[MarketDataItem] = _mkt_data[0]
    fx_data_list: list[FXDataItem] = _mkt_data[1]
    historical_data_list: list[HistoricalDataItem] = _mkt_data[2]
    trading_calendar_list: list[TradingCalendarItem] = _mkt_data[3]
    market_hours_list: list[MarketHoursItem] = _mkt_data[4]
    event_calendar_list: list[EventCalendarItem] = _mkt_data[5]
    event_stream_list: list[EventStreamItem] = _mkt_data[6]
    reverse_inquiry_list: list[ReverseInquiryItem] = _mkt_data[7]
    _inst_data = _generate_instrument_data()
    ticker_data_list: list[TickerDataItem] = _inst_data[0]
    stock_screener_list: list[StockScreenerItem] = _inst_data[1]
    special_terms_list: list[SpecialTermItem] = _inst_data[2]
    instrument_data_list: list[InstrumentDataItem] = _inst_data[3]
    instrument_terms_list: list[InstrumentTermItem] = _inst_data[4]
    _risk_data = _generate_risk_data()
    delta_change_list: list[DeltaChangeItem] = _risk_data[0]
    risk_measures_list: list[RiskMeasureItem] = _risk_data[1]
    risk_inputs_list: list[RiskInputItem] = _risk_data[2]
    _emsa_data = _generate_emsa_data()
    emsa_orders_list: list[EMSAOrderItem] = _emsa_data[0]
    emsa_routes_list: list[EMSAOrderItem] = _emsa_data[1]

    @rx.var(cache=True)
    def filtered_positions(self) -> list[PositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.positions_data
        return [p for p in self.positions_data if query in p["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_stock_positions(self) -> list[StockPositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.stock_positions
        return [
            p
            for p in self.stock_positions
            if query in p["ticker"].lower() or query in p["sector"].lower()
        ]

    @rx.var(cache=True)
    def filtered_warrant_positions(self) -> list[WarrantPositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.warrant_positions
        return [
            p
            for p in self.warrant_positions
            if query in p["ticker"].lower() or query in p["underlying"].lower()
        ]

    @rx.var(cache=True)
    def filtered_bond_positions(self) -> list[BondPositionItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.bond_positions
        return [p for p in self.bond_positions if query in p["issuer"].lower()]

    @rx.var(cache=True)
    def filtered_trade_summaries(self) -> list[TradeSummaryItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.trade_summaries
        return [p for p in self.trade_summaries if query in p["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_pnl_change(self) -> list[PnLChangeItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pnl_change_data
        return [
            item
            for item in self.pnl_change_data
            if query in item["ticker"].lower() or query in item["underlying"].lower()
        ]

    @rx.var(cache=True)
    def filtered_pnl_summary(self) -> list[PnLSummaryItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pnl_summary_data
        return [
            item
            for item in self.pnl_summary_data
            if query in item["underlying"].lower() or query in item["currency"].lower()
        ]

    @rx.var(cache=True)
    def filtered_pnl_currency(self) -> list[PnLCurrencyItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pnl_currency_data
        return [
            item for item in self.pnl_currency_data if query in item["currency"].lower()
        ]

    @rx.var(cache=True)
    def filtered_restricted_list(self) -> list[RestrictedListItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.restricted_list_data
        return [i for i in self.restricted_list_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_undertakings(self) -> list[UndertakingItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.undertakings_data
        return [i for i in self.undertakings_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_beneficial_ownership(self) -> list[BeneficialOwnershipItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.beneficial_ownership_data
        return [
            i for i in self.beneficial_ownership_data if query in i["ticker"].lower()
        ]

    @rx.var(cache=True)
    def filtered_monthly_exercise_limit(self) -> list[MonthlyExerciseLimitItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.monthly_exercise_limit_data
        return [
            i for i in self.monthly_exercise_limit_data if query in i["ticker"].lower()
        ]

    @rx.var(cache=True)
    def filtered_pth(self) -> list[PayToHoldItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pth_data
        return [i for i in self.pth_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_short_ecl(self) -> list[ShortECLItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.short_ecl_data
        return [i for i in self.short_ecl_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_stock_borrow(self) -> list[StockBorrowItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.stock_borrow_data
        return [i for i in self.stock_borrow_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_po_settlement(self) -> list[POSettlementItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.po_settlement_data
        return [i for i in self.po_settlement_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_deal_indication(self) -> list[DealIndicationItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.deal_indication_data
        return [i for i in self.deal_indication_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_reset_dates(self) -> list[ResetDateItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.reset_dates_data
        return [i for i in self.reset_dates_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_coming_resets(self) -> list[ComingResetItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.coming_resets_data
        return [i for i in self.coming_resets_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_cb_installments(self) -> list[CBInstallmentItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.cb_installments_data
        return [i for i in self.cb_installments_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_excess_amount(self) -> list[ExcessAmountItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.excess_amount_data
        return [i for i in self.excess_amount_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_pps_recon(self) -> list[PPSReconItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pps_recon_data
        return [i for i in self.pps_recon_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_settlement_recon(self) -> list[SettlementReconItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.settlement_recon_data
        return [i for i in self.settlement_recon_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_failed_trades(self) -> list[FailedTradeItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.failed_trades_data
        return [i for i in self.failed_trades_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_pnl_recon(self) -> list[PnLReconItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.pnl_recon_data
        return [i for i in self.pnl_recon_data if query in i["underlying"].lower()]

    @rx.var(cache=True)
    def filtered_risk_input_recon(self) -> list[RiskInputReconItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.risk_input_recon_data
        return [i for i in self.risk_input_recon_data if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_daily_procedures(self) -> list[DailyProcedureItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.daily_procedure_data
        return [
            i for i in self.daily_procedure_data if query in i["procedure_name"].lower()
        ]

    @rx.var(cache=True)
    def filtered_operation_processes(self) -> list[OperationProcessItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.operation_process_data
        return [i for i in self.operation_process_data if query in i["process"].lower()]

    @rx.var(cache=True)
    def filtered_market_data(self) -> list[MarketDataItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.market_data_list
        return [i for i in self.market_data_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_fx_data(self) -> list[FXDataItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.fx_data_list
        return [i for i in self.fx_data_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_historical_data(self) -> list[HistoricalDataItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.historical_data_list
        return [i for i in self.historical_data_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_trading_calendar(self) -> list[TradingCalendarItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.trading_calendar_list
        return [
            i for i in self.trading_calendar_list if query in i["trade_date"].lower()
        ]

    @rx.var(cache=True)
    def filtered_market_hours(self) -> list[MarketHoursItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.market_hours_list
        return [i for i in self.market_hours_list if query in i["market"].lower()]

    @rx.var(cache=True)
    def filtered_event_calendar(self) -> list[EventCalendarItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.event_calendar_list
        return [i for i in self.event_calendar_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_event_stream(self) -> list[EventStreamItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.event_stream_list
        return [i for i in self.event_stream_list if query in i["symbol"].lower()]

    @rx.var(cache=True)
    def filtered_reverse_inquiry(self) -> list[ReverseInquiryItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.reverse_inquiry_list
        return [i for i in self.reverse_inquiry_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_ticker_data(self) -> list[TickerDataItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.ticker_data_list
        return [i for i in self.ticker_data_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_stock_screener(self) -> list[StockScreenerItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.stock_screener_list
        return [i for i in self.stock_screener_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_special_terms(self) -> list[SpecialTermItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.special_terms_list
        return [i for i in self.special_terms_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_instrument_data(self) -> list[InstrumentDataItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.instrument_data_list
        return [i for i in self.instrument_data_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_instrument_terms(self) -> list[InstrumentTermItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.instrument_terms_list
        return [i for i in self.instrument_terms_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_delta_change(self) -> list[DeltaChangeItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.delta_change_list
        return [i for i in self.delta_change_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_risk_measures(self) -> list[RiskMeasureItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.risk_measures_list
        return [i for i in self.risk_measures_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_risk_inputs(self) -> list[RiskInputItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.risk_inputs_list
        return [i for i in self.risk_inputs_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_emsa_orders(self) -> list[EMSAOrderItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.emsa_orders_list
        return [i for i in self.emsa_orders_list if query in i["ticker"].lower()]

    @rx.var(cache=True)
    def filtered_emsa_routes(self) -> list[EMSAOrderItem]:
        query = self.current_search_query.lower()
        if not query:
            return self.emsa_routes_list
        return [i for i in self.emsa_routes_list if query in i["ticker"].lower()]

    @rx.var
    def total_items(self) -> int:
        return len(self.filtered_table_data)

    @rx.var
    def total_pages(self) -> int:
        if self.total_items == 0:
            return 1
        return (self.total_items + self.page_size - 1) // self.page_size

    @rx.var(cache=True)
    def filtered_table_data(self) -> list[dict]:
        data = self._all_table_data
        query = self.current_search_query.lower()
        if not query:
            return data
        return [
            item
            for item in data
            if query in item["ticker"].lower() or query in item["description"].lower()
        ]

    @rx.var(cache=True)
    def paginated_table_data(self) -> list[dict]:
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.filtered_table_data[start:end]

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def set_page_size(self, size: str):
        self.page_size = int(size)
        self.current_page = 1