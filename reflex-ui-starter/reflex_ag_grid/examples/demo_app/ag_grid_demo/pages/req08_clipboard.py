"""
08 - Clipboard Page - Demonstrates copy cell with/without header.

Requirement 8: Copy cell / with header
AG Grid Feature: Clipboard API

Note: Uses processCellForClipboard to copy raw values without formatting.
Examples:
- Price: displays $155.30, copies 155.30
- Market Cap: displays $175mn, copies 175000000
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..components import nav_bar, status_badge


# Sample data with market cap for clipboard demo
CLIPBOARD_DATA = [
    {
        "symbol": "AAPL",
        "company": "Apple Inc.",
        "sector": "Technology",
        "price": 175.50,
        "market_cap": 2800000000000,
        "change": 2.5,
    },
    {
        "symbol": "GOOGL",
        "company": "Alphabet Inc.",
        "sector": "Technology",
        "price": 140.25,
        "market_cap": 1750000000000,
        "change": -1.2,
    },
    {
        "symbol": "MSFT",
        "company": "Microsoft Corp.",
        "sector": "Technology",
        "price": 378.91,
        "market_cap": 2810000000000,
        "change": 0.85,
    },
    {
        "symbol": "JPM",
        "company": "JPMorgan Chase",
        "sector": "Finance",
        "price": 195.00,
        "market_cap": 562000000000,
        "change": 1.3,
    },
    {
        "symbol": "GS",
        "company": "Goldman Sachs",
        "sector": "Finance",
        "price": 385.75,
        "market_cap": 125000000000,
        "change": -0.65,
    },
    {
        "symbol": "JNJ",
        "company": "Johnson & Johnson",
        "sector": "Healthcare",
        "price": 155.30,
        "market_cap": 375000000000,
        "change": 0.55,
    },
    {
        "symbol": "PFE",
        "company": "Pfizer Inc.",
        "sector": "Healthcare",
        "price": 28.50,
        "market_cap": 160000000000,
        "change": -2.1,
    },
    {
        "symbol": "XOM",
        "company": "Exxon Mobil",
        "sector": "Energy",
        "price": 105.20,
        "market_cap": 420000000000,
        "change": 3.2,
    },
]


def get_clipboard_columns():
    """Columns with currency formatting for clipboard demo.

    valueFormatter adds $ and abbreviations for display, but we configure AG Grid
    to copy raw values via processCellForClipboard.
    """
    return [
        ag_grid.column_def(
            field="symbol",
            header_name="Symbol",
            sortable=True,
            filter="agTextColumnFilter",
            width=100,
        ),
        ag_grid.column_def(field="company", header_name="Company", flex=1),
        ag_grid.column_def(
            field="sector", header_name="Sector", filter="agSetColumnFilter"
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            sortable=True,
            filter="agNumberColumnFilter",
            width=120,
            # Display with currency symbol: $175.50
            value_formatter=rx.Var(
                "(params) => params.value != null ? '$' + params.value.toFixed(2) : ''"
            ).to(rx.EventChain),
        ),
        ag_grid.column_def(
            field="market_cap",
            header_name="Market Cap",
            sortable=True,
            filter="agNumberColumnFilter",
            width=140,
            # Display with abbreviation: $175bn, $562mn
            value_formatter=rx.Var(
                """(params) => {
                    if (params.value == null) return '';
                    const val = params.value;
                    if (val >= 1e12) return '$' + (val / 1e12).toFixed(1) + 'tn';
                    if (val >= 1e9) return '$' + (val / 1e9).toFixed(0) + 'bn';
                    if (val >= 1e6) return '$' + (val / 1e6).toFixed(0) + 'mn';
                    return '$' + val.toLocaleString();
                }"""
            ).to(rx.EventChain),
        ),
        ag_grid.column_def(
            field="change",
            header_name="Change %",
            sortable=True,
            width=110,
            # Display with % symbol: 2.50%
            value_formatter=rx.Var(
                "(params) => params.value != null ? params.value.toFixed(2) + '%' : ''"
            ).to(rx.EventChain),
        ),
    ]


def clipboard_page() -> rx.Component:
    """Clipboard demo page.

    Features:
    - Copy single cell or range (Ctrl+C)
    - Currency formatted columns (display only)
    - Market Cap with abbreviations (bn/mn)
    - Raw values are copied (without $ or abbreviations)
    - Copy with headers
    - Context menu copy options
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("08 - Clipboard", size="6"),
        rx.text("Requirement 8: Copy cell / with header"),
        rx.callout(
            "Cells show formatted values but copy raw numbers. "
            "Market Cap shows '$175bn' but copies '175000000000'!",
            icon="info",
        ),
        rx.hstack(
            rx.text("Features:", weight="bold"),
            rx.badge("Currency Display", color_scheme="green"),
            rx.badge("Abbreviations", color_scheme="cyan"),
            rx.badge("Raw Copy", color_scheme="blue"),
            rx.badge("Ctrl+C", color_scheme="orange"),
            spacing="2",
        ),
        status_badge(),
        ag_grid(
            id="clipboard_grid",
            row_data=CLIPBOARD_DATA,
            column_defs=get_clipboard_columns(),
            row_selection="multiple",
            cell_selection=True,  # v35 API for range selection
            # Configure clipboard to copy raw values, not formatted values
            on_grid_ready=rx.Var(
                """(e) => {
                    e.api.setGridOption('processCellForClipboard', (params) => {
                        // Return raw value, not formatted value
                        return params.value;
                    });
                }"""
            ).to(rx.EventChain),
            on_selection_changed=DemoState.on_selection_change,
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.box(
            rx.heading("How It Works:", size="4"),
            rx.hstack(
                rx.vstack(
                    rx.text("Display:", weight="bold"),
                    rx.text("$175.50", color="green"),
                    rx.text("$2.8tn", color="green"),
                    rx.text("$562bn", color="green"),
                    rx.text("2.50%", color="green"),
                    align="start",
                ),
                rx.vstack(
                    rx.text("→", weight="bold"),
                    rx.text("→"),
                    rx.text("→"),
                    rx.text("→"),
                    rx.text("→"),
                ),
                rx.vstack(
                    rx.text("Clipboard:", weight="bold"),
                    rx.text("175.5", color="blue"),
                    rx.text("2800000000000", color="blue"),
                    rx.text("562000000000", color="blue"),
                    rx.text("2.5", color="blue"),
                    align="start",
                ),
                spacing="4",
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        rx.text(
            "Enterprise feature: Copy with headers, paste from Excel.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
