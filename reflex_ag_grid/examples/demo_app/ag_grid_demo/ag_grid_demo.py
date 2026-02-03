"""
AG Grid Demo App - Demo pages showcasing all AG Grid requirements.

One page per requirement from the AG Grid Traceability Matrix.
"""

import reflex as rx

from .pages import (
    context_menu_page,
    range_selection_page,
    cell_flash_page,
    jump_highlight_page,
    grouping_page,
    notifications_page,
    validation_page,
    clipboard_page,
    excel_export_page,
    websocket_page,
    cell_editors_page,
    edit_pause_page,
    transaction_api_page,
    background_tasks_page,
    column_state_page,
    cell_renderers_page,
    tree_data_page,
    perf_test_page,
    status_bar_page,
    overlays_page,
    crud_data_source_page,
    advanced_filter_page,
    set_filter_page,
    multi_filter_page,
    row_numbers_page,
    quick_filter_page,
    gallery_page,
)


# =============================================================================
# APP - Demo Pages (one per requirement)
# =============================================================================

app = rx.App()

# Home
app.add_page(gallery_page, route="/", title="AG Grid Demo Gallery")

# Req 1-5
app.add_page(context_menu_page, route="/01-context-menu", title="01 - Context Menu")
app.add_page(
    range_selection_page, route="/02-range-selection", title="02 - Range Selection"
)
app.add_page(cell_flash_page, route="/03-cell-flash", title="03 - Cell Flash")
app.add_page(
    jump_highlight_page, route="/04-jump-highlight", title="04 - Jump & Highlight"
)
app.add_page(grouping_page, route="/05-grouping", title="05 - Grouping & Summary")

# Req 6-10
app.add_page(notifications_page, route="/06-notifications", title="06 - Notifications")
app.add_page(validation_page, route="/07-validation", title="07 - Validation")
app.add_page(clipboard_page, route="/08-clipboard", title="08 - Clipboard")
app.add_page(excel_export_page, route="/09-excel-export", title="09 - Excel Export")
app.add_page(websocket_page, route="/10-websocket", title="10 - WebSocket")

# Req 11-15
app.add_page(cell_editors_page, route="/11-cell-editors", title="11 - Cell Editors")
app.add_page(edit_pause_page, route="/12-edit-pause", title="12 - Edit Pause")
app.add_page(
    transaction_api_page, route="/13-transaction-api", title="13 - Transaction API"
)
app.add_page(
    background_tasks_page, route="/14-background-tasks", title="14 - Background Tasks"
)
app.add_page(column_state_page, route="/15-column-state", title="15 - Column State")

# Req 16-21
app.add_page(
    cell_renderers_page, route="/16-cell-renderers", title="16 - Cell Renderers"
)
app.add_page(tree_data_page, route="/17-tree-data", title="17 - Tree Data")
app.add_page(perf_test_page, route="/18-perf-test", title="18 - Performance")
app.add_page(status_bar_page, route="/19-status-bar", title="19 - Status Bar")
app.add_page(overlays_page, route="/20-overlays", title="20 - Overlays")
app.add_page(crud_data_source_page, route="/21-crud", title="21 - CRUD")

# Req 22-25 (Phase 3 - v35 Features)
app.add_page(
    advanced_filter_page, route="/22-advanced-filter", title="22 - Advanced Filter"
)
app.add_page(set_filter_page, route="/23-set-filter", title="23 - Set Filter")
app.add_page(multi_filter_page, route="/24-multi-filter", title="24 - Multi Filter")
app.add_page(row_numbers_page, route="/25-row-numbers", title="25 - Row Numbers")
app.add_page(quick_filter_page, route="/26-quick-filter", title="26 - Quick Filter")
