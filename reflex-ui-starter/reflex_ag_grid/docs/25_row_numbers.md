# 25 - Row Numbers

Automatic row numbering column (v33.1+).

## Route
`/25-row-numbers`

## AG Grid Props
```python
row_numbers=True
# or with options
row_numbers={"allowShowHide": True}
```

## Features
- Automatic row numbering column on the left
- Numbers update with sort/filter
- Works with grouping

## Demo Code
```python
ag_grid(
    id="my_grid",
    row_data=state.data,
    column_defs=columns,
    row_numbers=True,
)
```

## Known Limitations
> [!WARNING]
> This feature requires `RowNumbersModule` in AG Grid v35+.
> May require additional module registration in the Reflex wrapper.

## Requirements
- AG Grid v33.1+
- `RowNumbersModule` must be registered
