# Reflex AG Grid Enterprise Wrapper

A generic, reusable AG Grid Enterprise wrapper for Reflex Python applications.

## Features

- ✅ **AG Grid Enterprise** - Full feature set (grouping, range selection, Excel export, context menu)
- ✅ **Simple API** - Use `ag_grid()` and `ag_grid.column_def()` helpers
- ✅ **Value Formatters** - Display currency ($175.50) while copying raw (175.5)
- ✅ **Event Sanitization** - Safe event data without circular references
- ✅ **Column Persistence** - Auto-save column state to localStorage

## Installation

This package is designed as a local package within your Reflex project.

1. The `reflex_ag_grid/` folder should be at your project root
2. Dependencies are managed via Reflex's npm integration (no separate package.json needed)

3. Set your license key (optional, removes watermark):

```python
import os
os.environ["AG_GRID_LICENSE_KEY"] = "your-license-key"
```

## Quick Start

```python
import reflex as rx
from reflex_ag_grid import ag_grid

class State(rx.State):
    data: list[dict] = [
        {"id": "1", "symbol": "AAPL", "price": 175.50, "qty": 100},
        {"id": "2", "symbol": "GOOGL", "price": 140.25, "qty": 50},
        {"id": "3", "symbol": "MSFT", "price": 378.91, "qty": 75},
    ]
    
    def on_cell_edit(self, data: dict):
        row_id = data["rowId"]
        field = data["field"]
        new_value = data["newValue"]
        print(f"Edited {field} to {new_value} in row {row_id}")


def index():
    return ag_grid(
        id="my_grid",
        row_data=State.data,
        column_defs=[
            ag_grid.column_def(field="symbol", header_name="Symbol"),
            ag_grid.column_def(
                field="price",
                header_name="Price",
                value_formatter=rx.Var(
                    "(params) => '$' + params.value.toFixed(2)"
                ).to(rx.EventChain),
            ),
            ag_grid.column_def(field="qty", header_name="Quantity", editable=True),
        ],
        on_cell_value_changed=State.on_cell_edit,
        theme="quartz",
        width="100%",
        height="400px",
    )

app = rx.App()
app.add_page(index)
```

## Documentation

See the `docs/` directory for detailed documentation on each feature:

| Doc | Feature |
|-----|---------|
| [01_context_menu.md](docs/01_context_menu.md) | Right-click context menu |
| [02_range_selection.md](docs/02_range_selection.md) | Bulk cell selection |
| [03_cell_flash.md](docs/03_cell_flash.md) | Flashing cell changes |
| [04_jump_highlight.md](docs/04_jump_highlight.md) | Jump to row & highlight |
| [05_grouping.md](docs/05_grouping.md) | Row grouping & aggregation |
| [06_notifications.md](docs/06_notifications.md) | Notification panel (demo-only) |
| [07_validation.md](docs/07_validation.md) | Data validation |
| [08_clipboard.md](docs/08_clipboard.md) | Copy with/without formatting |
| [09_excel_export.md](docs/09_excel_export.md) | Excel/CSV export |
| [10_websocket.md](docs/10_websocket.md) | Real-time updates |
| [11_cell_editors.md](docs/11_cell_editors.md) | Cell editor types |
| [12_edit_pause.md](docs/12_edit_pause.md) | Pause updates while editing |
| [13_transaction_api.md](docs/13_transaction_api.md) | Efficient delta updates |
| [14_background_tasks.md](docs/14_background_tasks.md) | Scheduled updates |
| [15_column_state.md](docs/15_column_state.md) | Save/restore column layout |
| [16_cell_renderers.md](docs/16_cell_renderers.md) | Custom cell rendering |
| [17_tree_data.md](docs/17_tree_data.md) | Hierarchical tree structure |
| [18_performance.md](docs/18_performance.md) | Large dataset performance |
| [19_status_bar.md](docs/19_status_bar.md) | Row counts & aggregations |
| [20_overlays.md](docs/20_overlays.md) | Loading/no-rows overlays |
| [21_crud_data_source.md](docs/21_crud_data_source.md) | CRUD operations |


## Demo App

Run the demo app to see all features in action:

```bash
cd reflex_ag_grid/examples/demo_app
uv run reflex run
# Open http://localhost:3000
```

## Column Definitions

Use `ag_grid.column_def()` helper for column configuration:

```python
columns = [
    # Basic column
    ag_grid.column_def(field="name", header_name="Name"),
    
    # Sortable + filterable
    ag_grid.column_def(
        field="price",
        header_name="Price",
        sortable=True,
        filter="agNumberColumnFilter",
    ),
    
    # Dropdown editor
    ag_grid.column_def(
        field="sector",
        editable=True,
        cell_editor="agSelectCellEditor",
        cell_editor_params={"values": ["Tech", "Finance", "Healthcare"]},
    ),
    
    # Grouping with aggregation
    ag_grid.column_def(
        field="sector",
        row_group=True,
        hide=True,
    ),
    ag_grid.column_def(
        field="price",
        agg_func="avg",  # sum, avg, min, max, count
    ),
]
```

## Value Formatters

Display formatted values while copying raw:

```python
ag_grid.column_def(
    field="price",
    # Display: $175.50
    value_formatter=rx.Var(
        "(params) => '$' + params.value.toFixed(2)"
    ).to(rx.EventChain),
)

ag_grid.column_def(
    field="market_cap",
    # Display: $175bn
    value_formatter=rx.Var(
        """(params) => {
            const val = params.value;
            if (val >= 1e9) return '$' + (val / 1e9).toFixed(0) + 'bn';
            return '$' + val;
        }"""
    ).to(rx.EventChain),
)
```

When copied (Ctrl+C), only the raw value is copied (175.5, not $175.50).
See [08_clipboard.md](docs/08_clipboard.md) for details.

## Events

All events receive sanitized data (no circular references):

| Event | Payload |
|-------|---------|
| `on_cell_value_changed` | `{rowId, field, oldValue, newValue, rowData}` |
| `on_row_clicked` | `{rowId, rowData}` |
| `on_row_double_clicked` | `{rowId, rowData}` |
| `on_selection_changed` | `{selectedRows, selectedCount}` |
| `on_grid_ready` | Grid API event |

## Enterprise Features

These require AG Grid Enterprise license:

- Row Grouping & Aggregation
- Range Selection
- Excel Export
- Context Menu
- Clipboard (copy with headers)

## License

Requires AG Grid Enterprise license for production use without watermark.
