"""
Instrument Term AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class InstrumentTermGridState(rx.State):
    """State for Instrument Term grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="deal_num",
            header_name="Deal Num",
            filter=AGFilters.text,
            min_width=90,
            pinned="left",
            tooltip_field="deal_num",
        ),
        ag_grid.column_def(
            field="detail_id",
            header_name="Detail ID",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="ticker",
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter="agSetColumnFilter",  # Categorical
            min_width=90,
        ),
        ag_grid.column_def(
            field="effective_date",
            header_name="Effective Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="maturity_date",
            header_name="Maturity Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="first_reset_da",
            header_name="First Reset Da",
            filter=AGFilters.date,
            min_width=120,
            tooltip_field="first_reset_da",
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "instrument_term_grid_state"
_GRID_ID = "instrument_term_grid"


def instrument_term_ag_grid() -> rx.Component:
    """Instrument Term AG-Grid component with full toolbar support."""
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="instrument_term",
            search_value=InstrumentTermGridState.search_text,
            on_search_change=InstrumentTermGridState.set_search,
            on_search_clear=InstrumentTermGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=InstrumentState.instrument_terms_last_updated,
            show_refresh=True,
            on_refresh=InstrumentState.force_refresh_instrument_terms,
            is_loading=InstrumentState.is_loading_instrument_terms,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=InstrumentState.instrument_terms,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=InstrumentState.is_loading_instrument_terms,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("instrument_term"),
            default_csv_export_params=get_default_csv_export_params("instrument_term"),
            quick_filter_text=InstrumentTermGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
