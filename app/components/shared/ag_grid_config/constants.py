"""
Universal AG Grid configuration constants.

Shared across all grids for consistent UX.
"""

# Standard status bar for all grids - shows row counts and aggregations
STANDARD_STATUS_BAR = {
    "statusPanels": [
        {"statusPanel": "agTotalRowCountComponent", "align": "left"},
        {"statusPanel": "agFilteredRowCountComponent", "align": "left"},
        {"statusPanel": "agSelectedRowCountComponent", "align": "center"},
        {"statusPanel": "agAggregationComponent", "align": "right"},
    ],
}

# Enhanced default column definition with floating filters
ENHANCED_DEFAULT_COL_DEF = {
    "sortable": True,
    "resizable": True,
    "filter": True,
    "floatingFilter": True,
}

# Standard default column definition (without floating filters)
STANDARD_DEFAULT_COL_DEF = {
    "sortable": True,
    "resizable": True,
    "filter": True,
}

# No-rows overlay message
NO_ROWS_TEMPLATE = (
    '<span style="padding: 10px; color: #6b7280;">No rows to display</span>'
)

# Compact mode configuration - reduces row height for dense data display
COMPACT_ROW_HEIGHT = 28  # Default is ~42px, compact is 28px
COMPACT_HEADER_HEIGHT = 32  # Slightly reduced header
