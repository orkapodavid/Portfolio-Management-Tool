import reflex as rx
from enum import StrEnum

NAV_BG = "#333333"
FINANCIAL_GREY = "#F0F0F0"
POSITIVE_GREEN = "#00A651"
NEGATIVE_RED = "#C00000"
ALERT_AMBER = "#FFC000"
ROW_HIGHLIGHT = "#FFF2CC"
BORDER_GREY = "#CCCCCC"
SIDEBAR_BG = "#F9F9F9"
NAV_HEIGHT = "40px"
KPI_HEIGHT = "28px"
MOVERS_ROW_HEIGHT = "22px"
MOVERS_EXPANDED_HEIGHT = "200px"
CONTROL_BAR_HEIGHT = "36px"
WORKSPACE_SUBTAB_HEIGHT = "28px"
WORKSPACE_GENERATE_BAR_HEIGHT = "40px"
TABLE_ROW_HEIGHT = "28px"
SIDEBAR_WIDTH = "220px"
DEFAULT_FONT = "Inter"
ICON_NAV_SIZE = 14
ICON_KPI_SIZE = 8
ICON_SIDEBAR_CLOSE = 14
ICON_ADD_ALERT = 12


# =============================================================================
# AG GRID ID REGISTRY
# =============================================================================


class GridId(StrEnum):
    """Enum of all AG Grid IDs in the application.
    
    Use these constants for notification navigation and grid targeting.
    """
    
    # Market Data
    MARKET_DATA = "market_data_grid"
    FX_DATA = "fx_data_grid"
    HISTORICAL_DATA = "historical_data_grid"
    TRADING_CALENDAR = "trading_calendar_grid"
    MARKET_HOURS = "market_hours_grid"
    
    # PnL
    PNL_CHANGE = "pnl_change_grid"
    PNL_SUMMARY = "pnl_summary_grid"
    PNL_CURRENCY = "pnl_currency_grid"
    PNL_FULL = "pnl_full_grid"
    
    # Positions
    POSITIONS = "positions_grid"
    STOCK_POSITION = "stock_position_grid"
    WARRANT_POSITION = "warrant_position_grid"
    BOND_POSITIONS = "bond_positions_grid"
    TRADE_SUMMARY = "trade_summary_grid"
    
    # Risk
    DELTA_CHANGE = "delta_change_grid"
    RISK_MEASURES = "risk_measures_grid"
    RISK_INPUTS = "risk_inputs_grid"
    
    # Reconciliation
    PPS_RECON = "pps_recon_grid"
    SETTLEMENT_RECON = "settlement_recon_grid"
    FAILED_TRADES = "failed_trades_grid"
    PNL_RECON = "pnl_recon_grid"
    RISK_INPUT_RECON = "risk_input_recon_grid"
    
    # Compliance
    RESTRICTED_LIST = "restricted_list_grid"
    UNDERTAKINGS = "undertakings_grid"
    BENEFICIAL_OWNERSHIP = "beneficial_ownership_grid"
    MONTHLY_EXERCISE_LIMIT = "monthly_exercise_limit_grid"
    
    # Portfolio Tools
    PAY_TO_HOLD = "pay_to_hold_grid"
    SHORT_ECL = "short_ecl_grid"
    STOCK_BORROW = "stock_borrow_grid"
    PO_SETTLEMENT = "po_settlement_grid"
    DEAL_INDICATION = "deal_indication_grid"
    RESET_DATES = "reset_dates_grid"
    COMING_RESETS = "coming_resets_grid"
    CB_INSTALLMENTS = "cb_installments_grid"
    EXCESS_AMOUNT = "excess_amount_grid"
    
    # Instruments
    TICKER_DATA = "ticker_data_grid"
    STOCK_SCREENER = "stock_screener_grid"
    SPECIAL_TERM = "special_term_grid"
    INSTRUMENT_DATA = "instrument_data_grid"
    INSTRUMENT_TERM = "instrument_term_grid"
    
    # Events
    EVENT_CALENDAR = "event_calendar_grid"
    EVENT_STREAM = "event_stream_grid"
    REVERSE_INQUIRY = "reverse_inquiry_grid"
    
    # Operations
    DAILY_PROCEDURE_CHECK = "daily_procedure_check_grid"
    OPERATION_PROCESS = "operation_process_grid"
    
    # Orders (EMSX)
    EMSX_ORDER = "emsx_order_grid"
    EMSX_ROUTE = "emsx_route_grid"


# Grid to route mapping for same-page detection
GRID_ROUTES = {
    GridId.MARKET_DATA: "/market-data/market-data",
    GridId.FX_DATA: "/market-data/fx-data",
    GridId.HISTORICAL_DATA: "/market-data/historical-data",
    GridId.TRADING_CALENDAR: "/market-data/trading-calendar",
    GridId.MARKET_HOURS: "/market-data/market-hours",
    GridId.PNL_CHANGE: "/pnl/pnl-change",
    GridId.PNL_SUMMARY: "/pnl/pnl-summary",
    GridId.PNL_CURRENCY: "/pnl/pnl-currency",
    GridId.PNL_FULL: "/pnl/pnl-full",
    GridId.POSITIONS: "/positions/positions",
    GridId.STOCK_POSITION: "/positions/stock-position",
    GridId.WARRANT_POSITION: "/positions/warrant-position",
    GridId.BOND_POSITIONS: "/positions/bond-positions",
    GridId.TRADE_SUMMARY: "/positions/trade-summary",
    GridId.DELTA_CHANGE: "/risk/delta-change",
    GridId.RISK_MEASURES: "/risk/risk-measures",
    GridId.RISK_INPUTS: "/risk/risk-inputs",
}


# Grid row ID configuration for notification navigation
# Each entry specifies the field(s) used to identify rows in that grid
# Supports single key (str) or composite keys (list[str])
GRID_ROW_ID_CONFIG: dict[str, str | list[str]] = {
    # Market Data - uses ticker
    GridId.MARKET_DATA: "ticker",
    GridId.FX_DATA: "ticker",
    GridId.HISTORICAL_DATA: "ticker",
    # PnL - various keys
    GridId.PNL_CHANGE: "ticker",
    GridId.PNL_FULL: "ticker",
    GridId.PNL_SUMMARY: "underlying",
    GridId.PNL_CURRENCY: "currency",
    # Positions - uses ticker
    GridId.POSITIONS: "ticker",
    GridId.STOCK_POSITION: "id",
    GridId.WARRANT_POSITION: "id",
    GridId.BOND_POSITIONS: "id",
    GridId.TRADE_SUMMARY: "id",
    # Risk - various keys
    GridId.DELTA_CHANGE: "ticker",
    GridId.RISK_MEASURES: "ticker",
    GridId.RISK_INPUTS: "seed",
    # Instruments - various keys
    GridId.TICKER_DATA: "ticker",
    GridId.STOCK_SCREENER: "ticker",
    GridId.INSTRUMENT_DATA: "deal_num",
    GridId.INSTRUMENT_TERM: "id",
    GridId.SPECIAL_TERM: "id",
    # Everything else defaults to "id"
}


def get_grid_row_id_key(grid_id: str) -> str | list[str]:
    """Get the row ID key(s) for a grid.
    
    Args:
        grid_id: The grid ID string (e.g., "market_data_grid")
        
    Returns:
        The field name(s) used for row identification. Defaults to "id".
    """
    return GRID_ROW_ID_CONFIG.get(grid_id, "id")