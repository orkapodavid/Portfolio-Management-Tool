# 23 - Set Filter

Enterprise multi-select checkbox filter for categorical columns.

## Route
`/23-set-filter`

## AG Grid Props
```python
# In column definition
{
    "field": "sector",
    "filter": "agSetColumnFilter",
    "filterParams": {
        "buttons": ["reset", "apply"],
    },
}
```

## Features
- Checkbox-based multi-select filtering
- Search within filter values
- Select All / Deselect All
- Works best with categorical data

## Demo Code
```python
columns = [
    {
        "field": "sector",
        "filter": "agSetColumnFilter",
        "filterParams": {"buttons": ["reset", "apply"]},
    },
]

ag_grid(
    id="my_grid",
    row_data=state.data,
    column_defs=columns,
    side_bar="filters",  # Shows filter panel
)
```

## Requirements
- AG Grid Enterprise license
