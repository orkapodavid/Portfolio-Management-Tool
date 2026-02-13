"""
09 - Excel Export Page - Demonstrates Excel/CSV export.

Requirement 9: Export Excel
AG Grid Feature: exportDataAsExcel()
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


# JavaScript to access grid API
GET_API_JS = """(function() {
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) return null;
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) return null;
    let fiber = wrapper[key];
    while (fiber) {
        if (fiber.stateNode && fiber.stateNode.api) return fiber.stateNode.api;
        fiber = fiber.return;
    }
    return null;
})()"""


def excel_export_page() -> rx.Component:
    """Excel Export demo page.

    Features:
    - Export to Excel (.xlsx)
    - Export to CSV
    - Export selected rows only
    - Custom export filename
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("09 - Excel Export", size="6"),
        rx.text("Requirement 9: Export Excel"),
        rx.callout(
            "Click the export buttons to download data as Excel or CSV.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "📥 Export Excel",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "if (api) { api.exportDataAsExcel(); } "
                    "else { alert('Grid API not ready'); }"
                ),
                color_scheme="green",
            ),
            rx.button(
                "📄 Export CSV",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "if (api) { api.exportDataAsCsv(); } "
                    "else { alert('Grid API not ready'); }"
                ),
                color_scheme="blue",
            ),
            rx.button(
                "📋 Export Selected",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "if (api) { api.exportDataAsCsv({onlySelected: true}); } "
                    "else { alert('Grid API not ready'); }"
                ),
                color_scheme="purple",
            ),
        ),
        status_badge(),
        ag_grid(
            id="excel_export_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_selection="multiple",
            on_selection_changed=DemoState.on_selection_change,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Excel export is Enterprise. CSV export is Community.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
