# AG Grid Config Package

> **Location:** `app/components/shared/ag_grid_config/`
>
> Shared AG Grid configuration for consistent UX across all 48+ grid components.

## Package Structure

```
app/components/shared/ag_grid_config/
├── __init__.py            # Re-exports all 18 public symbols (backward-compatible)
├── constants.py           # Universal config: status bar, default col defs, overlay
├── grid_factory.py        # create_standard_grid() factory function
├── export_helpers.py      # Excel/CSV export params, JS helpers
├── state_persistence.py   # grid_state_script() — localStorage save/restore/reset
├── toolbar.py             # grid_toolbar() — unified toolbar component
├── filter_bar.py          # filter_date_range_bar(), filter_date_input(), CSS constants
└── context_menu.py        # build_context_menu(), context_menu_dispatch_input()
```

### Import Pattern (unchanged)

All imports go through the package `__init__.py` — **callers never import sub-modules directly**:

```python
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    grid_state_script,
    grid_toolbar,
    get_default_export_params,
    get_default_csv_export_params,
    filter_date_range_bar,
    build_context_menu,
    context_menu_dispatch_input,
    FILTER_BTN_CLASS,
)
```

---

## Module Reference

### `constants.py` — Universal Configuration

| Symbol | Type | Description |
|--------|------|-------------|
| `STANDARD_STATUS_BAR` | `dict` | Status bar config (total/filtered row count panels) |
| `STANDARD_DEFAULT_COL_DEF` | `dict` | Default col def (sortable, resizable, filterable, floating filters) |
| `ENHANCED_DEFAULT_COL_DEF` | `dict` | Extended default col def with enterprise features (animations, context menu) |
| `NO_ROWS_TEMPLATE` | `str` | HTML template for empty grid overlay |
| `COMPACT_ROW_HEIGHT` | `int` | Row height in compact mode (28px) |
| `COMPACT_HEADER_HEIGHT` | `int` | Header height in compact mode (32px) |

---

### `grid_factory.py` — `create_standard_grid()`

Factory function that wraps `reflex_ag_grid.ag_grid` with standardized defaults.

```python
create_standard_grid(
    grid_id: str,                        # Required. Unique DOM id
    row_data: rx.Var[list[dict]],        # Required. Data source
    column_defs: list,                   # Required. AG Grid column definitions
    *,
    # Tier 2 options:
    enable_cell_flash: bool = False,     # Real-time grids (market data, PnL, risk)
    enable_row_numbers: bool = False,    # Auto-numbered first column
    enable_multi_select: bool = False,   # Checkbox selection
    enable_compact_mode: bool = False,   # Dense rows (28px)
    row_id_key: str = "id",             # Unique row identifier field
    # Export params:
    default_excel_export_params=None,
    default_csv_export_params=None,
    # AG Grid passthrough:
    **kwargs,                            # Additional AG Grid props
)
```

---

### `export_helpers.py` — Export Parameters

| Symbol | Description |
|--------|-------------|
| `get_default_export_params(page_name)` | Returns Excel export params with timestamped filename |
| `get_default_csv_export_params(page_name)` | Returns CSV export params with timestamped filename |

Internal helpers (used by `toolbar.py`):
- `_get_export_excel_js(page_name)` — JavaScript snippet for toolbar Excel button

---

### `state_persistence.py` — `grid_state_script()`

Generates JavaScript for localStorage-based column state persistence.

```python
grid_state_script(storage_key: str, grid_id: str) -> str
```

Produces three global functions:
- `saveGridState_{key}()` — Save column order, widths, sort, filter to localStorage
- `restoreGridState_{key}()` — Restore saved state
- `resetGridState_{key}()` — Clear saved state and reset grid to defaults

---

### `toolbar.py` — `grid_toolbar()`

Unified toolbar component. Visual layout:

```
[Generate] [Excel] [↻] [🔍 Search...]     [Compact] | [Save] [Restore] [Reset]
```

Key parameters:

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `storage_key` | `str` | Required | localStorage key for save/restore/reset |
| `page_name` | `str` | Required | Prefix for export filenames |
| `search_value` | `rx.Var[str]` | `None` | Quick filter search binding |
| `on_search_change` | `Callable` | `None` | Search input handler |
| `show_generate` | `bool` | `False` | Show Generate dropdown |
| `show_refresh` | `bool` | `False` | Show Refresh button |
| `show_compact_toggle` | `bool` | `False` | Show Compact mode toggle |
| `grid_id` | `str` | `None` | Required for compact toggle |
| `show_excel` | `bool` | `True` | Show Excel export button |
| `show_save` | `bool` | `True` | Show Save Layout button |
| `show_restore` | `bool` | `True` | Show Restore Layout button |
| `show_reset` | `bool` | `True` | Show Reset Layout button |
| `last_updated` | `rx.Var[str]` | `None` | Timestamp for status bar |
| `auto_refresh` | `rx.Var[bool]` | `None` | Auto-refresh toggle state |
| `on_auto_refresh_toggle` | `Callable` | `None` | Auto-refresh toggle handler |

---

### `filter_bar.py` — Date Range Filter Bar

| Symbol | Type | Description |
|--------|------|-------------|
| `filter_date_range_bar(...)` | `Component` | Full FROM/TO date filter bar with Apply/Clear buttons |
| `filter_date_input(...)` | `Component` | Single date input with label and calendar icon |
| `FILTER_LABEL_CLASS` | `str` | Tailwind class string for filter labels |
| `FILTER_INPUT_CLASS` | `str` | Tailwind class string for filter inputs |
| `FILTER_BTN_CLASS` | `str` | Tailwind class string for filter buttons |

**`filter_date_range_bar` parameters:**

```python
filter_date_range_bar(
    from_value: rx.Var[str],          # FROM date value binding
    to_value: rx.Var[str],            # TO date value binding
    on_from_change: Callable,         # FROM date change handler
    on_to_change: Callable,           # TO date change handler
    on_apply: Callable,               # Apply filter handler
    has_active_filters: rx.Var[bool], # Show/hide Clear button
    on_clear: Callable,               # Clear filter handler
)
```

---

### `context_menu.py` — Custom Context Menu

Adds custom right-click context menu items to AG Grid Enterprise grids.

| Symbol | Type | Description |
|--------|------|-------------|
| `build_context_menu(...)` | `rx.Var` | Builds a `getContextMenuItems` JS callback |
| `context_menu_dispatch_input(...)` | `Component` | Hidden input bridge for JS→Reflex event dispatch |

**Architecture:** Uses a visually-hidden `<input>` as a bridge between AG Grid's JS context menu `action` callbacks and Reflex's Python event handlers. When a custom menu item is clicked, JS writes a JSON payload to the hidden input, which triggers Reflex's `on_change` to dispatch to the backend.

**`build_context_menu` parameters:**

```python
build_context_menu(
    target_id: str,               # Must match the target_id in context_menu_dispatch_input
    items: list[dict],            # List of custom menu items (see below)
    include_defaults: bool=True,  # Append built-in Copy/Export items
) -> rx.Var
```

Each item dict:
- `name` (str): Display label (e.g. `"Rerun"`)
- `icon` (str, optional): Emoji or short HTML (e.g. `"🔄"`)

**`context_menu_dispatch_input` parameters:**

```python
context_menu_dispatch_input(
    target_id: str,       # Must match the target_id used in build_context_menu
    on_action: EventHandler,  # State handler receiving JSON payload str
)
```

The `on_action` handler receives a JSON string: `{"action": "Rerun", "row": {...row data...}}`

---

## Complete Usage Example

```python
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    grid_state_script,
    grid_toolbar,
    get_default_export_params,
    get_default_csv_export_params,
    filter_date_range_bar,
    build_context_menu,
    context_menu_dispatch_input,
)

_STORAGE_KEY = "my_grid_state"
_GRID_ID = "my_grid"
_CTX_MENU_ID = "my_grid_ctx"

# Build the context menu once at module level
_CONTEXT_MENU = build_context_menu(
    target_id=_CTX_MENU_ID,
    items=[
        {"name": "Rerun", "icon": "🔄"},
        {"name": "Kill",  "icon": "🛑"},
    ],
)

def my_grid_component() -> rx.Component:
    return rx.vstack(
        # 0. Context menu dispatch bridge
        context_menu_dispatch_input(
            target_id=_CTX_MENU_ID,
            on_action=MyState.handle_context_menu_action,
        ),
        # 1. State persistence script
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        # 2. Toolbar
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="my_table",
            search_value=MyState.search_text,
            on_search_change=MyState.set_search,
            on_search_clear=MyState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=MyState.last_updated,
            auto_refresh=MyState.auto_refresh,
            on_auto_refresh_toggle=MyState.toggle_auto_refresh,
        ),
        # 3. Optional filter bar
        filter_date_range_bar(
            from_value=MyState.from_date,
            to_value=MyState.to_date,
            on_from_change=MyState.set_from_date,
            on_to_change=MyState.set_to_date,
            on_apply=MyState.apply_filters,
            has_active_filters=MyState.has_filters,
            on_clear=MyState.clear_filters,
        ),
        # 4. Grid (pass context menu via kwargs)
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MyState.data,
            column_defs=_get_column_defs(),
            enable_cell_flash=True,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("my_table"),
            default_csv_export_params=get_default_csv_export_params("my_table"),
            quick_filter_text=MyState.search_text,
            get_context_menu_items=_CONTEXT_MENU,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
```

### Context Menu State Handler Example

```python
import json

class MyState(rx.State):
    async def handle_context_menu_action(self, payload_json: str):
        """Handle context menu actions from AG Grid."""
        payload = json.loads(payload_json)
        action = payload["action"]   # "Rerun" or "Kill"
        row = payload["row"]         # full row data dict

        if action == "Rerun":
            # ... call your service
            yield rx.toast.success(f"Rerunning {row['name']}")
        elif action == "Kill":
            yield rx.toast.warning(f"Killing {row['name']}")
```

---

## Related Documentation

- [AG Grid Factory Migration](../prompts/ag_grid_factory_migration_prompt.md) — Tier 2 options, column defs, value formatting, troubleshooting
- [AG Grid Wrapper Spec](ag-grid-reflex-wrapper-spec.md) — Low-level `reflex_ag_grid` wrapper reference (v35)
- [Status Bar Rollout](../todos/ag_grids/status_bar_rollout.md) — Status bar and auto-refresh implementation
