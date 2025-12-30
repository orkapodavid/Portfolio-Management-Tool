import reflex as rx
from app.states.portfolio_dashboard_state import (
    PortfolioDashboardState,
    PayToHoldItem,
    ShortECLItem,
    StockBorrowItem,
    POSettlementItem,
    DealIndicationItem,
    ResetDateItem,
    ComingResetItem,
    CBInstallmentItem,
    ExcessAmountItem,
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


def pth_row(item: PayToHoldItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["ticker"]),
        text_cell(item["currency"]),
        text_cell(item["counter_party"]),
        text_cell(item["side"]),
        text_cell(item["sl_rate"]),
        text_cell(item["pth_amount_sod"]),
        text_cell(item["pth_amount"]),
        text_cell(item["emsa_order"]),
        text_cell(item["emsa_remark"]),
        text_cell(item["emsa_working"]),
        text_cell(item["emsa_order_col"]),
        text_cell(item["emsa_filled"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def pay_to_hold_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("Ticker"),
                    header_cell("Currency"),
                    header_cell("Counter Party"),
                    header_cell("Side"),
                    header_cell("SL Rate"),
                    header_cell("PTH Amount SOD"),
                    header_cell("PTH Amount"),
                    header_cell("EMSA Order"),
                    header_cell("EMSA Order Remark"),
                    header_cell("EMSA Working"),
                    header_cell("EMSA order"),
                    header_cell("EMSA order Filled"),
                )
            ),
            rx.el.tbody(rx.foreach(PortfolioDashboardState.filtered_pth, pth_row)),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def ecl_row(item: ShortECLItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["pos_loc"]),
        text_cell(item["account"]),
        text_cell(item["short_position"]),
        text_cell(item["nosh"]),
        text_cell(item["short_ownership"]),
        text_cell(item["last_volume"]),
        text_cell(item["short_pos_truncated"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def short_ecl_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Pos Loc"),
                    header_cell("Account"),
                    header_cell("Short Position"),
                    header_cell("NOSH"),
                    header_cell("Short Ownership"),
                    header_cell("Last Volume"),
                    header_cell("ShortPos/(truncated)"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_short_ecl, ecl_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def borrow_row(item: StockBorrowItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["jpm_req"]),
        text_cell(item["jpm_firm"]),
        text_cell(item["borrow_rate"]),
        text_cell(item["bofa_req"]),
        text_cell(item["bofa_firm"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def stock_borrow_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("JPM Request Locate"),
                    header_cell("JPM Firm Locate"),
                    header_cell("Borrow Rate"),
                    header_cell("BofA Request Locate"),
                    header_cell("BofA Firm Locate"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_stock_borrow, borrow_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def settlement_row(item: POSettlementItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["deal_num"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["structure"]),
        text_cell(item["currency"]),
        text_cell(item["fx_rate"]),
        text_cell(item["last_price"]),
        text_cell(item["current_position"]),
        text_cell(item["shares_allocated"]),
        text_cell(item["shares_swap"]),
        text_cell(item["shares_hedged"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def po_settlement_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Structure"),
                    header_cell("Currency"),
                    header_cell("FX Rate"),
                    header_cell("Last Price"),
                    header_cell("Current Position"),
                    header_cell("Shares Allocated"),
                    header_cell("Shares in Swap"),
                    header_cell("Shares Hedged"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_po_settlement, settlement_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def deal_row(item: DealIndicationItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["identification"]),
        text_cell(item["deal_type"]),
        text_cell(item["agent"]),
        text_cell(item["captain"]),
        text_cell(item["indication_date"]),
        text_cell(item["currency"]),
        text_cell(item["market_cap_loc"]),
        text_cell(item["gross_proceed_loc"]),
        text_cell(item["indication_amount"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def deal_indication_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Identification"),
                    header_cell("Deal Type"),
                    header_cell("Agent"),
                    header_cell("Deal Captain"),
                    header_cell("Indication Date"),
                    header_cell("Currency"),
                    header_cell("Market Cap LOC"),
                    header_cell("Gross Proceed LOC"),
                    header_cell("Indication Amount"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_deal_indication, deal_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def reset_row(item: ResetDateItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["sec_type"]),
        text_cell(item["currency"]),
        text_cell(item["trade_date"]),
        text_cell(item["first_reset"]),
        text_cell(item["expiry"]),
        text_cell(item["latest_reset"]),
        text_cell(item["reset_up_down"]),
        text_cell(item["market_price"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def reset_dates_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Sec Type"),
                    header_cell("Currency"),
                    header_cell("Trade Date"),
                    header_cell("First Reset Date"),
                    header_cell("Expiry Date"),
                    header_cell("Latest Reset Date"),
                    header_cell("Reset Up/Down"),
                    header_cell("Market Price"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_reset_dates, reset_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def coming_row(item: ComingResetItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["deal_num"]),
        text_cell(item["detail_id"]),
        text_cell(item["ticker"]),
        text_cell(item["account"]),
        text_cell(item["company_name"]),
        text_cell(item["announce_date"]),
        text_cell(item["closing_date"]),
        text_cell(item["cal_days"]),
        text_cell(item["biz_days"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def coming_resets_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num"),
                    header_cell("Detail ID"),
                    header_cell("Ticker"),
                    header_cell("Account"),
                    header_cell("Company Name"),
                    header_cell("Announcement Date"),
                    header_cell("Closing Date"),
                    header_cell("Cal Days Since Announced"),
                    header_cell("Biz Days Since Announced"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_coming_resets, coming_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def cb_row(item: CBInstallmentItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["currency"]),
        text_cell(item["installment_date"]),
        text_cell(item["total_amount"]),
        text_cell(item["outstanding"]),
        text_cell(item["redeemed"]),
        text_cell(item["deferred"]),
        text_cell(item["converted"]),
        text_cell(item["installment_amount"]),
        text_cell(item["period"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def cb_installments_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Currency"),
                    header_cell("Installment Date"),
                    header_cell("Total Amount"),
                    header_cell("Outstanding Amount"),
                    header_cell("Redeemed Amount"),
                    header_cell("Deferred Amount"),
                    header_cell("Converted Amount"),
                    header_cell("Installment Amount"),
                    header_cell("Period"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_cb_installments, cb_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def excess_row(item: ExcessAmountItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["deal_num"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["warrants"]),
        text_cell(item["excess_amount"]),
        text_cell(item["threshold"]),
        text_cell(item["cb_redeem"]),
        text_cell(item["redeem"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def excess_amount_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Warrants"),
                    header_cell("Excess Amount"),
                    header_cell("Excess Amount Threshold"),
                    header_cell("CB Redeem/Converted Amt"),
                    header_cell("Redeem/Converted Amt"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_excess_amount, excess_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )