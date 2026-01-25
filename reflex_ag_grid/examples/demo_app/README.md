# AG Grid Demo App

A multi-page Reflex application demonstrating all 15 AG Grid requirements.

## Pages

| Page | Route | Requirements Covered |
|------|-------|---------------------|
| **Basic Grid** | `/` | Req 1, 8, 9 (context menu, copy, export) |
| **Editable Grid** | `/editable` | Req 7, 11, 12 (validation, cell editors, pause on edit) |
| **Grouped Grid** | `/grouped` | Req 5 (grouping & aggregation) |
| **Streaming Data** | `/streaming` | Req 3, 6, 10, 13, 14 (flash, notifications, updates) |
| **Range Selection** | `/range` | Req 2 (bulk range selection) |
| **Column State** | `/column-state` | Req 15 (save table format) |

## Running the Demo

```bash
cd reflex_ag_grid/examples/demo_app
uv run reflex run
```

Open http://localhost:3000 in your browser.

## Features Demonstrated

### Core Features
- ✅ Column definitions with Pydantic models
- ✅ Cell formatters (currency, percentage, number)
- ✅ Context menu (right-click)
- ✅ Excel/CSV export buttons

### Editing & Validation
- ✅ Different cell editors (text, number, select, checkbox)
- ✅ Validation with error feedback
- ✅ Pause updates while editing toggle

### Data Updates
- ✅ Cell flash on value change (`enableCellChangeFlash`)
- ✅ Notifications panel with jump-to-row
- ✅ Manual and streaming update modes
- ✅ Transaction API for efficient updates

### Enterprise Features
- ✅ Range selection (Shift+click)
- ✅ Row grouping with aggregation
- ✅ Column state persistence (localStorage)

## E2E Testing

```bash
# Run tests (requires demo app running)
uv run python reflex_ag_grid/tests/e2e_ag_grid.py --url http://localhost:3000
```
