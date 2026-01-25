"""
Demo App Pages - All 15 demo pages (one per requirement).

Exports all page functions for app registration.
"""

from .req01_context_menu import context_menu_page
from .req02_range_selection import range_selection_page
from .req03_cell_flash import cell_flash_page
from .req04_jump_highlight import jump_highlight_page
from .req05_grouping import grouping_page
from .req06_notifications import notifications_page
from .req07_validation import validation_page
from .req08_clipboard import clipboard_page
from .req09_excel_export import excel_export_page
from .req10_websocket import websocket_page
from .req11_cell_editors import cell_editors_page
from .req12_edit_pause import edit_pause_page
from .req13_transaction_api import transaction_api_page
from .req14_background_tasks import background_tasks_page
from .req15_column_state import column_state_page

__all__ = [
    "context_menu_page",
    "range_selection_page",
    "cell_flash_page",
    "jump_highlight_page",
    "grouping_page",
    "notifications_page",
    "validation_page",
    "clipboard_page",
    "excel_export_page",
    "websocket_page",
    "cell_editors_page",
    "edit_pause_page",
    "transaction_api_page",
    "background_tasks_page",
    "column_state_page",
]
