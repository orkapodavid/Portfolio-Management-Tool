"""
22 - Advanced Filter Page - Demonstrates the AG Grid Enterprise Advanced Filter.

Requirement 22: Advanced Filter (Enterprise)
AG Grid Feature: enableAdvancedFilter, advancedFilterModel, advancedFilterParams
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


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


def advanced_filter_page() -> rx.Component:
    """Advanced Filter demo page.

    Features:
    - Enterprise Advanced Filter builder UI
    - Complex filter expressions with AND/OR logic
    - Save and restore filter state
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("22 - Advanced Filter", size="6"),
        rx.text("Requirement 22: AG Grid Enterprise Advanced Filter"),
        rx.callout(
            "Click the filter icon in any column header to open the Advanced Filter builder. "
            "Create complex filter expressions with AND/OR logic.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "🔍 Show Filter Builder",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "if (api) { api.showAdvancedFilterBuilder(); } "
                    "else { alert('Grid API not ready'); }"
                ),
                color_scheme="blue",
            ),
            rx.button(
                "🗑️ Clear Filters",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "if (api) { api.setAdvancedFilterModel(null); } "
                    "else { alert('Grid API not ready'); }"
                ),
                color_scheme="gray",
            ),
            spacing="3",
        ),
        ag_grid(
            id="advanced_filter_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            enable_advanced_filter=True,
            side_bar=True,  # Shows filter panel in sidebar
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.text(
            "Enterprise feature: enableAdvancedFilter=True enables the filter builder.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
