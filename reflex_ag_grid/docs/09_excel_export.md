# 09 - Excel Export

**Requirement**: Export grid data to Excel  
**AG Grid Feature**: Enterprise Excel Export  
**Demo Route**: `/09-excel-export`

## Overview

AG Grid Enterprise provides native Excel export that maintains formatting, column widths, and can include grouped data.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `api.exportDataAsExcel()` | Export to .xlsx |
| `api.exportDataAsCsv()` | Export to .csv |
| Export params | Customize export options |

## Code Example

```python
from reflex_ag_grid import export_excel, export_csv
import reflex as rx

class State(rx.State):
    def export_to_excel(self):
        return export_excel("my_grid", filename="data.xlsx")
    
    def export_to_csv(self):
        return export_csv("my_grid", filename="data.csv")

# UI
rx.button("Export Excel", on_click=State.export_to_excel)
rx.button("Export CSV", on_click=State.export_to_csv)
```

## Export Options

```javascript
gridApi.exportDataAsExcel({
    fileName: 'export.xlsx',
    sheetName: 'Data',
    skipGroups: true,
    skipHeader: false,
    columnKeys: ['symbol', 'price'],  // Specific columns only
});
```

## Features

- **Excel format** - Native .xlsx with formatting
- **CSV format** - Simple comma-separated
- **Column selection** - Export specific columns
- **Include headers** - Optional header row
- **Skip groups** - Export flat data only

## How to Implement

1. Import `export_excel` or `export_csv` from `reflex_ag_grid`
2. Call with grid ID and optional filename
3. File downloads to user's browser

## Related Documentation

- [AG Grid Excel Export](https://www.ag-grid.com/javascript-data-grid/excel-export/)
</Parameter>
<parameter name="Complexity">3
