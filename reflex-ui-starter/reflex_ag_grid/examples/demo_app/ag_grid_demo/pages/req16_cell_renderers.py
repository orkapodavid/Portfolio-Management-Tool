"""
16 - Cell Renderers Page - Demonstrates cell styling with cellStyle, cellClass, and cellClassRules.

Requirement 16: Custom cell styling for conditional formatting
AG Grid Feature: cellStyle, cellClass, cellClassRules
"""

import reflex as rx

from reflex_ag_grid import ag_grid, AGFilters

from ..state import DemoState
from ..components import nav_bar


# =============================================================================
# CELL STYLE EXAMPLES
# =============================================================================

# Style 1: Static style (blue link)
_LINK_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

# Style 2: Conditional color based on value (green/red)
_CHANGE_STYLE = rx.Var(
    """(params) => {
        const val = parseFloat(params.value);
        if (isNaN(val)) return {};
        return {
            color: val >= 0 ? '#059669' : '#dc2626',
            fontWeight: '500'
        };
    }"""
)

# Style 3: Badge style with background
_BADGE_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const colors = {
            'active': { bg: '#d1fae5', text: '#065f46' },
            'pending': { bg: '#fef3c7', text: '#92400e' },
            'inactive': { bg: '#fee2e2', text: '#991b1b' }
        };
        const style = colors[val] || { bg: '#f3f4f6', text: '#374151' };
        return {
            backgroundColor: style.bg,
            color: style.text,
            padding: '2px 8px',
            borderRadius: '9999px',
            fontSize: '11px',
            fontWeight: '500',
            display: 'inline-block'
        };
    }"""
)


def get_styled_columns() -> list:
    """Return column definitions with cell styling examples."""
    return [
        ag_grid.column_def(
            field="id",
            header_name="ID",
            min_width=80,
        ),
        ag_grid.column_def(
            field="symbol",
            header_name="Symbol (Link Style)",
            filter=AGFilters.text,
            min_width=150,
            cell_style=_LINK_STYLE,
        ),
        ag_grid.column_def(
            field="change",
            header_name="Change % (Color)",
            filter=AGFilters.number,
            min_width=150,
            cell_style=_CHANGE_STYLE,
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status (Badge)",
            filter=AGFilters.text,
            min_width=140,
            cell_style=_BADGE_STYLE,
        ),
        ag_grid.column_def(
            field="sector",
            header_name="Sector",
            filter=AGFilters.text,
            min_width=120,
        ),
    ]


def cell_renderers_page() -> rx.Component:
    """Cell Renderers demo page.

    Features:
    - cellStyle for inline styling
    - Conditional colors based on value
    - Badge/pill styling with backgrounds
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("16 - Cell Renderers", size="6"),
        rx.text("Custom cell styling with cellStyle, cellClass, and cellClassRules"),
        rx.callout(
            "The grid below demonstrates different cell styling patterns.",
            icon="info",
        ),
        # Style Examples Card
        rx.card(
            rx.vstack(
                rx.text("Cell Style Examples:", weight="bold"),
                rx.hstack(
                    rx.badge("Symbol", color_scheme="blue"),
                    rx.text("→ Blue link style (static)"),
                ),
                rx.hstack(
                    rx.badge("Change %", color_scheme="green"),
                    rx.text("→ Green/red based on value (conditional)"),
                ),
                rx.hstack(
                    rx.badge("Status", color_scheme="purple"),
                    rx.text("→ Badge/pill styling (complex)"),
                ),
                spacing="2",
                align="start",
            ),
        ),
        ag_grid(
            id="cell_renderers_grid",
            row_data=DemoState.data,
            column_defs=get_styled_columns(),
            row_id_key="id",
            theme="quartz",
            width="90vw",
            height="50vh",
        ),
        # Code Example
        rx.card(
            rx.vstack(
                rx.text("Usage Example:", weight="bold"),
                rx.code_block(
                    """# Define cell style as rx.Var with JS function
_CHANGE_STYLE = rx.Var(
    '''(params) => {
        const val = parseFloat(params.value);
        return {
            color: val >= 0 ? '#059669' : '#dc2626',
            fontWeight: '500'
        };
    }'''
)

# Apply to column definition
ag_grid.column_def(
    field="change",
    header_name="Change %",
    cell_style=_CHANGE_STYLE,
)""",
                    language="python",
                ),
                spacing="2",
                align="start",
            ),
            width="90vw",
        ),
        rx.text(
            "cellStyle accepts a JS function that returns a CSS style object.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
