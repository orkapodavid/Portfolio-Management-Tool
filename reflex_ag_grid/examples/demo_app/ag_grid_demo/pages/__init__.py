"""
Demo App Pages - All demo pages (one per requirement).

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
from .req16_cell_renderers import cell_renderers_page
from .req17_tree_data import tree_data_page
from .req18_perf_testing import perf_test_page
from .req19_status_bar import status_bar_page
from .req20_overlays import overlays_page
from .req21_crud_data_source import crud_data_source_page
from .req22_advanced_filter import advanced_filter_page
from .req23_set_filter import set_filter_page
from .req24_multi_filter import multi_filter_page
from .req25_row_numbers import row_numbers_page
from .gallery import gallery_page

__all__ = [
    "gallery_page",
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
    "cell_renderers_page",
    "tree_data_page",
    "perf_test_page",
    "status_bar_page",
    "overlays_page",
    "crud_data_source_page",
    "advanced_filter_page",
    "set_filter_page",
    "multi_filter_page",
    "row_numbers_page",
]
