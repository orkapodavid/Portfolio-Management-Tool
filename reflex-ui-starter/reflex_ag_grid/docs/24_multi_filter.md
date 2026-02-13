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
            {
                "filter": "agTextColumnFilter",
                "display": "accordion",  # Show as expandable section
                "title": "Text Filter",
            },
            {
                "filter": "agSetColumnFilter",
                "display": "accordion",
                "title": "Set Filter",
            },
        ],
    },
}
```

## Features
- Combines multiple filter types (Text + Set, Number + Set)
- **Accordion interface** for switching between filters
- Each filter operates independently
- Display options: `'inline'`, `'accordion'`, `'subMenu'`

## Demo Code
```python
columns = [
    {
        "field": "symbol",
        "filter": "agMultiColumnFilter",
        "filterParams": {
            "filters": [
                {"filter": "agTextColumnFilter", "display": "accordion", "title": "Text"},
                {"filter": "agSetColumnFilter", "display": "accordion", "title": "Set"},
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
