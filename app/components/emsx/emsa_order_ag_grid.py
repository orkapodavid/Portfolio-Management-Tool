"""
EMSA Order AG-Grid Component.

AG-Grid based implementation for EMSA order table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.emsx.emsx_state import EMSXState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the EMSA order grid."""
    return [
        ag_grid.column_def(
            field="sequence",
            header_name="Sequence",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="broker",
            header_name="Broker",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="pos_loc",
            header_name="Pos Loc",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="side",
            header_name="Side",
            filter=AGFilters.text,
            min_width=70,
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="emsa_amount",
            header_name="EMSA Amount",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="emsa_routed",
            header_name="EMSA Routed",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="emsa_working",
            header_name="EMSA Working",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="emsa_filled",
            header_name="EMSA Filled",
            filter=AGFilters.text,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def emsa_order_ag_grid() -> rx.Component:
    """
    EMSA Order AG-Grid component.

    Displays EMSA orders with sequence, ticker, broker information.
    """
    return ag_grid(
        id="emsa_order_grid",
        row_data=EMSXState.filtered_emsa_orders,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="100%",
        width="100%",
    )
