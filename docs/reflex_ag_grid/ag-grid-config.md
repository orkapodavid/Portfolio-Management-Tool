# AG Grid Configuration Guide

This module provides a standardized factory for AG Grid components with consistent UX across all grids.

**File**: `app/components/shared/ag_grid_config.py`

---

## Quick Start

```python
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    grid_toolbar,
    grid_state_script,
)

def my_grid() -> rx.Component:
    return rx.fragment(
        rx.script(grid_state_script("my_grid_state", "my_grid")),
        grid_toolbar(
            storage_key="my_grid_state",
            page_name="my_report",
            search_value=State.search,
            on_search_change=State.set_search,
        ),
        create_standard_grid(
            grid_id="my_grid",
            row_data=State.data,
            column_defs=columns,
            row_id_key="id",  # Required for delta updates
            loading=State.is_loading,
        ),
    )
```

---

## `create_standard_grid()` - Factory Function

Creates AG Grid with Tier 1 universal enhancements enabled by default.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `grid_id` | `str` | required | Unique grid identifier |
| `row_data` | `rx.Var` | required | State variable with row data |
| `column_defs` | `list[dict]` | required | Column definitions |
| `row_id_key` | `str` | `"id"` | Field for unique row ID (required for updates) |
| **Tier 1 (default on)** ||||
| `enable_status_bar` | `bool` | `True` | Status bar with row counts |
| `enable_range_selection` | `bool` | `True` | Drag-selection of cell ranges |
| `enable_floating_filters` | `bool` | `True` | Quick-filter row under headers |
| `enable_no_rows_overlay` | `bool` | `True` | Message when data is empty |
| **Tier 2 (opt-in)** ||||
| `enable_cell_flash` | `bool` | `False` | Flash cells on value change |
| `enable_row_numbers` | `bool` | `False` | Auto-numbered row column |
| `enable_multi_select` | `bool` | `False` | Multi-row selection with checkboxes |
| `enable_compact_mode` | `bool` | `False` | Dense row height (28px) |
| `enable_notification_jump` | `bool` | `True` | Jump-to-row from sidebar |
| **Loading** ||||
| `loading` | `rx.Var[bool]` | `False` | Shows loading overlay |
| `loading_template` | `str` | `"Loading..."` | Custom loading HTML |

---

## `grid_toolbar()` - Unified Toolbar

Combines search, export, and layout controls above the grid.

### Visual Layout
```
[Generate▼] [Excel] [↻] [🔍 Search...] [📅 Date] │ [Compact] │ [Save] [Restore] [Reset]
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `storage_key` | `str` | localStorage key for grid state |
| `page_name` | `str` | Export filename prefix |
| `search_value` | `rx.Var[str]` | Search text state |
| `on_search_change` | `Callable` | Search handler |
| `show_generate` | `bool` | Show Generate dropdown |
| `generate_items` | `list[str]` | Dropdown menu items |
| `on_generate` | `Callable` | Generate item click handler |
| `show_refresh` | `bool` | Show Refresh button |
| `on_refresh` | `Callable` | Refresh handler |
| `is_loading` | `rx.Var[bool]` | Loading spinner state |
| `show_date_picker` | `bool` | Show date input |
| `show_compact_toggle` | `bool` | Show Compact mode button |
| `grid_id` | `str` | Required if `show_compact_toggle=True` |
| `last_updated` | `rx.Var[str]` | Shows status bar with timestamp |
| `auto_refresh` | `rx.Var[bool]` | Auto-refresh toggle state |

---

## `grid_state_script()` - State Persistence

Generates JavaScript for localStorage-based grid state persistence (columns, filters, sort).

```python
rx.script(grid_state_script("my_grid_state", "my_grid"))
```

### Generated Functions
- `saveGridState_{key}()` - Save state to localStorage
- `restoreGridState_{key}()` - Restore state with flex fix
- `resetGridState_{key}()` - Reset to defaults
- Auto-restore on page load (polling for SPA)

---

## Export Helpers

### `get_default_export_params(page_name: str)`
Excel export params with timestamped filename and selected-rows-only filtering.

```python
create_standard_grid(
    ...,
    default_excel_export_params=get_default_export_params("pnl_full"),
)
# Exports: pnl_full_20260207_1430.xlsx
```

---

## Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `STANDARD_STATUS_BAR` | dict | Status bar with row counts + aggregation |
| `ENHANCED_DEFAULT_COL_DEF` | dict | Sortable, resizable, filter + floating filter |
| `STANDARD_DEFAULT_COL_DEF` | dict | Sortable, resizable, filter (no floating) |
| `COMPACT_ROW_HEIGHT` | `28` | Dense row height (default ~42px) |
| `COMPACT_HEADER_HEIGHT` | `32` | Compact header height |

---

## v35 Migration Notes

AG Grid v35 introduced breaking changes handled by the wrapper:

| v32 (Old) | v35 (Current) |
|-----------|---------------|
| `row_selection="multiple"` | `rowSelection.mode: "multiRow"` |
| `enable_cell_change_flash` | `defaultColDef.enableCellChangeFlash` |
| `enable_range_selection` | `cell_selection=True` |
| CSS-based theming | JS theme objects (`theme="quartz"`) |

The `reflex_ag_grid` wrapper automatically transforms props to v35 format.

---

## Enterprise Features

| Feature | Prop |
|---------|------|
| Range Selection | `cell_selection=True` |
| Advanced Filter | `enable_advanced_filter=True` |
| Status Bar | `status_bar=STANDARD_STATUS_BAR` |
| Excel Export | Context menu or `exportDataAsExcel()` |
| Row Grouping | `rowGroup=True` in column def |

---

## Troubleshooting

### Grid API not found
The wrapper uses React Fiber traversal to access AG Grid API:
```javascript
const wrapper = document.querySelector('#grid_id .ag-root-wrapper');
const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
```

### Props not recognized after changes
```bash
uv sync --reinstall-package reflex-ag-grid
```

### Loading overlay not showing
Ensure `loading` is a reactive state variable, not a static boolean.
