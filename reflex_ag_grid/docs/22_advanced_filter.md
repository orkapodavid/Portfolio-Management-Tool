# 22 - Advanced Filter

Enterprise feature for complex filter expressions with builder UI.

## Route
`/22-advanced-filter`

## AG Grid Props
```python
enable_advanced_filter=True
side_bar=True  # Shows filter panel
```

## Features
- Builder UI for complex AND/OR filter logic
- Filter expressions saved/restored via `advancedFilterModel`
- Works with all column types

## API Methods
```python
# Show the filter builder
rx.call_script("refs['ref_grid_id']?.current?.api?.showAdvancedFilterBuilder()")

# Clear filters
rx.call_script("refs['ref_grid_id']?.current?.api?.setAdvancedFilterModel(null)")
```

## Demo Code
```python
ag_grid(
    id="my_grid",
    row_data=state.data,
    column_defs=columns,
    enable_advanced_filter=True,
    side_bar=True,
)
```

## Screenshot
The Advanced Filter builder shows a visual expression builder.

## Requirements
- AG Grid Enterprise license
- v32.0.0+ (enhanced in v35)
