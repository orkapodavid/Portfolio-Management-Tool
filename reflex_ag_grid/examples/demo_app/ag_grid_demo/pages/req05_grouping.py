"""
05 - Grouping & Summary Page - Demonstrates row grouping, aggregation, and grand total pinning.

Requirement 5: Grouping & Summary + Grand Total Pinning
AG Grid Feature: rowGroup + aggFunc + rowGroupPanelShow + grandTotalRow
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..components import nav_bar, status_badge


def get_dynamic_grouped_columns():
    """Columns with dynamic grouping support.

    All columns have enable_row_group=True so they can be dragged
    to the grouping panel.
    """
    return [
        ag_grid.column_def(
            field="symbol",
            header_name="Symbol",
            enable_row_group=True,  # Can be grouped
            sortable=True,
        ),
        ag_grid.column_def(
            field="company",
            header_name="Company",
            flex=1,
            enable_row_group=True,
        ),
        ag_grid.column_def(
            field="sector",
            header_name="Sector",
            enable_row_group=True,
            row_group=True,  # Default grouped by sector
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            agg_func="avg",  # Aggregate function
            enable_row_group=True,
        ),
        ag_grid.column_def(
            field="qty",
            header_name="Quantity",
            agg_func="sum",
            enable_row_group=True,
        ),
        ag_grid.column_def(
            field="change",
            header_name="Change %",
            agg_func="avg",
            enable_row_group=True,
        ),
    ]


def grouping_page() -> rx.Component:
    """Grouping & Summary page.

    Features:
    - Row grouping by sector column (default)
    - Drag columns to grouping panel for multi-column grouping
    - Aggregation functions (sum, avg)
    - Expandable/collapsible group rows
    - Group summaries with totals
    - Grand Total Pinning at bottom (Phase 3)
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("05 - Grouping & Summary", size="6"),
        rx.text("Requirement 5: Grouping & Summary + Grand Total Pinning"),
        rx.callout(
            "DRAG column headers to the 'Row Groups' panel at top to group by that column. "
            "Grand total is pinned at the bottom!",
            icon="info",
        ),
        rx.hstack(
            rx.text("Currently grouped by:", weight="bold"),
            rx.badge("Sector", color_scheme="blue"),
            rx.text("(drag more columns to panel above grid)"),
            rx.badge("Grand Total: Bottom", color_scheme="green"),
            spacing="2",
        ),
        status_badge(),
        ag_grid(
            id="grouping_grid",
            row_data=DemoState.data,
            column_defs=get_dynamic_grouped_columns(),
            # Show row group panel for drag-drop grouping
            row_group_panel_show="always",
            group_default_expanded=-1,  # -1 = all expanded
            # Grand Total Pinning (Phase 3)
            grand_total_row="bottom",
            # Enable sidebar with columns tool
            side_bar=True,
            # Enable grouping for all columns via defaultColDef
            default_col_def={"enableRowGroup": True},
            # Use on_grid_ready to set rowGroupPanelShow via API
            # (workaround for Reflex prop passing issue)
            on_grid_ready=rx.Var(
                "(e) => e.api.setGridOption('rowGroupPanelShow', 'always')"
            ).to(rx.EventChain),
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.box(
            rx.heading("How to Group:", size="4"),
            rx.text("1. Drag any column header to the 'Row Groups' bar at the top"),
            rx.text("2. Drop multiple columns for nested grouping"),
            rx.text("3. Remove a group by dragging it back out"),
            rx.text("4. Grand Total row is pinned at the bottom (v33.3+ feature)"),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        rx.text(
            "Enterprise feature: Row grouping with drag-drop panel, aggregation, and grand total pinning.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
