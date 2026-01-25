# 16 - Cell Renderers

**Requirement**: Custom cell styling for conditional formatting  
**AG Grid Feature**: `cellStyle`, `cellClass`, `cellClassRules`  
**Demo Route**: `/16-cell-renderers`

## Overview

Cell styling allows you to customize the appearance of individual cells based on their values. This is useful for:
- Highlighting important values (positive/negative numbers)
- Creating badge/pill styled status columns
- Making clickable link-style columns

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `cell_style` | JS function returning CSS style object |
| `cell_class` | JS function returning CSS class name(s) |
| `cell_class_rules` | Object mapping class names to conditions |

## Code Examples

### 1. Static Style (Link Style)

```python
_LINK_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

ag_grid.column_def(
    field="ticker",
    header_name="Ticker",
    cell_style=_LINK_STYLE,
)
```

### 2. Conditional Color (Green/Red)

```python
_CHANGE_STYLE = rx.Var(
    """(params) => {
        const val = parseFloat(params.value);
        if (isNaN(val)) return {};
        return {
            color: val >= 0 ? '#059669' : '#dc2626',
            fontWeight: '500'
        };
    }"""
)

ag_grid.column_def(
    field="change",
    header_name="Change %",
    cell_style=_CHANGE_STYLE,
)
```

### 3. Badge Style (Rounded Pill)

```python
_BADGE_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const isOpen = val.includes('open');
        return {
            backgroundColor: isOpen ? '#d1fae5' : '#fee2e2',
            color: isOpen ? '#065f46' : '#991b1b',
            padding: '2px 8px',
            borderRadius: '9999px',
            fontSize: '11px',
            fontWeight: '500',
            display: 'inline-block'
        };
    }"""
)

ag_grid.column_def(
    field="status",
    header_name="Status",
    cell_style=_BADGE_STYLE,
)
```

## Why Not cellRenderer?

AG Grid React does NOT support:
1. `cellRenderer` returning DOM elements → Crashes React
2. HTML string returns → Escaped as text

**Use `cellStyle` instead** for most styling needs.

## How to Implement

1. Define your cell style as `rx.Var` containing a JS function
2. The function receives `params` with `.value` and other cell data
3. Return a CSS style object (camelCase properties)
4. Pass the `rx.Var` to `cell_style` in `ag_grid.column_def()`

## Related Documentation

- [AG Grid Cell Styles](https://www.ag-grid.com/javascript-data-grid/cell-styles/)
