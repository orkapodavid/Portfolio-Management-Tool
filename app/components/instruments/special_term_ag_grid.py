"""
Special Term AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
Includes a position date selector that triggers database reload.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class SpecialTermGridState(rx.State):
    """State for Special Term grid quick filter."""

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
            field="pos_loc",
            header_name="Position Location",
            filter="agSetColumnFilter",  # Categorical
            min_width=130,
        ),
        ag_grid.column_def(
            field="account",
            header_name="Account",
            filter="agSetColumnFilter",  # Categorical
            min_width=100,
        ),
        ag_grid.column_def(
            field="effective_date",
            header_name="Effective Date",
            filter=AGFilters.date,
            min_width=110,
        ),
        ag_grid.column_def(
            field="position",
            header_name="Position",
            filter=AGFilters.number,
            min_width=90,
        ),
    ]


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar — triggers data reload on change."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span(
                    "POSITION DATE",
                    class_name=FILTER_LABEL_CLASS,
                ),
                rx.el.input(
                    type="date",
                    value=InstrumentState.special_terms_position_date,
                    on_change=InstrumentState.set_special_terms_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border border-gray-100 rounded-lg backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "special_term_grid_state"
_GRID_ID = "special_term_grid"


def special_term_ag_grid() -> rx.Component:
    """Special Term AG-Grid component with full toolbar support."""
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
            page_name="special_term",
            search_value=SpecialTermGridState.search_text,
            on_search_change=SpecialTermGridState.set_search,
            on_search_clear=SpecialTermGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=InstrumentState.special_terms_last_updated,
            show_refresh=True,
            on_refresh=InstrumentState.force_refresh_special_terms,
            is_loading=InstrumentState.is_loading_special_terms,
        ),
        # Position date selector bar
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=InstrumentState.special_terms,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=InstrumentState.is_loading_special_terms,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("special_term"),
            default_csv_export_params=get_default_csv_export_params("special_term"),
            quick_filter_text=SpecialTermGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )

