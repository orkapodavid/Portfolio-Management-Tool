# Performance Guide

AG Grid is designed to handle large datasets efficiently. This guide explains how to get the best performance with Reflex.

## 1. Use `row_data` Prop

**Always** pass your data list directly to the `row_data` prop.

```python
# ✅ GOOD - Fast
ag_grid(
    row_data=State.data,  # Passed as a single JSON object
    column_defs=...,
)

# ❌ BAD - Slow
rx.foreach(
    State.data,
    lambda row: ... # Generates individual components per row
)
```

## 2. Row IDs

AG Grid needs stable Row IDs to handle updates efficiently. Without them, it may re-render the entire grid on every change.

```python
# ✅ GOOD
ag_grid(
    row_data=State.data,
    row_id_key="id",  # Field to use as unique ID
)
```

## 3. Efficient State Updates

When updating data, try to update only the changed rows if possible.

Reflex checks for object equality. If you replace the entire list, it triggers a full grid refresh.
However, `reflex-ag-grid` is optimized to handle this reasonably well.

For granular updates (e.g. flashing a single cell), use the `AGGridStateMixin` methods:

```python
# Updates specific row without replacing whole dataset
self.update_row_data(
    data_attr="items",
    row_id="123",
    updates={"status": "complete"}
)
```

## 4. Column Configuration

- **Suppress Auto-Size**: Auto-sizing columns (`size_columns_to_fit`) can be slow for large grids.
- **Fixed Widths**: Define `width` or `flex` for columns to avoid layout thrashing.

## 5. Pagination vs Virtualization

AG Grid uses row virtualization by default (DOM virtualization). It can handle ~100k rows smoothly.

For very large datasets (>10k rows), enabling pagination improves initial load time and browser responsiveness.

```python
ag_grid(
    pagination=True,
    pagination_page_size=100,
)
```

## 6. Theme Performance

The `quartz` theme is more complex than `balham`. If you need maximum rendering speed for high-frequency updates, `balham` might be slightly faster (though minimal difference in modern browsers).
