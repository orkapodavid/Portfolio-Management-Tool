# 24 - Multi Filter

Enterprise combined filter with multiple filter types in one column.

## Route
`/24-multi-filter`

## AG Grid Props
```python
# In column definition
{
    "field": "sport",
    "filter": "agMultiColumnFilter",
    "filterParams": {
        "filters": [
            {"filter": "agTextColumnFilter"},
            {"filter": "agSetColumnFilter"},
        ],
    },
}
```

## Features
- Combines multiple filter types (Text + Set, Number + Set)
- Tabbed interface for switching between filters
- Each filter operates independently

## Demo Code
```python
columns = [
    {
        "field": "symbol",
        "filter": "agMultiColumnFilter",
        "filterParams": {
            "filters": [
                {"filter": "agTextColumnFilter"},
                {"filter": "agSetColumnFilter"},
            ],
        },
    },
]

ag_grid(
    id="my_grid",
    row_data=state.data,
    column_defs=columns,
)
```

## Requirements
- AG Grid Enterprise license
