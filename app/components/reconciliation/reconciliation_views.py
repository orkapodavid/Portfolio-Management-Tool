import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import (
    PortfolioDashboardState,
    PPSReconItem,
    SettlementReconItem,
    FailedTradeItem,
    PnLReconItem,
    RiskInputReconItem,
)


def header_cell(text: str, align: str = "left") -> rx.Component:
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 text-{align} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap",
    )


def text_cell(val: str) -> rx.Component:
    return rx.el.td(
        val,
        class_name="px-3 py-2 text-[10px] font-medium text-gray-700 border-b border-gray-200 align-middle whitespace-nowrap",
    )


def pps_row(item: PPSReconItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["value_date"]),
        text_cell(item["trade_date"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["code"]),
        text_cell(item["company_name"]),
        text_cell(item["sec_type"]),
        text_cell(item["pos_loc"]),
        text_cell(item["account"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def pps_recon_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Value Date"),
                    header_cell("Trade Date"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Code"),
                    header_cell("Company Name"),
                    header_cell("Sec Type"),
                    header_cell("Pos Loc"),
                    header_cell("Account"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_pps_recon, pps_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def settle_row(item: SettlementReconItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["ml_report_date"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["pos_loc"]),
        text_cell(item["currency"]),
        text_cell(item["sec_type"]),
        text_cell(item["position_settled"]),
        text_cell(item["ml_inventory"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def settlement_recon_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("ML Report Date"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Pos Loc"),
                    header_cell("Currency"),
                    header_cell("Sec Type"),
                    header_cell("Position Settled"),
                    header_cell("ML Inventory"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_settlement_recon, settle_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def failed_row(item: FailedTradeItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["report_date"]),
        text_cell(item["trade_date"]),
        text_cell(item["value_date"]),
        text_cell(item["settlement_date"]),
        text_cell(item["portfolio_code"]),
        text_cell(item["instrument_ref"]),
        text_cell(item["instrument_name"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["isin"]),
        text_cell(item["sedol"]),
        text_cell(item["broker"]),
        text_cell(item["glass_reference"]),
        text_cell(item["trade_reference"]),
        text_cell(item["deal_type"]),
        text_cell(item["q"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def failed_trades_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Report Date"),
                    header_cell("Trade Date"),
                    header_cell("Value Date"),
                    header_cell("Settlement Date"),
                    header_cell("Portfolio Code"),
                    header_cell("Instrument Ref"),
                    header_cell("Instrument Name"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("ISIN"),
                    header_cell("SEDOL"),
                    header_cell("Broker"),
                    header_cell("Glass Reference"),
                    header_cell("Trade Reference"),
                    header_cell("Deal Type"),
                    header_cell("Q"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_failed_trades, failed_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def pnl_recon_row(item: PnLReconItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["report_date"]),
        text_cell(item["deal_num"]),
        text_cell(item["row_index"]),
        text_cell(item["underlying"]),
        text_cell(item["pos_loc"]),
        text_cell(item["stock_sec_id"]),
        text_cell(item["warrant_sec_id"]),
        text_cell(item["bond_sec_id"]),
        text_cell(item["stock_position"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def pnl_recon_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("Report Date"),
                    header_cell("Deal Num"),
                    header_cell("Row Index"),
                    header_cell("Underlying"),
                    header_cell("Pos Loc"),
                    header_cell("Stock SecID"),
                    header_cell("Warrant SecID"),
                    header_cell("Bond SecID"),
                    header_cell("Stock Position"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_pnl_recon, pnl_recon_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def risk_recon_row(item: RiskInputReconItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["value_date"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["sec_type"]),
        text_cell(item["spot_mc"]),
        text_cell(item["spot_ppd"]),
        text_cell(item["position"]),
        text_cell(item["value_mc"]),
        text_cell(item["value_ppd"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def risk_input_recon_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Value Date"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Sec Type"),
                    header_cell("Spot (MC)"),
                    header_cell("Spot (PPD)"),
                    header_cell("Position"),
                    header_cell("Value (MC)"),
                    header_cell("Value (PPD)"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_risk_input_recon, risk_recon_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )