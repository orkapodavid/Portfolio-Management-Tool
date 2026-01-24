# Reflex AG Grid Enterprise Wrapper

A generic, reusable AG Grid Enterprise wrapper for Reflex Python applications.

## Features

- ✅ **AG Grid Enterprise** - Full feature set (grouping, range selection, Excel export, context menu)
- ✅ **Type-Safe** - Pydantic models for column definitions and validation
- ✅ **Registry Pattern** - Formatters and renderers as string keys (no serialization issues)
- ✅ **Event Sanitization** - Safe event data without circular references
- ✅ **Column Persistence** - Auto-save column state to localStorage
- ✅ **Notifications** - Built-in notification system with jump-to-row

## Installation

This package is designed as a local package that can be copied between repositories.

1. Copy the `reflex_ag_grid/` folder to your project root
2. Add AG Grid dependencies to your `package.json`:

```json
{
  "dependencies": {
    "ag-grid-react": "^31.3.0",
    "ag-grid-enterprise": "^31.3.0",
    "ag-grid-community": "^31.3.0"
  }
}
```

3. Set your license key (optional, but removes watermark):

```python
# In your app
import os
# Set via environment variable
os.environ["AG_GRID_LICENSE_KEY"] = "your-license-key"

# Or pass directly to component
AGGrid.create(..., license_key="your-license-key")
```

## Quick Start

```python
import reflex as rx
from reflex_ag_grid import AGGrid, AGGridStateMixin, ColumnDef

class MyState(rx.State, AGGridStateMixin):
    """State with AG Grid mixin for notifications and grid control."""
    
    items: list[dict] = [
        {"id": "1", "name": "Apple", "price": 1.50, "quantity": 100},
        {"id": "2", "name": "Banana", "price": 0.75, "quantity": 200},
        {"id": "3", "name": "Cherry", "price": 3.00, "quantity": 50},
    ]
    
    def handle_cell_edit(self, data: dict):
        """Called when user edits a cell."""
        row_id = data["rowId"]
        field = data["field"]
        new_value = data["newValue"]
        
        # Update local state
        self.update_row_data("items", row_id, {field: new_value})
        
        # Add notification
        self.add_notification(
            message=f"Updated {field} to {new_value}",
            row_id=row_id,
            notification_type="success"
        )


def my_grid():
    """Grid component."""
    return AGGrid.create(
        column_defs=[
            ColumnDef(field="id", header_name="ID", editable=False, width=80),
            ColumnDef(field="name", header_name="Name", editable=True),
            ColumnDef(
                field="price", 
                header_name="Price", 
                type="number",
                editable=True,
                formatter="currency",  # Uses registry
            ),
            ColumnDef(
                field="quantity", 
                header_name="Qty", 
                type="integer",
                editable=True,
                formatter="number",
            ),
        ],
        row_data=MyState.items,
        on_cell_edit=MyState.handle_cell_edit,
        on_selection_change=MyState.handle_selection_change,
        grid_id="products",
        height="500px",
    )


def index():
    return rx.box(
        my_grid(),
        padding="20px",
    )


app = rx.App()
app.add_page(index)
```

## Column Definitions

Use the `ColumnDef` Pydantic model for type-safe column configuration:

```python
from reflex_ag_grid import ColumnDef, ColumnType

columns = [
    # Basic text column
    ColumnDef(field="name", header_name="Name"),
    
    # Number with formatting
    ColumnDef(
        field="price",
        header_name="Price",
        type=ColumnType.NUMBER,
        formatter="currency",  # Registry key
        editable=True,
    ),
    
    # Enum with dropdown editor
    ColumnDef(
        field="status",
        header_name="Status",
        type=ColumnType.ENUM,
        enum_values=["Active", "Pending", "Cancelled"],
        editable=True,
    ),
    
    # Boolean with checkbox
    ColumnDef(
        field="is_active",
        header_name="Active",
        type=ColumnType.BOOLEAN,
        editable=True,
    ),
    
    # Grouped column with aggregation
    ColumnDef(
        field="category",
        header_name="Category",
        row_group=True,
        hide=True,  # Hide when grouped
    ),
    ColumnDef(
        field="total",
        header_name="Total",
        type=ColumnType.NUMBER,
        agg_func="sum",  # Show sum in group rows
        formatter="currency",
    ),
    
    # Conditional styling
    ColumnDef(
        field="change",
        header_name="Change %",
        type=ColumnType.FLOAT,
        formatter="percentage",
        cell_class_rules="traffic_light",  # Green/red based on value
    ),
]
```

## Formatter Registry

Available formatters (use as string keys):

| Key | Description | Example |
|-----|-------------|---------|
| `currency` | USD currency | $1,234.56 |
| `currency_jpy` | JPY currency | ¥1,234 |
| `percentage` | Multiply by 100 | 12.34% |
| `percentage_value` | Already percentage | 12.34% |
| `number` | Comma-separated | 1,234,567 |
| `decimal` | Two decimals | 1,234.56 |
| `date` | ISO date | 2024-01-15 |
| `datetime` | Local datetime | 1/15/2024, 2:30 PM |
| `boolean` | Yes/No | Yes |
| `uppercase` | Uppercase text | HELLO |

### Adding Custom Formatters

Edit `ag_grid_wrapper.js` to add custom formatters:

```javascript
const FORMATTER_REGISTRY = {
    // ... existing formatters ...
    
    // Add your custom formatter
    my_custom: (params) => {
        if (params.value == null) return '';
        return `Custom: ${params.value}`;
    },
};
```

Then use in Python:

```python
ColumnDef(field="myfield", formatter="my_custom")
```

## Cell Class Rules

Available cell styling rules:

| Key | Description |
|-----|-------------|
| `traffic_light` | Green for positive, red for negative |
| `threshold` | Green ≥100, yellow ≥50, red <50 |
| `bold_nonzero` | Bold for non-zero values |

## Validation

Use Pydantic models for validation:

```python
from reflex_ag_grid import ValidationSchema, FieldValidation

schema = ValidationSchema(
    fields=[
        FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=10000,
            required=True,
        ),
        FieldValidation(
            field_name="email",
            field_type="string",
            pattern=r"^[\w.-]+@[\w.-]+\.\w+$",
        ),
    ]
)

# Pass to grid
AGGrid.create(
    column_defs=columns,
    row_data=data,
    validation_schema=schema,
)
```

## Grid Control

Use the state mixin methods to control the grid:

```python
class MyState(rx.State, AGGridStateMixin):
    def on_button_click(self):
        # Jump to specific row
        return self.jump_to_row("row_123", grid_id="my_grid")
    
    def export_data(self):
        # Trigger Excel export
        return self.export_to_excel(grid_id="my_grid")
    
    def reset_view(self):
        # Reset column positions/widths
        return self.reset_column_state(grid_id="my_grid")
```

## Events

All events receive sanitized data (no circular references):

| Event | Payload |
|-------|---------|
| `on_cell_edit` | `{rowId, field, oldValue, newValue, rowData}` |
| `on_row_click` | `{rowId, rowData}` |
| `on_row_double_click` | `{rowId, rowData}` |
| `on_row_right_click` | `{rowId, rowData, clientX, clientY}` |
| `on_selection_change` | `{selectedRows, selectedCount}` |
| `on_grid_ready` | `{gridId}` |

## License

Requires AG Grid Enterprise license for production use without watermark.
