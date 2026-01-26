"""
Risk Measures AG-Grid Component.

AG-Grid based implementation for risk measures table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.risk.risk_state import RiskState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the risk measures grid."""
    return [
        ag_grid.column_def(
            field="seed",
            header_name="Seed",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="simulation_num",
            header_name="Simulation#",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="trial_num",
            header_name="Trial#",
            filter=AGFilters.text,
            min_width=80,
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
            field="sec_type",
            header_name="Sec Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="is_private",
            header_name="Is Private",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="national",
            header_name="National",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="national_used",
            header_name="National Used",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="national_current",
            header_name="National Current",
            filter=AGFilters.text,
            min_width=120,
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
            field="spot_price",
            header_name="Spot Price",
            filter=AGFilters.text,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def risk_measures_ag_grid() -> rx.Component:
    """
    Risk Measures AG-Grid component.

    Displays risk measures simulation data.
    """
    return ag_grid(
        id="risk_measures_grid",
        row_data=RiskState.filtered_risk_measures,
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
