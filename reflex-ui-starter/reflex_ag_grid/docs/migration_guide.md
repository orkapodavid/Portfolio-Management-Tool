# Migration Guide: From rx.el.table to AG Grid

This guide helps you migrate from Reflex's basic `rx.el.table` to the Enterprise AG Grid wrapper.

## Why Migrate?

| Feature | rx.el.table | AG Grid |
|---------|-------------|---------|
| Sorting | Manual implementation | Built-in |
| Filtering | Manual implementation | Built-in filters |
| Editing | Not supported | Inline editing |
| Pagination | Manual implementation | Built-in |
| Excel Export | Not supported | One-click export |
| Performance | Struggles with >100 rows | Handles millions |
| Selection | Manual state | Built-in selection API |

## Quick Migration

### Before: rx.el.table

```python
import reflex as rx

class State(rx.State):
    data: list[dict] = [
        {"name": "Alice", "age": 30, "city": "NYC"},
        {"name": "Bob", "age": 25, "city": "LA"},
    ]

def table_view():
    return rx.el.table(
        rx.el.thead(
            rx.el.tr(
                rx.el.th("Name"),
                rx.el.th("Age"),
                rx.el.th("City"),
            )
        ),
        rx.el.tbody(
            rx.foreach(
                State.data,
                lambda row: rx.el.tr(
                    rx.el.td(row["name"]),
                    rx.el.td(row["age"]),
                    rx.el.td(row["city"]),
                )
            )
        ),
    )
```

### After: AG Grid

```python
import reflex as rx
from reflex_ag_grid import ag_grid

class State(rx.State):
    data: list[dict] = [
        {"id": "1", "name": "Alice", "age": 30, "city": "NYC"},
        {"id": "2", "name": "Bob", "age": 25, "city": "LA"},
    ]

def table_view():
    return ag_grid(
        id="my_grid",
        row_data=State.data,
        column_defs=[
            ag_grid.column_def(field="name", header_name="Name"),
            ag_grid.column_def(field="age", header_name="Age"),
            ag_grid.column_def(field="city", header_name="City"),
        ],
        row_id_key="id",
        theme="quartz",
        width="100%",
        height="400px",
    )
```

## Step-by-Step Migration

### Step 1: Add Row IDs

AG Grid needs unique row identifiers. Add an `id` field if you don't have one:

```python
# Before
data = [{"name": "Alice", "age": 30}]

# After
data = [{"id": "1", "name": "Alice", "age": 30}]
```

Or use another unique field with `row_id_key`:

```python
ag_grid(
    ...
    row_id_key="email",  # Use email as row ID
)
```

### Step 2: Convert Headers to Column Definitions

| rx.el.table | AG Grid |
|-------------|---------|
| `rx.el.th("Name")` | `ag_grid.column_def(field="name", header_name="Name")` |
| `rx.el.th("Age")` | `ag_grid.column_def(field="age", header_name="Age")` |

### Step 3: Replace foreach with row_data

```python
# Before
rx.foreach(State.data, lambda row: rx.el.tr(...))

# After
ag_grid(row_data=State.data, ...)
```

### Step 4: Add Features

Now add the features you previously had to build manually:

```python
ag_grid(
    id="my_grid",
    row_data=State.data,
    column_defs=[
        ag_grid.column_def(
            field="name",
            header_name="Name",
            sortable=True,           # Click header to sort
            filter="agTextColumnFilter",  # Add text filter
        ),
        ag_grid.column_def(
            field="age",
            header_name="Age",
            sortable=True,
            filter="agNumberColumnFilter",  # Number filter
            editable=True,           # Allow editing
        ),
    ],
    row_selection="multiple",        # Multi-select with checkboxes
    pagination=True,                 # Built-in pagination
    pagination_page_size=10,
)
```

## Common Patterns

### Pattern 1: Manual Sorting → Built-in Sorting

**Before:**
```python
class State(rx.State):
    data: list[dict] = [...]
    sort_field: str = ""
    sort_asc: bool = True
    
    @rx.var
    def sorted_data(self) -> list[dict]:
        return sorted(self.data, key=lambda x: x[self.sort_field], reverse=not self.sort_asc)
```

**After:**
```python
ag_grid.column_def(field="name", sortable=True)
# Sorting is automatic!
```

### Pattern 2: Manual Filter → Built-in Filter

**Before:**
```python
class State(rx.State):
    search_text: str = ""
    
    @rx.var
    def filtered_data(self) -> list[dict]:
        return [r for r in self.data if self.search_text.lower() in r["name"].lower()]
```

**After:**
```python
ag_grid(
    quick_filter_text=State.search_text,  # Global search
    ...
)
# Or per-column filters:
ag_grid.column_def(field="name", filter="agTextColumnFilter")
```

### Pattern 3: Click Handler → Selection Events

**Before:**
```python
def row_item(row):
    return rx.el.tr(
        rx.el.td(row["name"]),
        on_click=State.select_row(row["id"]),
    )
```

**After:**
```python
ag_grid(
    on_row_clicked=State.on_row_click,
    row_selection="single",
)

# In State:
def on_row_click(self, row_index: int, field: str, value: str):
    # Handle click
    pass
```

### Pattern 4: Manual Pagination → Built-in Pagination

**Before:**
```python
class State(rx.State):
    page: int = 0
    page_size: int = 10
    
    @rx.var
    def paginated_data(self) -> list[dict]:
        start = self.page * self.page_size
        return self.data[start:start + self.page_size]
```

**After:**
```python
ag_grid(
    pagination=True,
    pagination_page_size=10,
    pagination_page_size_selector=[10, 25, 50],
)
```

### Pattern 5: Editable Cells

**Before:** Not supported in rx.el.table

**After:**
```python
ag_grid(
    column_defs=[
        ag_grid.column_def(
            field="price",
            editable=True,
            cell_editor="agNumberCellEditor",
        ),
    ],
    on_cell_value_changed=State.on_cell_edit,
)

# In State:
def on_cell_edit(self, row_index: int, field: str, new_value: str):
    self.data[row_index][field] = new_value
```

## Troubleshooting

### Grid not showing

**Problem:** Grid renders but no data appears.

**Solutions:**
1. Check `row_data` is a valid list of dicts
2. Ensure `column_defs` field names match your data keys
3. Add height: `height="400px"`

### Row IDs not working

**Problem:** Selection/updates don't work correctly.

**Solution:** Always specify `row_id_key`:
```python
ag_grid(row_id_key="id", ...)
```

### Events not firing

**Problem:** `on_cell_value_changed` not called.

**Solution:** Check event handler signature matches expected format:
```python
# Correct
def on_cell_edit(self, row_index: int, field: str, new_value: str):
    pass

# Incorrect
def on_cell_edit(self, event: dict):  # Wrong signature
    pass
```

### Styling doesn't match app theme

**Solution:** Use theme prop with color mode:
```python
ag_grid(theme="quartz", ...)  # Auto light/dark mode
```

### Large data is slow

**Solution:** Use pagination or virtualization (default):
```python
ag_grid(
    pagination=True,
    pagination_page_size=50,
)
```

## Feature Comparison Checklist

Use this checklist when migrating:

- [ ] Replace `rx.el.table` with `ag_grid()`
- [ ] Replace `rx.el.th()` with `ag_grid.column_def()`
- [ ] Replace `rx.foreach()` with `row_data=State.data`
- [ ] Add `row_id_key="id"` for proper row identification
- [ ] Add `theme="quartz"` for consistent styling
- [ ] Add `width` and `height` for proper sizing
- [ ] Migrate sorting logic → `sortable=True`
- [ ] Migrate filtering logic → `filter="agTextColumnFilter"`
- [ ] Migrate pagination logic → `pagination=True`
- [ ] Update event handlers to match AG Grid signatures

## Need More Help?

- See [README.md](../README.md) for API reference
- See [docs/](.) for feature-specific guides
- Run the demo app: `cd examples/demo_app && reflex run`
