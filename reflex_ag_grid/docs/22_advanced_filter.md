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
# Helper to find Grid API
GET_API_JS = """(function() {
    const wrapper = document.querySelector('.ag-root-wrapper');
    // ... logic to find api from __reactFiber ...
    return fiber?.stateNode?.api;
})()"""

# Use API in event handlers
rx.call_script(f"const api = {GET_API_JS}; api?.showAdvancedFilterBuilder()")
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
