import reflex as rx
from app.states.risk.risk_state import RiskState
from app.states.risk.types import (
    DeltaChangeItem,
    RiskMeasureItem,
    RiskInputItem,
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


def delta_row(item: DeltaChangeItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["structure"]),
        text_cell(item["currency"]),
        text_cell(item["fx_rate"]),
        text_cell(item["current_price"]),
        text_cell(item["valuation_price"]),
        text_cell(item["pos_delta"]),
        text_cell(item["pos_delta_small"]),
        text_cell(item["pos_g"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def delta_change_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Structure"),
                    header_cell("Currency"),
                    header_cell("FX Rate"),
                    header_cell("Current Price"),
                    header_cell("Valuation Price"),
                    header_cell("POS DELTA"),
                    header_cell("POS DELTA SMALL"),
                    header_cell("Pos G"),
                )
            ),
            rx.el.tbody(rx.foreach(RiskState.filtered_delta_changes, delta_row)),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def risk_measure_row(item: RiskMeasureItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["seed"]),
        text_cell(item["simulation_num"]),
        text_cell(item["trial_num"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["sec_type"]),
        text_cell(item["is_private"]),
        text_cell(item["national"]),
        text_cell(item["national_used"]),
        text_cell(item["national_current"]),
        text_cell(item["currency"]),
        text_cell(item["fx_rate"]),
        text_cell(item["spot_price"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def risk_measures_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Seed"),
                    header_cell("Simulation#"),
                    header_cell("Trial#"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Sec Type"),
                    header_cell("Is Private"),
                    header_cell("National"),
                    header_cell("National Used"),
                    header_cell("National Current"),
                    header_cell("Currency"),
                    header_cell("FX Rate"),
                    header_cell("Spot Price"),
                )
            ),
            rx.el.tbody(rx.foreach(RiskState.filtered_risk_measures, risk_measure_row)),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def risk_inputs_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Seed"),
                    header_cell("Simulation#"),
                    header_cell("Trial#"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Sec Type"),
                    header_cell("Is Private"),
                    header_cell("National"),
                    header_cell("National Used"),
                    header_cell("National Current"),
                    header_cell("Currency"),
                    header_cell("FX Rate"),
                    header_cell("Spot Price"),
                )
            ),
            rx.el.tbody(rx.foreach(RiskState.filtered_risk_inputs, risk_measure_row)),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def pricer_warrant_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Terms", class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Valuation Date", class_name="font-bold block mb-1"),
                    rx.el.input(
                        type="date", class_name="border rounded p-1 w-full text-xs"
                    ),
                ),
                rx.el.div(
                    rx.el.label("Effective Date", class_name="font-bold block mb-1"),
                    rx.el.input(
                        type="date", class_name="border rounded p-1 w-full text-xs"
                    ),
                ),
                rx.el.div(
                    rx.el.label("Maturity Date", class_name="font-bold block mb-1"),
                    rx.el.input(
                        type="date", class_name="border rounded p-1 w-full text-xs"
                    ),
                ),
                rx.el.div(
                    rx.el.label("Underlying", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                rx.el.div(
                    rx.el.label("Maturity Ticker", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                rx.el.div(
                    rx.el.label("Spot Price", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                rx.el.div(
                    rx.el.label("Strike Price", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                rx.el.div(
                    rx.el.label("Hit Fee Dec", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                rx.el.div(
                    rx.el.label("Currency", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                rx.el.div(
                    rx.el.label("Hit Rate", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                rx.el.div(
                    rx.el.label("Interest Rate", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                class_name="grid grid-cols-2 gap-4 text-xs",
            ),
            class_name="w-1/3 p-4 border-r border-gray-200 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.h3(
                "Simulations & Outputs",
                class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(header_cell("Simulation#"), header_cell("Jump to 0"))
                    ),
                    rx.el.tbody(rx.el.tr(text_cell("1"), text_cell("No"))),
                    class_name="w-full table-auto border-separate border-spacing-0 mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span("Fair Value:", class_name="font-bold mr-2"),
                        rx.el.span("$45.20", class_name="font-mono text-green-600"),
                        class_name="text-lg mb-2",
                    ),
                    rx.el.div(
                        rx.el.span("Delta:", class_name="font-bold mr-2"),
                        rx.el.span("0.65", class_name="font-mono text-gray-700"),
                        class_name="text-md",
                    ),
                    class_name="p-4 bg-gray-50 rounded border border-gray-200",
                ),
                class_name="flex flex-col gap-4",
            ),
            class_name="flex-1 p-4",
        ),
        class_name="flex w-full h-full bg-white",
    )


def pricer_bond_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Terms", class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Valuation Date", class_name="font-bold block mb-1"),
                    rx.el.input(
                        type="date", class_name="border rounded p-1 w-full text-xs"
                    ),
                ),
                rx.el.div(
                    rx.el.label("Coupon Rate", class_name="font-bold block mb-1"),
                    rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                ),
                class_name="grid grid-cols-1 gap-4 text-xs",
            ),
            class_name="w-1/3 p-4 border-r border-gray-200 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.h3(
                "Pricing Results",
                class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded",
            ),
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        header_cell("Ticker"),
                        header_cell("Spot Price"),
                        header_cell("Fair Value"),
                        header_cell("Discount"),
                    )
                ),
                rx.el.tbody(
                    rx.el.tr(
                        text_cell("AAPL 4.5% 2029"),
                        text_cell("98.50"),
                        text_cell("99.25"),
                        text_cell("0.75%"),
                    )
                ),
                class_name="w-full table-auto border-separate border-spacing-0",
            ),
            class_name="flex-1 p-4",
        ),
        class_name="flex w-full h-full bg-white",
    )
