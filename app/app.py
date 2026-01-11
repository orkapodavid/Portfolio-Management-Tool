import reflex as rx
from app.components.shared.top_navigation import top_navigation
from app.components.shared.performance_header import performance_header
from app.components.shared.contextual_workspace import contextual_workspace
from app.components.shared.notification_sidebar import notification_sidebar
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState
from app.pages.portfolio.portfolio_page import portfolio_page
from app.pages.portfolio.watchlist_page import watchlist_page
from app.pages.research.research_page import research_page
from app.pages.reports.reports_page import reports_page
from app.pages.portfolio.goals_page import goals_page
from app.pages.user.profile_page import profile_page
from app.pages.notifications.notifications_page import notifications_page
from app.pages.user.settings_page import settings_page

# Import new states for on_load handlers
from app.states.pnl.pnl_state import PnLState
from app.states.positions.positions_state import PositionsState
from app.states.market_data.market_data_state import MarketDataState

# Import PnL Pages
from app.pages.pnl.pnl_change_page import pnl_change_page
from app.pages.pnl.pnl_summary_page import pnl_summary_page
from app.pages.pnl.pnl_currency_page import pnl_currency_page
from app.pages.pnl.pnl_full_page import pnl_full_page

# Import Positions Pages
from app.pages.positions.positions_page import positions_page
from app.pages.positions.stock_position_page import stock_position_page
from app.pages.positions.warrant_position_page import warrant_position_page
from app.pages.positions.bond_positions_page import bond_positions_page
from app.pages.positions.trade_summary_page import trade_summary_page

# Import Market Data Pages
from app.pages.market_data.market_data_page import market_data_page
from app.pages.market_data.fx_data_page import fx_data_page
from app.pages.market_data.historical_data_page import historical_data_page
from app.pages.market_data.trading_calendar_page import trading_calendar_page
from app.pages.market_data.market_hours_page import market_hours_page
from app.pages.market_data.ticker_data_page import ticker_data_page
from app.constants import FINANCIAL_GREY, DEFAULT_FONT

# Risk Pages
from app.pages.risk.delta_change_page import delta_change_page
from app.pages.risk.risk_measures_page import risk_measures_page
from app.pages.risk.risk_inputs_page import risk_inputs_page
from app.pages.risk.pricer_warrant_page import pricer_warrant_page
from app.pages.risk.pricer_bond_page import pricer_bond_page

# Recon Pages
from app.pages.reconciliation.pps_recon_page import pps_recon_page
from app.pages.reconciliation.settlement_recon_page import settlement_recon_page
from app.pages.reconciliation.failed_trades_page import failed_trades_page
from app.pages.reconciliation.pnl_recon_page import pnl_recon_page
from app.pages.reconciliation.risk_input_recon_page import risk_input_recon_page

# Compliance Pages
from app.pages.compliance.restricted_list_page import restricted_list_page
from app.pages.compliance.undertakings_page import undertakings_page
from app.pages.compliance.beneficial_ownership_page import beneficial_ownership_page
from app.pages.compliance.monthly_exercise_limit_page import monthly_exercise_limit_page

# Portfolio Tools Pages
from app.pages.portfolio_tools.pay_to_hold_page import pay_to_hold_page
from app.pages.portfolio_tools.short_ecl_page import short_ecl_page
from app.pages.portfolio_tools.stock_borrow_page import stock_borrow_page
from app.pages.portfolio_tools.po_settlement_page import po_settlement_page
from app.pages.portfolio_tools.deal_indication_page import deal_indication_page
from app.pages.portfolio_tools.reset_dates_page import reset_dates_page
from app.pages.portfolio_tools.coming_resets_page import coming_resets_page
from app.pages.portfolio_tools.cb_installments_page import cb_installments_page
from app.pages.portfolio_tools.excess_amount_page import excess_amount_page

# Instruments Pages
from app.pages.instruments.ticker_data_page import (
    ticker_data_page as inst_ticker_data_page,
)
from app.pages.instruments.stock_screener_page import stock_screener_page
from app.pages.instruments.special_term_page import special_term_page
from app.pages.instruments.instrument_data_page import instrument_data_page
from app.pages.instruments.instrument_term_page import instrument_term_page

# Events Pages
from app.pages.events.event_calendar_page import event_calendar_page
from app.pages.events.event_stream_page import event_stream_page
from app.pages.events.reverse_inquiry_page import reverse_inquiry_page

# Operations Pages
from app.pages.operations.daily_procedure_check_page import daily_procedure_check_page
from app.pages.operations.operation_process_page import operation_process_page

# Orders Pages
from app.pages.orders.emsx_order_page import emsx_order_page
from app.pages.orders.emsx_route_page import emsx_route_page


def index() -> rx.Component:
    return rx.el.div(
        top_navigation(),
        performance_header(),
        rx.el.div(
            contextual_workspace(),
            notification_sidebar(),
            class_name=f"flex flex-1 overflow-hidden min-h-0 bg-[{FINANCIAL_GREY}] w-full",
        ),
        class_name=f"flex flex-col h-screen w-screen bg-[{FINANCIAL_GREY}] font-['{DEFAULT_FONT}'] antialiased overflow-hidden",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="blue"),
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
)
app.add_page(index, route="/", on_load=PortfolioDashboardState.on_load)
app.add_page(portfolio_page, route="/portfolios")
app.add_page(watchlist_page, route="/watchlist")
app.add_page(research_page, route="/research")
app.add_page(reports_page, route="/reports")
app.add_page(goals_page, route="/goals")
app.add_page(profile_page, route="/profile")
app.add_page(notifications_page, route="/notifications")
app.add_page(settings_page, route="/settings")

# ================= Module Root Redirects =================
# ================= Module Root Redirects =================
# Mapping root routes directly to default subtab pages for cleaner experience
app.add_page(
    pnl_change_page,
    route="/pnl",
    on_load=[
        PnLState.load_pnl_change_data,
        lambda: PnLState.set_pnl_subtab("PnL Change"),
        lambda: PortfolioDashboardState.set_module("PnL"),
    ],
)
app.add_page(
    positions_page,
    route="/positions",
    on_load=[
        PositionsState.load_positions_data,
        lambda: PositionsState.set_positions_subtab("Positions"),
        lambda: PortfolioDashboardState.set_module("Positions"),
    ],
)
app.add_page(
    market_data_page,
    route="/market-data",
    on_load=[
        MarketDataState.load_market_data,
        lambda: MarketDataState.set_market_data_subtab("Market Data"),
        lambda: PortfolioDashboardState.set_module("Market Data"),
    ],
)

# ================= PnL Routes =================
app.add_page(
    pnl_change_page,
    route="/pnl/pnl-change",
    on_load=[
        PnLState.load_pnl_change_data,
        lambda: PnLState.set_pnl_subtab("PnL Change"),
        lambda: PortfolioDashboardState.set_module("PnL"),
    ],
)
app.add_page(
    pnl_summary_page,
    route="/pnl/pnl-summary",
    on_load=[
        PnLState.load_pnl_summary_data,
        lambda: PnLState.set_pnl_subtab("PnL Summary"),
        lambda: PortfolioDashboardState.set_module("PnL"),
    ],
)
app.add_page(
    pnl_currency_page,
    route="/pnl/pnl-currency",
    on_load=[
        PnLState.load_pnl_currency_data,
        lambda: PnLState.set_pnl_subtab("PnL Currency"),
        lambda: PortfolioDashboardState.set_module("PnL"),
    ],
)
app.add_page(
    pnl_full_page,
    route="/pnl/pnl-full",
    on_load=[
        PnLState.load_pnl_full_data,
        lambda: PnLState.set_pnl_subtab("PnL Full"),
        lambda: PortfolioDashboardState.set_module("PnL"),
    ],
)

# ================= Positions Routes =================
app.add_page(
    positions_page,
    route="/positions/positions",
    on_load=[
        PositionsState.load_positions_data,
        lambda: PositionsState.set_positions_subtab("Positions"),
        lambda: PortfolioDashboardState.set_module("Positions"),
    ],
)
app.add_page(
    stock_position_page,
    route="/positions/stock-position",
    on_load=[
        PositionsState.load_stock_positions_data,
        lambda: PositionsState.set_positions_subtab("Stock Position"),
        lambda: PortfolioDashboardState.set_module("Positions"),
    ],
)
app.add_page(
    warrant_position_page,
    route="/positions/warrant-position",
    on_load=[
        PositionsState.load_warrant_positions_data,
        lambda: PositionsState.set_positions_subtab("Warrant Position"),
        lambda: PortfolioDashboardState.set_module("Positions"),
    ],
)
app.add_page(
    bond_positions_page,
    route="/positions/bond-positions",
    on_load=[
        PositionsState.load_bond_positions_data,
        lambda: PositionsState.set_positions_subtab("Bond Positions"),
        lambda: PortfolioDashboardState.set_module("Positions"),
    ],
)
app.add_page(
    trade_summary_page,
    route="/positions/trade-summary",
    on_load=[
        PositionsState.load_trade_summary_data,
        lambda: PositionsState.set_positions_subtab("Trade Summary"),
        lambda: PortfolioDashboardState.set_module("Positions"),
    ],
)

# ================= Market Data Routes =================
app.add_page(
    market_data_page,
    route="/market-data/market-data",
    on_load=[
        MarketDataState.load_market_data,
        lambda: MarketDataState.set_market_data_subtab("Market Data"),
        lambda: PortfolioDashboardState.set_module("Market Data"),
    ],
)
app.add_page(
    fx_data_page,
    route="/market-data/fx-data",
    on_load=[
        MarketDataState.load_fx_data,
        lambda: MarketDataState.set_market_data_subtab("FX Data"),
        lambda: PortfolioDashboardState.set_module("Market Data"),
    ],
)
app.add_page(
    ticker_data_page,
    route="/market-data/reference-data",
    on_load=[
        MarketDataState.load_ticker_data,
        lambda: MarketDataState.set_market_data_subtab("Reference Data"),
        lambda: PortfolioDashboardState.set_module("Market Data"),
    ],
)
app.add_page(
    historical_data_page,
    route="/market-data/historical-data",
    on_load=[
        MarketDataState.load_historical_data,
        lambda: MarketDataState.set_market_data_subtab("Historical Data"),
        lambda: PortfolioDashboardState.set_module("Market Data"),
    ],
)
app.add_page(
    trading_calendar_page,
    route="/market-data/trading-calendar",
    on_load=[
        MarketDataState.load_trading_calendar,
        lambda: MarketDataState.set_market_data_subtab("Trading Calendar"),
        lambda: PortfolioDashboardState.set_module("Market Data"),
    ],
)
app.add_page(
    market_hours_page,
    route="/market-data/market-hours",
    on_load=[
        MarketDataState.load_market_hours,
        lambda: MarketDataState.set_market_data_subtab("Market Hours"),
        lambda: PortfolioDashboardState.set_module("Market Data"),
    ],
)

# ================= Risk Routes =================
app.add_page(
    delta_change_page,
    route="/risk",
    on_load=[
        PortfolioDashboardState.load_risk_data,
        lambda: PortfolioDashboardState.set_module("Risk"),
        lambda: PortfolioDashboardState.set_subtab("Delta Change"),
    ],
)
app.add_page(
    delta_change_page,
    route="/risk/delta-change",
    on_load=[
        PortfolioDashboardState.load_risk_data,
        lambda: PortfolioDashboardState.set_module("Risk"),
        lambda: PortfolioDashboardState.set_subtab("Delta Change"),
    ],
)
app.add_page(
    risk_measures_page,
    route="/risk/risk-measures",
    on_load=[
        PortfolioDashboardState.load_risk_data,
        lambda: PortfolioDashboardState.set_module("Risk"),
        lambda: PortfolioDashboardState.set_subtab("Risk Measures"),
    ],
)
app.add_page(
    risk_inputs_page,
    route="/risk/risk-inputs",
    on_load=[
        PortfolioDashboardState.load_risk_data,
        lambda: PortfolioDashboardState.set_module("Risk"),
        lambda: PortfolioDashboardState.set_subtab("Risk Inputs"),
    ],
)
app.add_page(
    pricer_warrant_page,
    route="/risk/pricer-warrant",
    on_load=[
        lambda: PortfolioDashboardState.set_module("Risk"),
        lambda: PortfolioDashboardState.set_subtab("Pricer Warrant"),
    ],
)
app.add_page(
    pricer_bond_page,
    route="/risk/pricer-bond",
    on_load=[
        lambda: PortfolioDashboardState.set_module("Risk"),
        lambda: PortfolioDashboardState.set_subtab("Pricer Bond"),
    ],
)

# ================= Recon Routes =================
app.add_page(
    pps_recon_page,
    route="/recon",
    on_load=[
        PortfolioDashboardState.load_reconciliation_data,
        lambda: PortfolioDashboardState.set_module("Recon"),
        lambda: PortfolioDashboardState.set_subtab("PPS Recon"),
    ],
)
app.add_page(
    pps_recon_page,
    route="/recon/pps-recon",
    on_load=[
        PortfolioDashboardState.load_reconciliation_data,
        lambda: PortfolioDashboardState.set_module("Recon"),
        lambda: PortfolioDashboardState.set_subtab("PPS Recon"),
    ],
)
app.add_page(
    settlement_recon_page,
    route="/recon/settlement-recon",
    on_load=[
        PortfolioDashboardState.load_reconciliation_data,
        lambda: PortfolioDashboardState.set_module("Recon"),
        lambda: PortfolioDashboardState.set_subtab("Settlement Recon"),
    ],
)
app.add_page(
    failed_trades_page,
    route="/recon/failed-trades",
    on_load=[
        PortfolioDashboardState.load_reconciliation_data,
        lambda: PortfolioDashboardState.set_module("Recon"),
        lambda: PortfolioDashboardState.set_subtab("Failed Trades"),
    ],
)
app.add_page(
    pnl_recon_page,
    route="/recon/pnl-recon",
    on_load=[
        PortfolioDashboardState.load_reconciliation_data,
        lambda: PortfolioDashboardState.set_module("Recon"),
        lambda: PortfolioDashboardState.set_subtab("PnL Recon"),
    ],
)
app.add_page(
    risk_input_recon_page,
    route="/recon/risk-input-recon",
    on_load=[
        PortfolioDashboardState.load_reconciliation_data,
        lambda: PortfolioDashboardState.set_module("Recon"),
        lambda: PortfolioDashboardState.set_subtab("Risk Input Recon"),
    ],
)

# ================= Compliance Routes =================
app.add_page(
    restricted_list_page,
    route="/compliance",
    on_load=[
        PortfolioDashboardState.load_compliance_data,
        lambda: PortfolioDashboardState.set_module("Compliance"),
        lambda: PortfolioDashboardState.set_subtab("Restricted List"),
    ],
)
app.add_page(
    restricted_list_page,
    route="/compliance/restricted-list",
    on_load=[
        PortfolioDashboardState.load_compliance_data,
        lambda: PortfolioDashboardState.set_module("Compliance"),
        lambda: PortfolioDashboardState.set_subtab("Restricted List"),
    ],
)
app.add_page(
    undertakings_page,
    route="/compliance/undertakings",
    on_load=[
        PortfolioDashboardState.load_compliance_data,
        lambda: PortfolioDashboardState.set_module("Compliance"),
        lambda: PortfolioDashboardState.set_subtab("Undertakings"),
    ],
)
app.add_page(
    beneficial_ownership_page,
    route="/compliance/beneficial-ownership",
    on_load=[
        PortfolioDashboardState.load_compliance_data,
        lambda: PortfolioDashboardState.set_module("Compliance"),
        lambda: PortfolioDashboardState.set_subtab("Beneficial Ownership"),
    ],
)
app.add_page(
    monthly_exercise_limit_page,
    route="/compliance/monthly-exercise-limit",
    on_load=[
        PortfolioDashboardState.load_compliance_data,
        lambda: PortfolioDashboardState.set_module("Compliance"),
        lambda: PortfolioDashboardState.set_subtab("Monthly Exercise Limit"),
    ],
)

# ================= Portfolio Tools Routes =================
app.add_page(
    pay_to_hold_page,
    route="/portfolio-tools",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Pay-To-Hold"),
    ],
)
app.add_page(
    pay_to_hold_page,
    route="/portfolio-tools/pay-to-hold",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Pay-To-Hold"),
    ],
)
app.add_page(
    short_ecl_page,
    route="/portfolio-tools/short-ecl",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Short ECL"),
    ],
)
app.add_page(
    stock_borrow_page,
    route="/portfolio-tools/stock-borrow",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Stock Borrow"),
    ],
)
app.add_page(
    po_settlement_page,
    route="/portfolio-tools/po-settlement",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("PO Settlement"),
    ],
)
app.add_page(
    deal_indication_page,
    route="/portfolio-tools/deal-indication",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Deal Indication"),
    ],
)
app.add_page(
    reset_dates_page,
    route="/portfolio-tools/reset-dates",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Reset Dates"),
    ],
)
app.add_page(
    coming_resets_page,
    route="/portfolio-tools/coming-resets",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Coming Resets"),
    ],
)
app.add_page(
    cb_installments_page,
    route="/portfolio-tools/cb-installments",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("CB Installments"),
    ],
)
app.add_page(
    excess_amount_page,
    route="/portfolio-tools/excess-amount",
    on_load=[
        PortfolioDashboardState.load_portfolio_tools_data,
        lambda: PortfolioDashboardState.set_module("Portfolio Tools"),
        lambda: PortfolioDashboardState.set_subtab("Excess Amount"),
    ],
)

# ================= Instruments Routes =================
app.add_page(
    inst_ticker_data_page,
    route="/instruments",
    on_load=[
        PortfolioDashboardState.load_instruments_data,
        lambda: PortfolioDashboardState.set_module("Instruments"),
        lambda: PortfolioDashboardState.set_subtab("Ticker Data"),
    ],
)
app.add_page(
    inst_ticker_data_page,
    route="/instruments/ticker-data",
    on_load=[
        PortfolioDashboardState.load_instruments_data,
        lambda: PortfolioDashboardState.set_module("Instruments"),
        lambda: PortfolioDashboardState.set_subtab("Ticker Data"),
    ],
)
app.add_page(
    stock_screener_page,
    route="/instruments/stock-screener",
    on_load=[
        PortfolioDashboardState.load_instruments_data,
        lambda: PortfolioDashboardState.set_module("Instruments"),
        lambda: PortfolioDashboardState.set_subtab("Stock Screener"),
    ],
)
app.add_page(
    special_term_page,
    route="/instruments/special-term",
    on_load=[
        PortfolioDashboardState.load_instruments_data,
        lambda: PortfolioDashboardState.set_module("Instruments"),
        lambda: PortfolioDashboardState.set_subtab("Special Term"),
    ],
)
app.add_page(
    instrument_data_page,
    route="/instruments/instrument-data",
    on_load=[
        PortfolioDashboardState.load_instruments_data,
        lambda: PortfolioDashboardState.set_module("Instruments"),
        lambda: PortfolioDashboardState.set_subtab("Instrument Data"),
    ],
)
app.add_page(
    instrument_term_page,
    route="/instruments/instrument-term",
    on_load=[
        PortfolioDashboardState.load_instruments_data,
        lambda: PortfolioDashboardState.set_module("Instruments"),
        lambda: PortfolioDashboardState.set_subtab("Instrument Term"),
    ],
)

# ================= Events Routes =================
app.add_page(
    event_calendar_page,
    route="/events",
    on_load=[
        PortfolioDashboardState.load_events_data,
        lambda: PortfolioDashboardState.set_module("Events"),
        lambda: PortfolioDashboardState.set_subtab("Event Calendar"),
    ],
)
app.add_page(
    event_calendar_page,
    route="/events/event-calendar",
    on_load=[
        PortfolioDashboardState.load_events_data,
        lambda: PortfolioDashboardState.set_module("Events"),
        lambda: PortfolioDashboardState.set_subtab("Event Calendar"),
    ],
)
app.add_page(
    event_stream_page,
    route="/events/event-stream",
    on_load=[
        PortfolioDashboardState.load_events_data,
        lambda: PortfolioDashboardState.set_module("Events"),
        lambda: PortfolioDashboardState.set_subtab("Event Stream"),
    ],
)
app.add_page(
    reverse_inquiry_page,
    route="/events/reverse-inquiry",
    on_load=[
        PortfolioDashboardState.load_events_data,
        lambda: PortfolioDashboardState.set_module("Events"),
        lambda: PortfolioDashboardState.set_subtab("Reverse Inquiry"),
    ],
)

# ================= Operations Routes =================
app.add_page(
    daily_procedure_check_page,
    route="/operations",
    on_load=[
        PortfolioDashboardState.load_operations_data,
        lambda: PortfolioDashboardState.set_module("Operations"),
        lambda: PortfolioDashboardState.set_subtab("Daily Procedure Check"),
    ],
)
app.add_page(
    daily_procedure_check_page,
    route="/operations/daily-procedure-check",
    on_load=[
        PortfolioDashboardState.load_operations_data,
        lambda: PortfolioDashboardState.set_module("Operations"),
        lambda: PortfolioDashboardState.set_subtab("Daily Procedure Check"),
    ],
)
app.add_page(
    operation_process_page,
    route="/operations/operation-process",
    on_load=[
        PortfolioDashboardState.load_operations_data,
        lambda: PortfolioDashboardState.set_module("Operations"),
        lambda: PortfolioDashboardState.set_subtab("Operation Process"),
    ],
)

# ================= Orders Routes =================
app.add_page(
    emsx_order_page,
    route="/orders",
    on_load=[
        PortfolioDashboardState.load_emsa_data,
        lambda: PortfolioDashboardState.set_module("Orders"),
        lambda: PortfolioDashboardState.set_subtab("EMSX Order"),
    ],
)
app.add_page(
    emsx_order_page,
    route="/orders/emsx-order",
    on_load=[
        PortfolioDashboardState.load_emsa_data,
        lambda: PortfolioDashboardState.set_module("Orders"),
        lambda: PortfolioDashboardState.set_subtab("EMSX Order"),
    ],
)
app.add_page(
    emsx_route_page,
    route="/orders/emsx-route",
    on_load=[
        PortfolioDashboardState.load_emsa_data,
        lambda: PortfolioDashboardState.set_module("Orders"),
        lambda: PortfolioDashboardState.set_subtab("EMSX Route"),
    ],
)
