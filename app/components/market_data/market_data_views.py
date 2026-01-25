"""
Market Data Views - Re-exports for backward compatibility.

All table components have been split into individual files:
- market_data_ag_grid.py (AG-Grid implementation)
- fx_data_table.py
- historical_data_table.py
- trading_calendar_table.py
- market_hours_table.py
- table_components.py (shared helpers)

Import directly from individual files or from __init__.py for cleaner code.
"""

# Re-export all components for backward compatibility
from app.components.market_data.table_components import header_cell, text_cell
from app.components.market_data.market_data_ag_grid import market_data_ag_grid
from app.components.market_data.fx_data_table import fx_data_table, fx_data_row
from app.components.market_data.historical_data_table import (
    historical_data_table,
    historical_row,
)
from app.components.market_data.trading_calendar_table import (
    trading_calendar_table,
    calendar_row,
)
from app.components.market_data.market_hours_table import market_hours_table, hours_row

__all__ = [
    # Shared components
    "header_cell",
    "text_cell",
    # Table functions
    "market_data_ag_grid",
    "fx_data_table",
    "fx_data_row",
    "historical_data_table",
    "historical_row",
    "trading_calendar_table",
    "calendar_row",
    "market_hours_table",
    "hours_row",
]
