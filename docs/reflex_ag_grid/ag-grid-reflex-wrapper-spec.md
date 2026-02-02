# AG Grid Enterprise Wrapper for Reflex Python

## Overview

A generic, reusable AG Grid Enterprise wrapper for Reflex Python applications, providing high-performance data grids with cell-level updates and trading-terminal features.

**Version:** AG Grid v35.0.1  
**Framework:** Reflex Python  
**Architecture:** Local workspace package (`reflex_ag_grid/`)

---

## Project Structure

```
reflex_ag_grid/
├── __init__.py              # Package exports (ag_grid, column_def, AGFilters, AGEditors)
├── pyproject.toml           # UV workspace package configuration
├── components/
│   ├── ag_grid.py           # Main Reflex component (AgGrid class)
│   └── ag_grid_state.py     # Base state mixin (jump_to_row, export helpers)
├── docs/                    # Feature documentation (25 pages)
│   ├── README.md            # Quick reference table
│   └── 01_context_menu.md...25_row_numbers.md
├── examples/demo_app/       # Demo application (all 25 features)
│   ├── rxconfig.py
│   ├── ag_grid_demo/
│   │   ├── state.py         # DemoState class
│   │   ├── data.py          # Sample data
│   │   └── pages/           # req01_*.py through req25_*.py
│   └── README.md
└── tests/                   # E2E tests (Playwright)
```

---

## Feature Matrix (25 Requirements)

| # | Feature | AG Grid API | Enterprise |
|---|---------|-------------|:----------:|
| 01 | Context Menu | `getContextMenuItems()` | ✅ |
| 02 | Range Selection | `cellSelection` | ✅ |
| 03 | Cell Flash | `enableCellChangeFlash` | |
| 04 | Jump & Highlight | `ensureNodeVisible()` + `flashCells()` | |
| 05 | Grouping & Summary | `rowGroup` + `aggFunc` | ✅ |
| 06 | Notifications | Custom Reflex component | |
| 07 | Validation | `cellEditorParams.validation` | |
| 08 | Clipboard | Context menu + Clipboard API | ✅ |
| 09 | Excel Export | `exportDataAsExcel()` | ✅ |
| 10 | WebSocket Updates | Reflex state management | |
| 11 | Cell Editors | `cellEditor` (select, checkbox, etc.) | |
| 12 | Edit Pause + Undo/Redo | `undoRedoCellEditing` | |
| 13 | Transaction API | `applyTransaction()` | |
| 14 | Background Tasks | `rx.background` | |
| 15 | Column State | `localStorage` persistence | |
| 16 | Cell Renderers | `cellStyle`, `cellClass` | |
| 17 | Tree Data | `treeData` + `getDataPath` | ✅ |
| 18 | Performance (1000 rows) | Delta updates via `row_id_key` | |
| 19 | Status Bar | `statusBar` panels | ✅ |
| 20 | Overlays | `loading`, overlay templates | |
| 21 | CRUD Data Source | Pandas-backed operations | |
| 22 | Advanced Filter | `enableAdvancedFilter` | ✅ |
| 23 | Set Filter | `agSetColumnFilter` | ✅ |
| 24 | Multi Filter | `agMultiColumnFilter` | ✅ |
| 25 | Row Numbers | `rowNumbers` | ✅ |

---

## v35 Migration Notes

### Theming API (Breaking Change)

AG Grid v35 replaced CSS-based theming with JavaScript theme objects:

```python
# v35 - Pass theme name, wrapper handles JS object
ag_grid(theme="quartz", ...)  # "quartz" | "balham" | "alpine" | "material"
```

The wrapper imports theme objects (`themeQuartz`, etc.) from `ag-grid-community` and passes raw JS references.

### Module Registration

Enterprise features require module registration (handled automatically):

```python
# Wrapper's add_custom_code() registers modules
ModuleRegistry.registerModules([AllEnterpriseModule]);
```

### Row Selection (v35 Object Format)

String values are transformed to v35 objects:

```python
# What you write
ag_grid(row_selection="multiple", ...)

# What renders to JavaScript
{ rowSelection: { mode: "multiRow", checkboxes: true } }
```

### Deprecated Props Migration

| v32 (Deprecated) | v35 (Current) |
|------------------|---------------|
| `row_selection="multiple"` | `rowSelection.mode: "multiRow"` |
| `enable_cell_change_flash` | `defaultColDef.enableCellChangeFlash` |
| `suppress_row_click_selection` | `rowSelection.enableClickSelection` |
| `group_selects_children` | `rowSelection.groupSelects` |
| `enable_range_selection` | `cell_selection=True` |

---

## Quick Start

```python
import reflex as rx
from reflex_ag_grid import ag_grid

class State(rx.State):
    data: list[dict] = [
        {"id": "1", "symbol": "AAPL", "price": 175.50},
        {"id": "2", "symbol": "GOOGL", "price": 140.25},
    ]

def index():
    return ag_grid(
        id="my_grid",
        row_data=State.data,
        column_defs=[
            {"field": "symbol", "headerName": "Symbol"},
            {"field": "price", "headerName": "Price", "editable": True},
        ],
        row_id_key="id",  # Required for delta updates
        theme="quartz",
    )
```

---

## Key Props Reference

### Grid-Level Props

| Prop | Type | Description |
|------|------|-------------|
| `row_data` | `list[dict]` | Grid data (required) |
| `column_defs` | `list[dict]` | Column definitions (required) |
| `row_id_key` | `str` | Field for unique row ID (required for updates) |
| `theme` | `str` | `"quartz"`, `"balham"`, `"alpine"`, `"material"` |
| `row_selection` | `str` | `"single"` or `"multiple"` |
| `cell_selection` | `bool` | Enable range selection |
| `default_col_def` | `dict` | Default column properties |
| `auto_size_strategy` | `dict` | `{"type": "fitCellContents"}` |

### Enterprise Props

| Prop | Type | Description |
|------|------|-------------|
| `enable_advanced_filter` | `bool` | Enable advanced filter builder |
| `status_bar` | `dict` | Status bar configuration |
| `tree_data` | `bool` | Enable tree data mode |
| `get_data_path` | `rx.Var` | JS function for tree hierarchy |
| `grand_total_row` | `str` | `"top"` or `"bottom"` |
| `row_numbers` | `bool` | Show row number column |

### Overlay Props

| Prop | Type | Description |
|------|------|-------------|
| `loading` | `bool` | Show loading overlay |
| `overlay_loading_template` | `str` | Custom loading HTML |
| `overlay_no_rows_template` | `str` | Custom no-rows HTML |

---

## Events

| Event | Payload |
|-------|---------|
| `on_cell_value_changed` | `{rowId, field, oldValue, newValue, rowData}` |
| `on_row_clicked` | `{rowId, rowData}` |
| `on_selection_changed` | `{selectedRows, selectedCount}` |
| `on_grid_ready` | `{}` |

---

## Running the Demo

```bash
cd reflex_ag_grid/examples/demo_app
uv run reflex run
# Open http://localhost:3000
```

## Troubleshooting

### Startup Crash (SIGSEGV)

```bash
# Clean reinstall
cd reflex_ag_grid/examples/demo_app
uv sync --reinstall
uv run reflex run
```

### Props Not Recognized

After modifying `ag_grid.py`, reinstall the package:

```bash
uv sync --reinstall-package reflex-ag-grid
```

---

## Documentation Links

- [Full README](../../reflex_ag_grid/README.md)
- [Demo Docs](../../reflex_ag_grid/docs/README.md)
- [Implementation History](../todos/table_improvement.md)
