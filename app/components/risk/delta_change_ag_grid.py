"""
Delta Change AG-Grid Component.

AG-Grid based implementation for delta change table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.risk.risk_state import RiskState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the delta change grid."""
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="structure",
            header_name="Structure",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="fx_rate",
            header_name="FX Rate",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="current_price",
            header_name="Current Price",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="valuation_price",
            header_name="Valuation Price",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="pos_delta",
            header_name="POS DELTA",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="pos_delta_small",
            header_name="POS DELTA SMALL",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="pos_g",
            header_name="Pos G",
            filter=AGFilters.text,
            min_width=80,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def delta_change_ag_grid() -> rx.Component:
    """
    Delta Change AG-Grid component.

    Displays delta change data for risk analysis.
    """
    return ag_grid(
        id="delta_change_grid",
        row_data=RiskState.filtered_delta_changes,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="calc(100vh - 300px)",
        width="100%",
    )
