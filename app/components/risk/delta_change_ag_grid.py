"""
Delta Change AG-Grid Component.

Migrated to use create_standard_grid factory with cell flash enabled.
Includes a position date selector that triggers database reload.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.risk.risk_state import RiskState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    filter_date_input,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


class DeltaChangeGridState(rx.State):
    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            pinned="left",
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
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="fx_rate",
            header_name="FX Rate",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="current_price",
            header_name="Current Price",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="valuation_price",
            header_name="Valuation Price",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="pos_delta",
            header_name="POS DELTA",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="pos_delta_small",
            header_name="POS DELTA SMALL",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="pos_g", header_name="Pos G", filter=AGFilters.number, min_width=80
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
                    value=RiskState.delta_change_position_date,
                    on_change=RiskState.set_delta_change_position_date,
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


_STORAGE_KEY = "delta_change_grid_state"
_GRID_ID = "delta_change_grid"


def delta_change_ag_grid() -> rx.Component:
    """
    Delta Change AG-Grid component.

    Displays delta change data with:
    - Position date selector (defaults to today, auto-reloads on change)
    - Quick filter search across all columns
    - Excel export button
    - Full grid state persistence
    - Refresh button with loading overlay
    """
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
            page_name="delta_change",
            search_value=DeltaChangeGridState.search_text,
            on_search_change=DeltaChangeGridState.set_search,
            on_search_clear=DeltaChangeGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=RiskState.delta_change_last_updated,
            auto_refresh=RiskState.delta_change_auto_refresh,
            on_auto_refresh_toggle=RiskState.toggle_delta_change_auto_refresh,
            # Refresh button
            show_refresh=True,
            on_refresh=RiskState.force_refresh_delta_change,
            is_loading=RiskState.is_loading_delta_change,
        ),
        # Position date selector bar
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=RiskState.filtered_delta_changes,
            column_defs=_get_column_defs(),
            row_id_key="ticker",
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("delta_change"),
            default_csv_export_params=get_default_csv_export_params("delta_change"),
            quick_filter_text=DeltaChangeGridState.search_text,
            loading=RiskState.is_loading_delta_change,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=RiskState.start_delta_change_auto_refresh,
    )
