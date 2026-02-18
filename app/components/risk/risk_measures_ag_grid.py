"""
Risk Measures AG-Grid Component.

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


class RiskMeasuresGridState(rx.State):
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
            field="seed", header_name="Seed", filter=AGFilters.number, min_width=80
        ),
        ag_grid.column_def(
            field="simulation_num",
            header_name="Simulation#",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="trial_num",
            header_name="Trial#",
            filter=AGFilters.number,
            min_width=80,
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="is_private",
            header_name="Is Private",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="notional",
            header_name="Notional",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="notional_used",
            header_name="Notional Used",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="notional_current",
            header_name="Notional Current",
            filter=AGFilters.number,
            min_width=120,
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
            field="spot_price",
            header_name="Spot Price",
            filter=AGFilters.number,
            min_width=100,
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
                    value=RiskState.risk_measures_position_date,
                    on_change=RiskState.set_risk_measures_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "w-full px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border-b border-gray-100 backdrop-blur-sm"
        ),
    )


_STORAGE_KEY = "risk_measures_grid_state"
_GRID_ID = "risk_measures_grid"


def risk_measures_ag_grid() -> rx.Component:
    """
    Risk Measures AG-Grid component.

    Displays risk measures data with:
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
            page_name="risk_measures",
            search_value=RiskMeasuresGridState.search_text,
            on_search_change=RiskMeasuresGridState.set_search,
            on_search_clear=RiskMeasuresGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar
            last_updated=RiskState.risk_measures_last_updated,
            auto_refresh=RiskState.risk_measures_auto_refresh,
            on_auto_refresh_toggle=RiskState.toggle_risk_measures_auto_refresh,
            # Refresh button
            show_refresh=True,
            on_refresh=RiskState.force_refresh_risk_measures,
            is_loading=RiskState.is_loading_risk_measures,
        ),
        # Position date selector bar
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=RiskState.filtered_risk_measures,
            column_defs=_get_column_defs(),
            row_id_key="ticker",
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("risk_measures"),
            default_csv_export_params=get_default_csv_export_params("risk_measures"),
            quick_filter_text=RiskMeasuresGridState.search_text,
            loading=RiskState.is_loading_risk_measures,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=RiskState.start_risk_measures_auto_refresh,
    )
