# 23 - Set Filter

Enterprise multi-select checkbox filter for categorical columns.

## Route
`/23-set-filter`

## AG Grid Props
```python
# Mixed filter configuration
column_defs = [
    {
        "field": "sector",
        "filter": "agSetColumnFilter",  # Checkbox filter
    },
    {
        "field": "price",
        "filter": "agNumberColumnFilter",  # Number filter
    },
]

# Auto-size columns to fit content
auto_size_strategy = {"type": "fitCellContents"}
```

## Features
- **Set Filter**: Multi-select checkboxes for categorical columns (Sector, Status)
- **Text/Number Filter**: Standard filters for other columns
- **Search**: Search within Set Filter values
- **Auto-Size**: Columns automatically resize to fit content

## Usage Note
- **Row Selection**: Use checkboxes on the far left to select rows.
- **Filtering**: Click column menu filter icons to filter data.

## Demo Code
```python
columns = [
    {
        "field": "sector",
        "filter": "agSetColumnFilter",
        "filterParams": {"buttons": ["reset", "apply"]},
    },
    {
        "field": "price",
        "filter": "agNumberColumnFilter",
    },
]

ag_grid(
    id="my_grid",
    row_data=state.data,
    column_defs=columns,
    side_bar="filters",
    auto_size_strategy={"type": "fitCellContents"},
)
```

## Requirements
- AG Grid Enterprise license (for Set Filter)
