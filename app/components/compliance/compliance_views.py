import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState
from app.states.dashboard.portfolio_dashboard_types import (
    RestrictedListItem,
    UndertakingItem,
    BeneficialOwnershipItem,
    MonthlyExerciseLimitItem,
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


def restricted_row(item: RestrictedListItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["in_emdx"]),
        text_cell(item["compliance_type"]),
        text_cell(item["firm_block"]),
        text_cell(item["compliance_start"]),
        text_cell(item["nda_end"]),
        text_cell(item["mnpi_end"]),
        text_cell(item["wc_end"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def restricted_list_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("In EMDX?"),
                    header_cell("Compliance Type"),
                    header_cell("Firm_Block"),
                    header_cell("Compliance Start"),
                    header_cell("NDA End"),
                    header_cell("MNPI End"),
                    header_cell("WC End"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_restricted_list, restricted_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def undertaking_row(item: UndertakingItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["deal_num"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["account"]),
        text_cell(item["undertaking_expiry"]),
        text_cell(item["undertaking_type"]),
        text_cell(item["undertaking_details"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def undertakings_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Account"),
                    header_cell("Undertaking Expiry"),
                    header_cell("Undertaking Type"),
                    header_cell("Undertaking Details"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_undertakings, undertaking_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def ownership_row(item: BeneficialOwnershipItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["nosh_reported"]),
        text_cell(item["nosh_bbg"]),
        text_cell(item["nosh_proforma"]),
        text_cell(item["stock_shares"]),
        text_cell(item["warrant_shares"]),
        text_cell(item["bond_shares"]),
        text_cell(item["total_shares"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def beneficial_ownership_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("NOSH (Reported)"),
                    header_cell("NOSH (BBG)"),
                    header_cell("NOSH Proforma"),
                    header_cell("Stock Shares"),
                    header_cell("Warrant Shares"),
                    header_cell("Bond Shares"),
                    header_cell("Total Shares"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_beneficial_ownership, ownership_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def limit_row(item: MonthlyExerciseLimitItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["sec_type"]),
        text_cell(item["original_nosh"]),
        text_cell(item["original_quantity"]),
        text_cell(item["monthly_exercised_quantity"]),
        text_cell(item["monthly_exercised_pct"]),
        text_cell(item["monthly_sal"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def monthly_exercise_limit_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Sec Type"),
                    header_cell("Original Nosh"),
                    header_cell("Original Quantity"),
                    header_cell("Monthly Exercised Quantity"),
                    header_cell("Monthly Exercised %"),
                    header_cell("Monthly Sal"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_monthly_exercise_limit, limit_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )