"""
FX Data AG-Grid Component.

Uses create_standard_grid factory with grid_toolbar for the FX Data page.
Supports live ticking with cell flash animation.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from starter_app.states.market_data import MarketDataState
from starter_app.components.shared.ag_grid_config import create_standard_grid, grid_toolbar


# =============================================================================
# CELL STYLES
# =============================================================================

# Pair name - bold blue link-style
_PAIR_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

# Change % - green for positive, red for negative
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

# Session badge style
_SESSION_STYLE = rx.Var(
    """(params) => ({
        backgroundColor: '#f0f9ff',
        color: '#0369a1',
        padding: '2px 8px',
        borderRadius: '9999px',
        fontSize: '11px',
        fontWeight: '500',
        display: 'inline-block'
    })"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the FX data grid."""
    return [
        ag_grid.column_def(
            field="pair",
            header_name="Pair",
            filter=AGFilters.text,
            min_width=100,
            pinned="left",
            cell_style=_PAIR_STYLE,
        ),
        ag_grid.column_def(
            field="bid",
            header_name="Bid",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="ask",
            header_name="Ask",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="mid",
            header_name="Mid",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="change_pct",
            header_name="Change %",
            filter=AGFilters.number,
            min_width=100,
            cell_style=_CHANGE_STYLE,
        ),
        ag_grid.column_def(
            field="spread",
            header_name="Spread",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="volume",
            header_name="Volume",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="session",
            header_name="Session",
            filter="agSetColumnFilter",
            min_width=110,
            cell_style=_SESSION_STYLE,
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter="agSetColumnFilter",
            min_width=90,
        ),
    ]


# =============================================================================
# STREAMING TOGGLE
# =============================================================================


def _stream_toggle() -> rx.Component:
    """Play/Pause toggle for FX data streaming."""
    return rx.el.button(
        rx.cond(
            MarketDataState.fx_streaming,
            rx.fragment(
                rx.icon("pause", size=14),
                rx.el.span("Live", class_name="text-[11px] font-bold uppercase tracking-wider"),
            ),
            rx.fragment(
                rx.icon("play", size=14),
                rx.el.span("Stream", class_name="text-[11px] font-bold uppercase tracking-wider"),
            ),
        ),
        on_click=MarketDataState.toggle_fx_stream,
        class_name=rx.cond(
            MarketDataState.fx_streaming,
            # Active state: pulsing green
            "h-7 px-3 rounded flex items-center gap-1.5 transition-all cursor-pointer "
            "bg-gradient-to-r from-emerald-500 to-green-600 text-white shadow-md "
            "animate-pulse",
            # Inactive state: neutral
            "h-7 px-3 rounded flex items-center gap-1.5 transition-all cursor-pointer "
            "bg-white border border-gray-200 text-gray-600 hover:border-emerald-400 "
            "hover:text-emerald-600 shadow-sm",
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "fx_data_grid_state"
_GRID_ID = "fx_data_grid"


def fx_data_ag_grid() -> rx.Component:
    """FX Data AG-Grid component with toolbar, streaming toggle, and cell flash."""
    return rx.vstack(
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="fx_data",
            search_value=MarketDataState.fx_search_text,
            on_search_change=MarketDataState.set_fx_search,
            on_search_clear=MarketDataState.clear_fx_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            extra_left_content=_stream_toggle(),
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MarketDataState.fx_row_data,
            column_defs=_get_column_defs(),
            row_id_key="pair",
            enable_row_numbers=True,
            enable_multi_select=True,
            enable_cell_flash=True,  # Flash cells on tick
            quick_filter_text=MarketDataState.fx_search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
