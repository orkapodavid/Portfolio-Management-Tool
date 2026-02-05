"""
Risk Inputs AG-Grid Component.

Migrated to use create_standard_grid factory with cell flash enabled.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.risk.risk_state import RiskState
from app.components.shared.ag_grid_config import create_standard_grid


class RiskInputsGridState(rx.State):
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
            field="national",
            header_name="National",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="national_used",
            header_name="National Used",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="national_current",
            header_name="National Current",
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


_STORAGE_KEY = "risk_inputs_grid_state"
_GRID_ID = "risk_inputs_grid"


def risk_inputs_ag_grid() -> rx.Component:
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
            page_name="risk_inputs",
            search_value=RiskInputsGridState.search_text,
            on_search_change=RiskInputsGridState.set_search,
            on_search_clear=RiskInputsGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar - use mixin-specific state
            last_updated=RiskState.risk_inputs_last_updated,
            auto_refresh=RiskState.risk_inputs_auto_refresh,
            on_auto_refresh_toggle=RiskState.toggle_risk_inputs_auto_refresh,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=RiskState.filtered_risk_inputs,
            column_defs=_get_column_defs(),
            row_id_key="seed",
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("risk_inputs"),
            default_csv_export_params=get_default_csv_export_params("risk_inputs"),
            quick_filter_text=RiskInputsGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=RiskState.start_risk_inputs_auto_refresh,
    )

